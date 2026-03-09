use axum::{routing::post, Router};
use std::net::SocketAddr;
use std::sync::{Arc, Mutex};
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use kernel_rust::scheduler::Scheduler;

mod api;

#[tokio::main]
async fn main() {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new(
            std::env::var("RUST_LOG").unwrap_or_else(|_| "info".into()),
        ))
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Initialize scheduler
    let scheduler = Arc::new(Mutex::new(Scheduler::new()));

    // Build application with routes
    let app = Router::new()
        .route("/api/v1/submit_job", post(api::submit_job))
        .layer(TraceLayer::new_for_http())
        .with_state(scheduler);

    // Run it
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    tracing::info!("listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
