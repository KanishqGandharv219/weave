"""Job submission and lifecycle routes."""

from __future__ import annotations

from enum import Enum
from typing import Optional
from uuid import uuid4

import structlog
from fastapi import APIRouter
from pydantic import BaseModel, Field

logger = structlog.get_logger()
router = APIRouter()


# ── Schemas ──────────────────────────────────────────


class JobStatus(str, Enum):
    """Lifecycle states for a compute job."""

    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


class JobSubmission(BaseModel):
    """Request body for submitting a new job."""

    model: str = Field(
        default="meta-llama/Llama-3.1-8B-Instruct",
        description="HuggingFace model ID to run inference against.",
    )
    prompt: str = Field(..., min_length=1, max_length=32_000)
    max_tokens: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class JobResponse(BaseModel):
    """Returned after job submission or status query."""

    job_id: str
    status: JobStatus
    model: str
    result: Optional[str] = None
    credits_charged: float = 0.0
    assigned_node: Optional[str] = None


# ── In-memory store (replaced by Postgres in Phase 1) ──

_jobs: dict[str, JobResponse] = {}


# ── Routes ───────────────────────────────────────────


@router.post("/jobs", status_code=201)
async def submit_job(submission: JobSubmission) -> JobResponse:
    """Submit a new inference job to the network."""
    job_id = str(uuid4())
    job = JobResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        model=submission.model,
    )
    _jobs[job_id] = job
    logger.info(
        "job.submitted",
        job_id=job_id,
        model=submission.model,
        max_tokens=submission.max_tokens,
    )
    return job


@router.get("/jobs/{job_id}")
async def get_job(job_id: str) -> JobResponse:
    """Query job status and result."""
    if job_id not in _jobs:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return _jobs[job_id]


@router.get("/jobs")
async def list_jobs(status: Optional[JobStatus] = None) -> list[JobResponse]:
    """List jobs, optionally filtered by status."""
    jobs = list(_jobs.values())
    if status:
        jobs = [j for j in jobs if j.status == status]
    return jobs
