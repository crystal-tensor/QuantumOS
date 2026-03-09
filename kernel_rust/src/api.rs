use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use kernel_rust::scheduler::{Scheduler, QuantumTask, TaskType};

#[derive(Debug, Deserialize, Serialize)]
#[serde(untagged)]
pub enum Operand {
    Integer(i64),
    Float(f64),
}

#[derive(Debug, Deserialize, Serialize)]
pub struct QisaInstruction {
    pub opcode: String,
    pub operands: Vec<Operand>,
    #[serde(default)]
    pub target_qubits: Option<Vec<u32>>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct JobRequest {
    pub job_id: String,
    pub tenant_id: Option<String>,
    pub required_qubits: u32,
    pub expected_duration_ns: u64,
    #[serde(default)]
    pub priority: i32,
    pub qisa_instructions: Vec<QisaInstruction>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct JobResponse {
    pub job_id: String,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<serde_json::Value>,
}

pub async fn submit_job(
    State(state): State<Arc<Mutex<Scheduler>>>,
    Json(payload): Json<JobRequest>,
) -> Response {
    {
        let mut scheduler = state.lock().unwrap();

        let priority = if payload.priority < 0 { 0 } else { payload.priority as u32 };

        let task = QuantumTask {
            id: payload.job_id.clone(),
            priority,
            task_type: TaskType::Job,
            duration_ns: payload.expected_duration_ns,
        };

        scheduler.add_task(task);
    }
    
    // Forward to Simulator
    let client = reqwest::Client::new();
    let sim_res = client.post("http://localhost:8001/driver/run")
        .json(&payload.qisa_instructions)
        .send()
        .await;

    let (status, result) = match sim_res {
        Ok(resp) => {
            if resp.status().is_success() {
                let json: serde_json::Value = resp.json().await.unwrap_or(serde_json::json!({}));
                ("COMPLETED".to_string(), Some(json))
            } else {
                ("FAILED_SIM".to_string(), Some(serde_json::json!({"error": resp.status().to_string()})))
            }
        },
        Err(e) => {
            ("FAILED_CONN".to_string(), Some(serde_json::json!({"error": e.to_string()})))
        }
    };

    let response = JobResponse {
        job_id: payload.job_id,
        status,
        result,
    };

    (StatusCode::OK, Json(response)).into_response()
}

#[cfg(test)]
mod tests {
    use super::*;
    use axum::body::Body;
    use axum::http::{Request, header};
    use tower::util::ServiceExt;
    use axum::routing::post;
    use axum::Router;

    #[tokio::test]
    async fn test_submit_job() {
        let scheduler = Arc::new(Mutex::new(Scheduler::new()));
        let app = Router::new()
            .route("/api/v1/submit_job", post(submit_job))
            .with_state(scheduler.clone());

        let job_request = serde_json::json!({
            "job_id": "test-job-123",
            "tenant_id": "tenant-1",
            "required_qubits": 2,
            "expected_duration_ns": 1000,
            "priority": 10,
            "qisa_instructions": [
                {
                    "opcode": "H",
                    "operands": [0]
                }
            ]
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/v1/submit_job")
                    .header(header::CONTENT_TYPE, "application/json")
                    .body(Body::from(job_request.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let scheduler = scheduler.lock().unwrap();
        assert_eq!(scheduler.task_count(), 1);
        let task = scheduler.peek_task().unwrap();
        assert_eq!(task.id, "test-job-123");
        assert_eq!(task.priority, 10);
    }
    
    #[tokio::test]
    async fn test_submit_job_invalid_json() {
        let scheduler = Arc::new(Mutex::new(Scheduler::new()));
        let app = Router::new()
            .route("/api/v1/submit_job", post(submit_job))
            .with_state(scheduler);

        let invalid_request = serde_json::json!({
            "job_id": "test-job-123",
            // missing required fields
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/v1/submit_job")
                    .header(header::CONTENT_TYPE, "application/json")
                    .body(Body::from(invalid_request.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    }
}
