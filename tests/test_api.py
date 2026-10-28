import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, SessionLocal
from app.seed_data import seed_portfolio_data

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()
    db = SessionLocal()
    seed_portfolio_data(db, force=True)
    db.close()

def test_get_portfolio():
    response = client.get("/api/portfolio")
    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["name"] == "Raj Bharat Rasal"
    assert len(data["projects"]) >= 3
    assert len(data["skills"]) >= 10
    assert len(data["publications"]) >= 2

def test_get_sample_jds():
    response = client.get("/api/sample-jds")
    assert response.status_code == 200
    jds = response.json()
    assert len(jds) >= 2
    assert "Distributed" in jds[0]["title"]

def test_analyze_jd_distributed_systems():
    jd_payload = {
        "job_description": "We are seeking a Distributed Systems Architect experienced in Python, C++, zero-trust protocols, and tensor sharding.",
        "target_title": "Backend & Distributed Systems Architect"
    }
    response = client.post("/api/ai/analyze-jd", json=jd_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["match_score"] > 60
    assert len(data["matched_skills"]) > 0
    assert len(data["suggested_project_ids"]) > 0
    assert "Raj" in data["suggested_summary"] or "Undergraduate" in data["suggested_summary"] or "Systems" in data["suggested_summary"]

def test_analyze_jd_ai_multi_agent():
    jd_payload = {
        "job_description": "Looking for an AI Platform Engineer skilled in multi-agent orchestration, intent classification, FastAPI, and decoupled communication.",
        "target_title": "AI Systems & Multi-Agent Infrastructure Engineer"
    }
    response = client.post("/api/ai/analyze-jd", json=jd_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["match_score"] > 60
    assert len(data["matched_skills"]) > 0

def test_resume_preview():
    preview_payload = {
        "target_title": "Distributed Systems Engineer",
        "job_description": "Distributed computing, Python, C++, tensor sharding",
        "custom_summary": "Test verified summary.",
        "selected_project_ids": [1, 2],
        "selected_skill_ids": [1, 2, 4],
        "selected_experience_ids": [1]
    }
    response = client.post("/api/resume/preview", json=preview_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_title"] == "Distributed Systems Engineer"
    assert len(data["projects"]) == 2
    assert len(data["skills"]) == 3

def test_export_pdf():
    pdf_payload = {
        "target_title": "Backend Systems Architect",
        "selected_project_ids": [1, 2],
        "selected_skill_ids": [1, 2],
        "selected_experience_ids": [1]
    }
    response = client.post("/api/resume/export-pdf", json=pdf_payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000

def test_export_docx():
    docx_payload = {
        "target_title": "Backend Systems Architect",
        "selected_project_ids": [1, 2],
        "selected_skill_ids": [1, 2],
        "selected_experience_ids": [1]
    }
    response = client.post("/api/resume/export-docx", json=docx_payload)
    assert response.status_code == 200
    assert "openxmlformats" in response.headers["content-type"]
    assert len(response.content) > 1000

def test_download_sheets_xlsx():
    response = client.get("/api/sheets/export-xlsx")
    assert response.status_code == 200
    assert "spreadsheetml.sheet" in response.headers["content-type"]
    assert len(response.content) > 1000

def test_unstructured_parse():
    parse_payload = {
        "raw_text": "Alex Morgan, alex@example.com, +1 555-0199. Skills: Python, FastAPI, Redis, Distributed Systems."
    }
    response = client.post("/api/ai/parse-unstructured", json=parse_payload)
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data
    assert "skills" in data

def test_skill_crud():
    # Create
    new_skill = {
        "name": "Rust Systems Programming",
        "category": "Languages",
        "proficiency": "Intermediate",
        "is_highlighted": False
    }
    res_create = client.post("/api/skills", json=new_skill)
    assert res_create.status_code == 200
    created_id = res_create.json()["id"]

    # Update
    res_update = client.put(f"/api/skills/{created_id}", json={
        "name": "Rust (Async)",
        "category": "Languages",
        "proficiency": "Advanced",
        "is_highlighted": True
    })
    assert res_update.status_code == 200
    assert res_update.json()["name"] == "Rust (Async)"

    # Delete
    res_delete = client.delete(f"/api/skills/{created_id}")
    assert res_delete.status_code == 200

