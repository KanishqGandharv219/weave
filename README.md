# Weave

**Peer-to-peer compute network** — idle consumer devices contribute spare compute to run AI inference jobs, earning credits spendable on compute themselves.

> BitTorrent's reciprocity model, applied to compute instead of files.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Developer Surface                   │
│         REST API (FastAPI) · Python SDK · Dashboard  │
├─────────────────────────────────────────────────────┤
│               Coordination Layer                     │
│    Job Queue · Scheduler · Credit Ledger · TOPLOC    │
├─────────────────────────────────────────────────────┤
│                  P2P Layer                           │
│   libp2p Transport · DHT Discovery · NAT Traversal  │
├─────────────────────────────────────────────────────┤
│              Consumer Devices                        │
│   Rust Daemon · llama.cpp/MLX/tinygrad · Sandbox    │
└─────────────────────────────────────────────────────┘
```

## Project Structure

```
weave/
├── coordinator/      # FastAPI coordinator service
├── daemon/           # Rust device client
├── sdk/python/       # Python SDK
├── proto/            # Protobuf definitions
├── dashboard/        # Web UI
├── docs/adr/         # Architecture Decision Records
├── scripts/          # Tooling & benchmarks
└── docker-compose.yml
```

## Design Constraints

1. **No cryptocurrency** — credits are internal ledger entries, not tokens
2. **AI inference first** — prove the model before generalizing
3. **Consumer product + API** — device client people install, not just a dev API
4. **Desktop/laptop only at launch** — no mobile promises until core is proven

## Quick Start

```bash
# Coordinator (Python)
cd coordinator
pip install -e ".[dev]"
uvicorn weave_coordinator.main:app --reload

# Daemon (Rust)
cd daemon
cargo build
cargo run

# Full dev stack
docker-compose up
```

## Status

**Phase 0** — Foundation & Validation (Week 1-2)

## License

TBD
