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
