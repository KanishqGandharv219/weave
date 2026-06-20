"""Health check routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Liveness probe."""
    return {
        "status": "ok",
        "service": "weave-coordinator",
        "version": "0.1.0",
    }


@router.get("/ready")
async def readiness_check() -> dict:
    """Readiness probe — will check DB + node registry connectivity."""
    # TODO: verify DB pool, node registry health
    return {
        "status": "ok",
        "checks": {
            "database": "not_configured",
            "node_registry": "not_configured",
        },
    }
