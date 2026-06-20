"""Weave Coordinator — FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from weave_coordinator.api import health, jobs
from weave_coordinator.config import settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifecycle — startup/shutdown hooks."""
    logger.info("weave_coordinator.starting", version="0.1.0", env=settings.environment)
    # TODO: init DB pool, connect to message bus
    yield
    logger.info("weave_coordinator.shutting_down")
    # TODO: close DB pool, flush telemetry


app = FastAPI(
    title="Weave Coordinator",
    description="Job scheduling, credit accounting, and verification for the Weave compute network.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Route registration ---
app.include_router(health.router, tags=["health"])
app.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
