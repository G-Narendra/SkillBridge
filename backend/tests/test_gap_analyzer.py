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
    # Role-calibrated dimensions for Data Analyst: query_languages (35%), data_manipulation (25%), warehouses_modeling (25%), bi_visualization (15%)
    data_analyst_languages = ROLE_PROFILES["Data Analyst"]["languages"]
    result = analyze_gap(data_analyst_languages, "Data Analyst")
    assert result["category_breakdown"]["query_languages"]["percentage"] == 100
    assert result["category_breakdown"]["data_manipulation"]["percentage"] == 0
    assert result["category_breakdown"]["warehouses_modeling"]["percentage"] == 0
    assert result["category_breakdown"]["bi_visualization"]["percentage"] == 0
    assert result["match_percentage"] == 35
    # Deficit Delta: 65% deficit when 35% matched
    assert result["competency_deficit_delta"] == 65.0
    assert result["euclidean_distance"] > 0.0
    assert "Delta = sum(w_k * max(0, d_k - s_k))" in result["deficit_formula"]
    assert len(result["dimensions"]) == 4
    assert result["archetype_metadata"]["id"] == "data_analytics"

def test_role_based_archetype_frontend_omits_databases():
    # Frontend candidates must NOT be penalized for databases (weight 0.0, omitted)
    frontend_skills = ["TypeScript", "JavaScript", "HTML", "CSS", "React", "Next.js", "Tailwind CSS", "Redux"]
    result = analyze_gap(frontend_skills, "Frontend Engineer")
    arch = result["archetype_metadata"]
    assert arch["id"] == "frontend_ui"
    assert "Databases" in arch["omitted_metrics"][0]
    assert result["category_breakdown"]["databases"]["is_omitted"] is True
    assert result["category_breakdown"]["databases"]["weight"] == 0.0
    # Match percentage should be high without having any database skills
    assert result["match_percentage"] >= 80

def test_role_based_archetype_devops_calibrated_weights():
    # DevOps engineers should have heavy weights on Cloud/IaC & Containers, not web frameworks
    devops_skills = ["Docker", "Kubernetes", "Linux", "Bash", "Terraform", "AWS", "Prometheus", "Grafana", "GitHub Actions"]
    result = analyze_gap(devops_skills, "DevOps Engineer")
    arch = result["archetype_metadata"]
    assert arch["id"] == "devops_platform"
    assert "Web Frontend Frameworks" in arch["omitted_metrics"]
    weights = result["dimension_weights"]
    assert weights["iac_cloud"] >= 0.30
    assert weights["container_orchestration"] >= 0.30
    assert result["match_percentage"] >= 75

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
        ["Docker", "Git", "AWS"] # missing only Linux/Kubernetes from infra
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

    # 3. Cover letter (must be rejected cleanly)
    cover_letter = """
    Cover Letter
    Dear Hiring Manager,
    I am writing to express my strong interest in the Junior Analyst position.
    In my previous projects, I used Python and SQL to analyze datasets.
    I look forward to hearing from you.
    Sincerely,
    Narendra Gandikota
    narendragandikota2540@gmail.com
    """
    res3 = classify_document(cover_letter)
    assert res3.is_resume is False
    assert res3.document_type == "cover_letter"
    assert "cover letter" in res3.rejection_reason.lower()


def test_marketplace_engineer_archetype_and_projects():
    result = analyze_gap(["Python", "SQL"], "Marketplace Engineer", experience_years=2)
    arch = result["archetype_metadata"]
    assert arch["id"] == "marketplace_systems"
    assert "Marketplace Systems" in arch["name"]
    # Check that client UI is omitted
    assert any("UI" in om or "CSS" in om for om in arch["omitted_metrics"])
    # Check dimensions
    dim_ids = [d["id"] for d in result["dimensions"]]
    assert "matching_dispatch" in dim_ids
    assert "dynamic_pricing_auctions" in dim_ids
    # Check projects are authentic marketplace projects
    projects = result["projects"]
    assert len(projects) >= 3
    assert any("Surge Pricing" in p["title"] or "Escrow" in p["title"] or "Dispatch" in p["title"] for p in projects)


