//! Daemon configuration.

use serde::Deserialize;

/// Runtime configuration for the daemon.
#[derive(Debug, Deserialize, Clone)]
pub struct DaemonConfig {
    /// Coordinator service URL
    pub coordinator_url: String,

    /// Max CPU percentage to donate (0-100)
    pub max_cpu_percent: u8,

    /// Max RAM percentage to donate (0-100)
    pub max_ram_percent: u8,

    /// Only run jobs when device is idle
    pub idle_only: bool,

    /// Heartbeat interval in seconds
    pub heartbeat_interval_secs: u64,
}

impl Default for DaemonConfig {
    fn default() -> Self {
        Self {
            coordinator_url: "http://localhost:8000".to_string(),
            max_cpu_percent: 80,
            max_ram_percent: 60,
            idle_only: true,
            heartbeat_interval_secs: 30,
        }
    }
}
