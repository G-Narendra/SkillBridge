import os
import io
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

SAMPLE_PDF_PATH = r"E:\Moving\Desktop\SkillBridge\CV_Narendra_Gandikota_td_data-analyst.pdf"

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert data["roles_available"] >= 465

def test_api_roles_catalog():
    res = client.get("/api/roles")
    assert res.status_code == 200
    roles = res.json()["roles"]
    assert len(roles) >= 465
    role_names = [r["name"] for r in roles]
    assert "Data Analyst" in role_names
    assert "AI Engineer" in role_names
    assert "Backend Engineer" in role_names

def test_api_resume_parse_standard_role():
    if os.path.exists(SAMPLE_PDF_PATH):
        with open(SAMPLE_PDF_PATH, "rb") as f:
            pdf_bytes = f.read()
    else:
        # Fallback to in-memory PDF with text stream
        import pypdf
        writer = pypdf.PdfWriter()
        page = writer.add_blank_page(width=612, height=792)
        buf = io.BytesIO()
        writer.write(buf)
        pdf_bytes = buf.getvalue()

    response = client.post(
        "/api/resume/parse",
        files={"file": ("test_resume.pdf", pdf_bytes, "application/pdf")},
        data={"target_job": "Data Analyst"}
    )
    if os.path.exists(SAMPLE_PDF_PATH):
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["target_role"] == "Data Analyst"
        assert "match_percentage" in data
        assert "category_breakdown" in data
        assert len(data["projects"]) in [2, 3, 4]
    else:
        assert response.status_code in [200, 422]

def test_api_resume_parse_custom_job_description():
    if os.path.exists(SAMPLE_PDF_PATH):
        with open(SAMPLE_PDF_PATH, "rb") as f:
            pdf_bytes = f.read()

        response = client.post(
            "/api/resume/parse",
            files={"file": ("test_resume.pdf", pdf_bytes, "application/pdf")},
            data={
                "target_job": "Rust Core Systems Architect",
                "job_description": "We require Python, SQL, Docker, PostgreSQL, and Linux for data engine."
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["target_role"] == "Rust Core Systems Architect"
        assert "matched_skills" in data
        assert "missing_skills" in data
        assert len(data["projects"]) in [2, 3, 4]

def test_api_validate_token_rejects_fake():
    res = client.post("/api/github/validate-token", json={"token": "demo"})
    # Correctly rejects fake demo tokens with 401 Unauthorized
    assert res.status_code == 401

def test_api_provision_requires_real_token():
    payload = {
        "title": "Data Pipeline Engine",
        "tech_stack": ["Python", "PostgreSQL", "Docker"],
        "roadmap": ["Step 1", "Step 2", "Step 3", "Step 4"],
        "token": "sandbox",
        "provider": "github"
    }
    res = client.post("/api/provision", json=payload)
    # Correctly rejects sandbox tokens with 401 Unauthorized
    assert res.status_code == 401
