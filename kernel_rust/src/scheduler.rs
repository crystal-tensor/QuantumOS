use std::collections::BinaryHeap;
use std::cmp::Ordering;

/// 任务类型枚举
#[derive(Debug, Eq, PartialEq, Clone)]
pub enum TaskType {
    /// 门操作
    GateOperation,
    /// 测量操作
    Measurement,
    /// 等待操作
    Wait,
    /// 复合任务 (Job)
    Job,
}

/// 调度任务结构体
#[derive(Debug, Eq, PartialEq, Clone)]
pub struct QuantumTask {
    /// 任务唯一标识 (UUID)
    pub id: String,
    /// 优先级 (值越大优先级越高)
    pub priority: u32,
    /// 任务类型
    pub task_type: TaskType,
    /// 预计执行时间 (纳秒)
    pub duration_ns: u64,
}

// 为 BinaryHeap 实现 Ordering，确保按优先级从高到低排序
impl Ord for QuantumTask {
    fn cmp(&self, other: &Self) -> Ordering {
        self.priority.cmp(&other.priority)
    }
}

impl PartialOrd for QuantumTask {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

/// 基础任务调度器
pub struct Scheduler {
    /// 任务优先队列
    task_queue: BinaryHeap<QuantumTask>,
}

impl Scheduler {
    /// 创建一个新的调度器实例
    pub fn new() -> Self {
        Self {
            task_queue: BinaryHeap::new(),
        }
    }

    /// 添加任务到队列
    pub fn add_task(&mut self, task: QuantumTask) {
        self.task_queue.push(task);
    }

    /// 获取下一个最高优先级的任务
    pub fn pop_task(&mut self) -> Option<QuantumTask> {
        self.task_queue.pop()
    }

    /// 查看下一个最高优先级的任务
    pub fn peek_task(&self) -> Option<&QuantumTask> {
        self.task_queue.peek()
    }

    /// 获取当前队列中的任务数量
    pub fn task_count(&self) -> usize {
        self.task_queue.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scheduler_priority() {
        let mut scheduler = Scheduler::new();

        let task1 = QuantumTask {
            id: "1".to_string(),
            priority: 10,
            task_type: TaskType::GateOperation,
            duration_ns: 20,
        };

        let task2 = QuantumTask {
            id: "2".to_string(),
            priority: 50, // Higher priority
            task_type: TaskType::Measurement,
            duration_ns: 100,
        };

        let task3 = QuantumTask {
            id: "3".to_string(),
            priority: 5,
            task_type: TaskType::Wait,
            duration_ns: 1000,
        };

        scheduler.add_task(task1.clone());
        scheduler.add_task(task2.clone());
        scheduler.add_task(task3.clone());

        assert_eq!(scheduler.pop_task().unwrap().id, "2");
        assert_eq!(scheduler.pop_task().unwrap().id, "1");
        assert_eq!(scheduler.pop_task().unwrap().id, "3");
    }
}