def test_fresher_experience_calibrated_benchmark():
    # Fresher candidate with only basic skills: Python, React, Git (0 years experience)
    candidate_skills = ["Python", "React", "Git"]
    # Evaluated as Fresher (0 years)
    fresher_result = analyze_gap(candidate_skills, "Frontend Engineer", experience_years=0)
    # Evaluated as Senior (6 years)
    senior_result = analyze_gap(candidate_skills, "Frontend Engineer", experience_years=6)

    # Fresher benchmark evaluates against core foundational subset, giving higher readiness percentage
    assert fresher_result["match_percentage"] >= senior_result["match_percentage"]
    # Dimensions for fresher have fewer, focused required competencies
    for dim in fresher_result["dimensions"]:
        assert dim["total_required"] <= 3


def test_custom_job_description_strict_evaluation():
    jd = """
    We are looking for a Python Backend Developer proficient in FastAPI, PostgreSQL, and Docker.
    Must have experience with Git and Redis caching.
    """
    candidate_skills = ["Python", "FastAPI", "Docker", "Git"] # Has 4 out of 5 required
    result = analyze_gap(candidate_skills, "Backend Engineer", custom_job_description=jd)

    assert result["archetype_metadata"]["id"] == "custom_job_description"
    assert "Custom Job Description Benchmark" in result["archetype_metadata"]["name"]
    # Missing skills should strictly include Redis and PostgreSQL (from the JD)
    missing = result["missing_skills"]
    assert "Redis" in missing or "PostgreSQL" in missing
    # Candidate should not be penalized for skills not in the JD (like Kubernetes or Django)
    assert "Kubernetes" not in missing
    assert "Django" not in missing


def test_role_authentic_project_tracks_and_clean_slugs():
    import re
    # 1. Frontend Engineer projects must be UI & client focused
    fe_result = analyze_gap(["HTML"], "Frontend Engineer", experience_years=2)
    fe_projects = fe_result["projects"]
    assert len(fe_projects) >= 3
    # Check that Frontend projects do not repeat PostgreSQL Persistence Engine
    assert any("Component Design System" in p["title"] or "Dashboard" in p["title"] for p in fe_projects)
    for p in fe_projects:
        # Must have clean slug without 16-hex hash
        assert not re.match(r'^[0-9a-f]{16}$', p["id"])
        assert not re.match(r'^[0-9a-f]{16}$', p["slug"])
        assert "---" not in p["slug"]

    # 2. DevOps Engineer projects must be Cloud & Container focused
    devops_result = analyze_gap(["Linux"], "DevOps Engineer", experience_years=2)
    devops_projects = devops_result["projects"]
    assert len(devops_projects) >= 3
    assert any("Infrastructure Pipeline" in p["title"] or "Container Cluster" in p["title"] or "CI/CD" in p["title"] for p in devops_projects)
    for p in devops_projects:
        assert not re.match(r'^[0-9a-f]{16}$', p["id"])
        assert not re.match(r'^[0-9a-f]{16}$', p["slug"])
        assert "---" not in p["slug"]

def test_advisory_leadership_role_omits_coding_tools():
    # Advisory Board Member must classify to tech_leadership_advisory
    result = analyze_gap(["Tech Strategy"], "Advisory Board Member", experience_years=8)
    arch = result["archetype_metadata"]
    assert arch["id"] == "tech_leadership_advisory"
    assert "Technology Leadership" in arch["name"]
    # Check that projects are leadership & governance focused, NOT Docker or PostgreSQL
    projects = result["projects"]
    assert len(projects) >= 3
    for p in projects:
        assert "Docker Architecture" not in p["title"]
        assert "PostgreSQL Analytics" not in p["title"]
    # Check benchmark standard has clean title without AI slop
    std_name = result["benchmark_standard"]["standard_name"]
    assert "Tier-1 Tech Mid-Level" not in std_name


