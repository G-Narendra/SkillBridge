import pytest
from telemetry_service import (
    compute_ast_modularity_from_files,
    process_github_webhook,
    synthesize_portfolio_card,
    PortfolioCard
)

def test_compute_ast_modularity():
    files_mock = {
        "src/main.py": "app = FastAPI()",
        "src/models/item.py": "class Item(BaseModel): pass",
        "src/engine/core.py": "def run(): pass",
        "tests/test_core.py": "def test_run(): pass",
        "ci/ci-pipeline.yml": "name: CI"
    }
    metrics = compute_ast_modularity_from_files(files_mock)
    assert metrics.modularity_score >= 90.0
    assert metrics.layer_separation_grade == "A+"
    assert metrics.cyclomatic_density > 0

def test_process_github_webhook_push():
    payload = {
        "repository": {"name": "test-repo", "owner": {"login": "testuser"}},
        "commits": [{"id": "c1", "message": "feat: init"}],
        "after": "c1"
    }
    res = process_github_webhook("push", payload)
    assert res["status"] == "processed"
    assert res["repository"] == "testuser/test-repo"

def test_synthesize_portfolio_card():
    card = synthesize_portfolio_card(
        username="G-Narendra",
        target_role="Ai Agents Engineer",
        match_percentage=80.0,
        competency_deficit_delta=20.0,
        verified_skills_count=5
    )
    assert isinstance(card, PortfolioCard)
    assert card.candidate_username == "G-Narendra"
    assert card.compatibility_score == 80.0
    assert card.competency_deficit_delta == 20.0
    assert card.ast_modularity_grade == "A+"
    assert card.overall_test_pass_rate == 100.0
    assert len(card.repositories) >= 2
    assert "Candidate G-Narendra" in card.executive_summary_15s
    assert len(card.verification_hash) > 0
