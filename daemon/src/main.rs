//! Weave Daemon — contributes idle compute to the Weave network.
//!
//! Responsibilities:
//! - Device capability profiling (CPU, RAM, GPU, bandwidth)
//! - Job execution in sandboxed environment
//! - Activation vector passing to/from peer nodes
//! - Idle detection (screen off, plugged in, on WiFi)
//! - Heartbeat reporting to coordinator

mod config;
mod profiler;

use clap::Parser;
use tracing::{info, Level};
use tracing_subscriber::EnvFilter;

/// Weave Device Daemon
#[derive(Parser, Debug)]
#[command(name = "weave-daemon", version, about = "Weave P2P compute contributor")]
struct Args {
    /// Coordinator URL to register with
    #[arg(long, default_value = "http://localhost:8000")]
    coordinator_url: String,

    /// Maximum percentage of CPU to donate
    #[arg(long, default_value_t = 80)]
    max_cpu_percent: u8,

    /// Maximum percentage of RAM to donate
    #[arg(long, default_value_t = 60)]
    max_ram_percent: u8,

    /// Only contribute when device is idle
    #[arg(long, default_value_t = true)]
    idle_only: bool,

    /// Log level
    #[arg(long, default_value = "info")]
    log_level: String,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let args = Args::parse();

    // Structured logging setup
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new(&args.log_level)),
        )
        .json()
        .init();

    info!(
        coordinator_url = %args.coordinator_url,
        max_cpu_percent = args.max_cpu_percent,
        max_ram_percent = args.max_ram_percent,
        "weave-daemon starting"
    );

    // Profile device capabilities
    let profile = profiler::DeviceProfile::detect();
    info!(
        cpu_cores = profile.cpu_cores,
        total_ram_gb = profile.total_ram_gb,
        gpu = ?profile.gpu_info,
        "device profiled"
    );

    // TODO Phase 1: Register with coordinator via libp2p
    // TODO Phase 1: Enter heartbeat loop
    // TODO Phase 1: Accept and execute assigned jobs in sandbox

    info!("weave-daemon ready — waiting for coordinator integration (Phase 1)");

    // Keep alive
    tokio::signal::ctrl_c().await?;
    info!("weave-daemon shutting down");

    Ok(())
}
