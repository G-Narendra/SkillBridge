import pytest
from gap_analyzer import analyze_gap
from role_archetype_engine import classify_role_archetype
from ten_project_catalog import get_projects_for_discipline

def test_ethical_hacker_archetype_classification():
    discipline = classify_role_archetype("Ethical Hacker")
    assert discipline == "security_cyber"
    
    pentest_disc = classify_role_archetype("Senior Penetration Tester")
    assert pentest_disc == "security_cyber"

def test_ethical_hacker_dimensions_and_gap_analysis():
    # Candidate with web skills
    candidate_skills = ["SQL", "Next.js", "Docker", "Git"]
    res = analyze_gap(candidate_skills, "Ethical Hacker", experience_years=1)
    
    benchmark = res.get("benchmark_standard", {})
    assert benchmark.get("archetype_id") == "security_cyber"
    assert "Cybersecurity" in benchmark.get("archetype_name", "")
    
    dim_labels = [d["label"] for d in res.get("dimensions", [])]
    # Verify NO generic web dev dimensions
    assert "Frontend & UI" not in dim_labels
    assert "Databases & Storage" not in dim_labels
    
    # Verify authentic security dimensions
    assert any("Pen-Testing" in lbl or "Security" in lbl for lbl in dim_labels)
    assert any("Cryptography" in lbl or "Protocols" in lbl for lbl in dim_labels)
    assert any("OS Hardening" in lbl or "WAF" in lbl for lbl in dim_labels)
    assert any("Security Scripting" in lbl or "Exploit" in lbl for lbl in dim_labels)
    
    # Missing skills must NOT be React or PostgreSQL
    assert "React" not in res["missing_skills"]
    assert "PostgreSQL" not in res["missing_skills"]
    
    # Must have authentic security projects
    projects = res["projects"]
    assert len(projects) >= 2
    proj_titles = [p["title"] for p in projects]
    # None of the projects should be database migration or stripe billing
    for title in proj_titles:
        assert "Database Migration" not in title
        assert "Stripe Webhooks" not in title
    
    # Projects should be security projects
    has_security_project = any(
        any(term in t.lower() for term in ["scapy", "port", "owasp", "vulnerability", "fuzzer", "waf", "reconnaissance", "honeypot", "vault"])
        for t in proj_titles
    )
    assert has_security_project

def test_security_projects_matrix():
    projects = get_projects_for_discipline("security_cyber")
    assert len(projects) == 10
    difficulties = [p["difficulty"] for p in projects]
    assert difficulties.count("Beginner") == 2
    assert difficulties.count("Intermediate") == 4
    assert difficulties.count("Advanced") == 4
