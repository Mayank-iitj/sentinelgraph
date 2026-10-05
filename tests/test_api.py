import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "graph_connected" in data
    assert "llm_mode" in data

def test_tenants():
    response = client.get("/tenants")
    assert response.status_code == 200
    data = response.json()
    assert "tenants" in data
    assert len(data["tenants"]) >= 1

def test_triage_endpoint():
    response = client.post("/triage", json=[
        {"id": "finding_1", "risk_score": 8.0}
    ])
    assert response.status_code == 200
    data = response.json()
    assert "verdicts" in data
    assert len(data["verdicts"]) == 1

def test_brain_ask_endpoint():
    response = client.post("/brain/ask", json={"query": "planted_entry_svc_0"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0

def test_benchmarks_endpoint():
    response = client.get("/benchmarks")
    assert response.status_code == 200

def test_graph_endpoint():
    response = client.get("/graph")
    assert response.status_code == 200
    data = response.json()
    assert "elements" in data

def test_pipeline_endpoint():
    response = client.post("/pipeline/run")
    assert response.status_code == 200
    data = response.json()
    assert "verdicts" in data
    assert "investigations" in data
    assert "remediations" in data
    assert "memory" in data

def test_stream_endpoint():
    response = client.get("/agents/tasks/stream")
    assert response.status_code == 200
