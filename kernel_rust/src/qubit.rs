/// 物理量子比特结构体
/// 映射 DeviceSpec 中的 qubit 定义
#[derive(Debug, Clone, Copy)]
pub struct PhysicalQubit {
    /// 物理量子比特 ID
    pub id: u32,
    /// 弛豫时间 (T1) - 单位: 微秒 (us)
    pub t1_us: f64,
    /// 退相干时间 (T2) - 单位: 微秒 (us)
    pub t2_us: f64,
    /// 共振频率 - 单位: GHz
    pub frequency_ghz: f64,
    /// 单次读出保真度 (0.0 - 1.0)
    pub readout_fidelity: f64,
}

impl PhysicalQubit {
    /// 创建一个新的物理量子比特实例
    ///
    /// # 参数
    ///
    /// * `id` - 物理量子比特索引
    /// * `t1_us` - 弛豫时间 (us)
    /// * `t2_us` - 退相干时间 (us)
    /// * `frequency_ghz` - 共振频率 (GHz)
    /// * `readout_fidelity` - 读出保真度 (0.0-1.0)
    pub fn new(
        id: u32,
        t1_us: f64,
        t2_us: f64,
        frequency_ghz: f64,
        readout_fidelity: f64,
    ) -> Self {
        Self {
            id,
            t1_us,
            t2_us,
            frequency_ghz,
            readout_fidelity,
        }
    }

    /// 获取 T1 时间的纳秒表示
    pub fn t1_ns(&self) -> u64 {
        (self.t1_us * 1_000.0) as u64
    }

    /// 获取 T2 时间的纳秒表示
    pub fn t2_ns(&self) -> u64 {
        (self.t2_us * 1_000.0) as u64
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_physical_qubit_creation() {
        let qubit = PhysicalQubit::new(0, 50.5, 70.2, 4.5, 0.98);
        assert_eq!(qubit.id, 0);
        assert_eq!(qubit.t1_us, 50.5);
        assert_eq!(qubit.t2_us, 70.2);
        assert_eq!(qubit.frequency_ghz, 4.5);
        assert_eq!(qubit.readout_fidelity, 0.98);
    }

    #[test]
    fn test_time_conversion() {
        let qubit = PhysicalQubit::new(1, 10.0, 20.0, 5.0, 0.99);
        assert_eq!(qubit.t1_ns(), 10_000);
        assert_eq!(qubit.t2_ns(), 20_000);
    }
}
