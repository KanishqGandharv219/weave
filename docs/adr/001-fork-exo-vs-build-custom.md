# ADR-001: Fork exo vs. Build Custom Partitioning Engine

**Status:** Proposed  
**Date:** 2026-06-20  
**Decision Maker:** Kanishq  

## Context

Weave needs a heterogeneous model partitioning engine — the ability to split a large model across devices with different hardware (CPU-only laptops, NVIDIA GPUs, Apple Silicon) and run inference cooperatively.

**exo** (github.com/exo-explore/exo) already solves this for LAN scenarios:
- Dynamic model sharding proportional to device memory/compute
- Multi-backend: MLX (Apple Silicon), tinygrad (NVIDIA/AMD), llama.cpp
- Automatic local network device discovery
- Can run 70B+ models across a cluster
- Active development, production-grade

## Decision

**RECOMMENDED: Fork/extend exo's core partitioning logic.**

Study its source for the partitioning algorithm and multi-backend execution layer. Build Weave's missing pieces (WAN networking, credits, verification, sandboxing) on top or alongside it.

**Do NOT rewrite the partitioning engine from scratch.** This saves an estimated 2-3 months.

## What exo provides (borrow)

- Dynamic layer-to-device assignment based on capabilities
- Multi-runtime execution (MLX, tinygrad, llama.cpp)
- Local peer discovery protocol (replace with libp2p for WAN)
- ChatGPT-compatible API endpoint

## What exo lacks (build)

- **WAN P2P networking** — LAN-only today → libp2p transport
- **Incentive layer** — no credit/payment system → Postgres double-entry ledger
- **Security model** — no untrusted-party sandboxing → WASM/gVisor
- **Verification** — no result integrity checking → TOPLOC integration
- **Fault tolerance** — assumes all devices stay online → re-routing logic

## Risks of Forking

1. **Upstream divergence** — exo is actively developed; maintaining a fork requires periodic rebasing
2. **Python dependency** — exo is Python; daemon is Rust. Options:
   - Run exo as a subprocess managed by the Rust daemon
   - Extract the partitioning algorithm into Rust (higher effort, better integration)
   - Keep exo as the inference engine, Rust daemon as the orchestration wrapper
3. **License compatibility** — exo is GPL-3.0. Must verify compatibility with Weave's intended license.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Build from scratch | Full control, Rust-native | 2-3 month delay, re-inventing solved problems |
| Fork Petals | WAN-ready, DHT built-in | Research-focused, less production-hardened than exo |
| Use distributed-llama | C++, lightweight | Tensor-parallel only (not pipeline), less flexible |

## Next Steps

1. Clone and run exo on 2 machines — validate it works on our specific hardware
2. Read exo source: focus on `partitioning/`, `inference/`, `discovery/`
3. Assess GPL-3.0 implications for Weave's license
4. Decide integration pattern (subprocess vs algorithm extraction vs wrapper)
5. Document findings and finalize this ADR status to "Accepted" or "Rejected"
