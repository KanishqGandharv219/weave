"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Basic liveness probe."""
    return {
        "status": "ok",
        "service": "weave-coordinator",
        "version": "0.1.0",
    }


@router.get("/ready")
async def readiness_check() -> dict:
    """Readiness probe — checks DB connectivity, etc."""
    # TODO: check DB pool, check node registry
    return {
        "status": "ok",
        "checks": {
            "database": "not_configured",
            "node_registry": "not_configured",
        },
    }
