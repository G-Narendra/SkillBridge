import os
import io
import pytest
from pypdf import PdfWriter
from cv_parser import (
    extract_skills_from_text,
    extract_candidate_links,
    detect_experience_years,
    extract_text_from_pdf,
    parse_resume
)

def test_extract_skills_categorization():
    text = "Proficient in Python, SQL, FastAPI, PostgreSQL, and Docker."
    res = extract_skills_from_text(text)
    assert "Python" in res["languages"]
    assert "SQL" in res["languages"]
    assert "FastAPI" in res["frameworks"]
    assert "PostgreSQL" in res["databases"]
    assert "Docker" in res["tools"]

def test_extract_skills_aliases():
    text = "Strong proficiency in TS, K8s, Postgres, and React.js."
    res = extract_skills_from_text(text)
    assert "TypeScript" in res["languages"]
    assert "Kubernetes" in res["tools"]
    assert "PostgreSQL" in res["databases"]
    assert "React" in res["frameworks"]

def test_extract_candidate_links():
    text = (
        "Narendra Gandikota | narendra@example.com | "
        "github.com/narendra-dev | linkedin.com/in/narendra-g | portfolio.dev"
    )
    links = extract_candidate_links(text)
    assert links["email"] == "narendra@example.com"
    assert "github.com/narendra-dev" in links["github"]
    assert "linkedin.com/in/narendra-g" in links["linkedin"]
    assert "portfolio.dev" in links["portfolio"]

def test_detect_experience_years():
    text1 = "Senior engineer with 5+ years of experience building distributed systems."
    assert detect_experience_years(text1) == 5

    text2 = "Employed at Tech Corp from 2021 to 2025 as software developer."
    assert detect_experience_years(text2) == 4

    # Fresher student with degree span and internship
    text3 = """
    EDUCATION
    B.Tech Computer Science | 2022 - 2026
    XYZ University, CGPA: 8.5

    EXPERIENCE
    Frontend Intern | June 2024 - Aug 2024
    Startup Inc (3 months internship)

    PROJECTS
    React Dashboard with Tailwind CSS
    """
    assert detect_experience_years(text3) == 0

    # Explicit < 1 year
    text4 = "Passionate junior developer with less than 1 year of experience in Python and SQL."
    assert detect_experience_years(text4) == 0

    # Fresher keyword
    text5 = "Recent college graduate, fresher software engineer seeking entry-level opportunity."
    assert detect_experience_years(text5) == 0

def test_parse_real_pdf_if_available():
    pdf_path = r"E:\Moving\Desktop\SkillBridge\CV_Narendra_Gandikota_td_data-analyst.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            data = parse_resume(f.read())
        assert len(data["skills"]) > 5
        assert data["contacts"]["email"] is not None
        assert data["experience_years"] >= 1
        assert "anonymized_snippet" in data
        assert data["anonymization_audit"]["status"] == "anonymized"

def test_anonymize_resume_pii():
    from cv_parser import anonymize_resume_pii
    raw = "Candidate: Jane Doe, Email: jane.doe@example.com, Phone: +1-555-123-4567, Address: 94103."
    contacts = {"name": "Jane Doe", "email": "jane.doe@example.com", "phone": "+1-555-123-4567"}
    res = anonymize_resume_pii(raw, contacts)
    assert "[REDACTED_EMAIL]" in res["anonymized_text"]
    assert "[REDACTED_PHONE]" in res["anonymized_text"]
    assert "[REDACTED_CANDIDATE_NAME]" in res["anonymized_text"]
    assert "jane.doe@example.com" not in res["anonymized_text"]
    assert res["audit"]["redactions_applied"] >= 3

