"""Coordinator test suite."""

import pytest
from httpx import ASGITransport, AsyncClient

from weave_coordinator.main import app


@pytest.fixture
async def client():
    """Async HTTP test client for the coordinator API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Health endpoint returns ok."""
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "weave-coordinator"


@pytest.mark.asyncio
async def test_submit_job(client: AsyncClient):
    """Submit a job and get back a pending response."""
    resp = await client.post(
        "/api/v1/jobs",
        json={"prompt": "Hello, Weave!", "max_tokens": 64},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "pending"
    assert data["job_id"]
    assert data["model"] == "meta-llama/Llama-3.1-8B-Instruct"


@pytest.mark.asyncio
async def test_get_job(client: AsyncClient):
    """Submit then retrieve a job by ID."""
    submit = await client.post(
        "/api/v1/jobs",
        json={"prompt": "Test prompt"},
    )
    job_id = submit.json()["job_id"]

    resp = await client.get(f"/api/v1/jobs/{job_id}")
    assert resp.status_code == 200
    assert resp.json()["job_id"] == job_id


@pytest.mark.asyncio
async def test_get_nonexistent_job(client: AsyncClient):
    """Requesting unknown job returns 404."""
    resp = await client.get("/api/v1/jobs/nonexistent-id")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_jobs(client: AsyncClient):
    """List all jobs."""
    await client.post("/api/v1/jobs", json={"prompt": "Job 1"})
    await client.post("/api/v1/jobs", json={"prompt": "Job 2"})

    resp = await client.get("/api/v1/jobs")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2
