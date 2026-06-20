//! Device capability profiling — detects CPU, RAM, GPU for shard assignment.

use sysinfo::System;

/// Detected device capabilities, reported to coordinator for shard assignment.
#[derive(Debug, Clone)]
pub struct DeviceProfile {
    pub hostname: String,
    pub os: String,
    pub cpu_cores: usize,
    pub cpu_brand: String,
    pub total_ram_gb: f64,
    pub available_ram_gb: f64,
    pub gpu_info: Option<GpuInfo>,
}

/// GPU information (if detected).
#[derive(Debug, Clone)]
pub struct GpuInfo {
    pub name: String,
    pub vram_gb: f64,
    pub backend: GpuBackend,
}

/// Which inference backend this GPU can use.
#[derive(Debug, Clone)]
pub enum GpuBackend {
    Cuda,       // NVIDIA — tinygrad/llama.cpp CUDA
    Mlx,        // Apple Silicon — MLX
    Vulkan,     // AMD/Intel — llama.cpp Vulkan
    CpuOnly,    // No GPU acceleration
}

impl DeviceProfile {
    /// Detect current device capabilities.
    pub fn detect() -> Self {
        let mut sys = System::new_all();
        sys.refresh_all();

        let total_ram_bytes = sys.total_memory();
        let available_ram_bytes = sys.available_memory();

        DeviceProfile {
            hostname: System::host_name().unwrap_or_else(|| "unknown".to_string()),
            os: System::long_os_version().unwrap_or_else(|| "unknown".to_string()),
            cpu_cores: sys.cpus().len(),
            cpu_brand: sys
                .cpus()
                .first()
                .map(|c| c.brand().to_string())
                .unwrap_or_else(|| "unknown".to_string()),
            total_ram_gb: total_ram_bytes as f64 / 1_073_741_824.0,
            available_ram_gb: available_ram_bytes as f64 / 1_073_741_824.0,
            gpu_info: detect_gpu(),
        }
    }
}

/// Attempt to detect GPU. Placeholder — real detection uses nvml/Metal/Vulkan queries.
fn detect_gpu() -> Option<GpuInfo> {
    // TODO Phase 1: Implement real GPU detection
    // - NVIDIA: use nvml-wrapper crate
    // - Apple Silicon: check for MLX availability
    // - AMD/Intel: check Vulkan support
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_profile_detects_something() {
        let profile = DeviceProfile::detect();
        assert!(profile.cpu_cores > 0);
        assert!(profile.total_ram_gb > 0.0);
    }
}
