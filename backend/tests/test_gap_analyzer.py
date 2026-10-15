import pytest
from gap_analyzer import analyze_gap, ROLE_PROFILES, WEIGHTS

def test_role_profiles_count():
    assert len(ROLE_PROFILES) >= 15
    for role, categories in ROLE_PROFILES.items():
        assert "languages" in categories
        assert "frameworks" in categories
        assert "databases" in categories
        assert "tools" in categories

def test_weighted_score_calculation():
    # Only languages matched: 100% of languages * 0.40 = 40%
    data_analyst_languages = ROLE_PROFILES["Data Analyst"]["languages"]
    result = analyze_gap(data_analyst_languages, "Data Analyst")
    assert result["category_breakdown"]["languages"]["percentage"] == 100
    assert result["category_breakdown"]["frameworks"]["percentage"] == 0
    assert result["category_breakdown"]["databases"]["percentage"] == 0
    assert result["category_breakdown"]["tools"]["percentage"] == 0
    assert result["match_percentage"] == 40
    # Deficit Delta: 60% deficit when 40% matched
    assert result["competency_deficit_delta"] == 60.0
    assert result["euclidean_distance"] > 0.0
    assert "Delta = sum(w_k * max(0, d_k - s_k))" in result["deficit_formula"]

def test_perfect_match_score():
    all_skills = []
    for cat in ROLE_PROFILES["Backend Engineer"].values():
        all_skills.extend(cat)
    result = analyze_gap(all_skills, "Backend Engineer")
    assert result["match_percentage"] == 100
    assert result["competency_deficit_delta"] == 0.0
    assert len(result["missing_skills"]) == 0
    assert result["is_senior_qualified"] is True
    assert result["projects"] == []

def test_blueprints_format_and_counts():
    candidate_skills = ["Python"]
    result = analyze_gap(candidate_skills, "AI Engineer")
    projects = result["projects"]
    assert len(projects) in [3, 4]
    for project in projects:
        assert len(project["title"]) > 5
        assert len(project["roadmap"]) == 4
        assert len(project["tech_stack"]) >= 2
        assert "README.md" in project["starter_files"]
        assert ".gitignore" in project["starter_files"]
        assert "Dockerfile" in project["starter_files"]
        assert "Makefile" in project["starter_files"]
        assert "requirements.txt" in project["starter_files"]
        assert "src/main.py" in project["starter_files"]
        assert len(project["starter_files"]) >= 10

def test_senior_standing_suppresses_forced_projects():
    # Candidate with >= 90% skills for Backend Engineer
    backend_skills = ROLE_PROFILES["Backend Engineer"]
    candidate_skills = (
        backend_skills["languages"] +
        backend_skills["frameworks"] +
        backend_skills["databases"] +
        ["Docker"] # missing only AWS/Git from tools
    )
    result = analyze_gap(candidate_skills, "Backend Engineer")
    assert result["match_percentage"] >= 90
    assert result["is_senior_qualified"] is True
    assert result["projects"] == []  # No beginner starter projects forced
    senior_standing = result["senior_standing"]
    assert senior_standing["readiness_status"] == "Interview Ready (Senior Standing)"
    assert len(senior_standing["interview_defense_topics"]) >= 3
    assert len(senior_standing["portfolio_polish_recommendations"]) >= 3

def test_dynamic_blueprint_cache_instant_retrieval():
    from dynamic_project_engine import synthesize_dynamic_blueprints, blueprint_cache
    role = "Data Analyst"
    missing = ["Snowflake", "dbt"]
    matched = ["Python", "SQL"]

    # First call - cache miss or populated
    bp1 = synthesize_dynamic_blueprints(role, missing, matched)
    assert len(bp1) in [3, 4]

    # Second call - guaranteed cache hit
    bp2 = synthesize_dynamic_blueprints(role, missing, matched)
    assert len(bp2) in [3, 4]
    assert all(p.get("is_cached") for p in bp2)

def test_jev_classifier_filtering():
    from jev_classifier import classify_document
    # 1. Authentic technical resume
    valid_resume = """
    Alice Johnson
    Senior Fullstack Engineer | alice@example.com | github.com/alicej
    WORK EXPERIENCE:
    Lead Software Engineer, TechCorp (2020 - Present)
    - Designed Next.js and FastAPI architecture serving 1M monthly active users.
    - Mentored team of 8 engineers and introduced automated CI pipelines.
    EDUCATION:
    B.S. in Computer Engineering, Stanford University (2016 - 2020)
    SKILLS: TypeScript, React, Next.js, Python, FastAPI, Docker, PostgreSQL
    """
    res1 = classify_document(valid_resume)
    assert res1.is_resume is True
    assert res1.confidence_score >= 0.50

    # 2. Invoice document (must be rejected)
    invoice = """
    INVOICE #INV-89212
    Issue Date: October 15, 2026
    Due Date: Net 30
    Billed To: Acquisitive Enterprises LLC
    Description: Cloud Infrastructure Consulting Services
    Amount Due: $12,500.00
    Please submit payment to our wire account.
    """
    res2 = classify_document(invoice)
    assert res2.is_resume is False
    assert "invoice" in res2.rejection_reason.lower()

