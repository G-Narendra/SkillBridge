import pytest
from unittest.mock import patch, MagicMock
from github_provisioner import provision_repository, sanitize_repo_name, provision_sandbox_mode

def test_sanitize_repo_name():
    assert sanitize_repo_name("Real-Time PyTorch Inference / API") == "real-time-pytorch-inference-api"
    assert sanitize_repo_name("  Distributed & Kafka Queue!! ") == "distributed-kafka-queue"

def test_provision_sandbox_mode():
    res = provision_sandbox_mode(
        "Data Pipeline Engine",
        ["Python", "PostgreSQL"],
        ["Milestone 1: Setup", "Milestone 2: Schema", "Milestone 3: Endpoints", "Milestone 4: Tests"],
        "github"
    )
    assert res["status"] == "success"
    assert res["is_sandbox"] is True
    assert "github.com" in res["repo_url"]
    assert len(res["issues_created"]) == 4

@patch("github_provisioner.Github")
def test_provision_repository_github_mocked(mock_github):
    mock_g = MagicMock()
    mock_user = MagicMock()
    mock_repo = MagicMock()

    mock_github.return_value = mock_g
    mock_g.get_user.return_value = mock_user
    mock_user.login = "testuser"
    mock_user.create_repo.return_value = mock_repo
    mock_repo.html_url = "https://github.com/testuser/test-project"

    res = provision_repository(
        "Test Project",
        ["Python"],
        ["Milestone 1: Init", "Milestone 2: Develop"],
        {"README.md": "# Test"},
        token="ghp_mock_live_token",
        provider="github"
    )

    assert res["status"] == "success"
    assert res["repo_url"] == "https://github.com/testuser/test-project"
    assert res["is_sandbox"] is False

def test_pandas_blueprint_routing():
    from blueprint_generator import generate_production_blueprint_files
    title = "Production Service Architecture with Pandas"
    stack = ["Pandas", "PostgreSQL", "Docker", "Git"]
    roadmap = [
        "Architect vectorized statistical calculation engine and 5-number summary pipelines with Pandas 2.2",
        "Implement automated data cleansing, schema inference, and categorical memory optimization",
        "Build high-throughput dynamic GroupBy aggregations and parametric outlier detection",
        "Establish containerized FastAPI gateway, Prometheus telemetry, and automated CI test matrix"
    ]
    files = generate_production_blueprint_files(title, stack, roadmap, role="Ai Agents Engineer")
    
    # Verify core pandas domain engine files are present
    assert "src/engine/analytics_core.py" in files
    assert "src/engine/data_cleaner.py" in files
    assert "src/engine/aggregator.py" in files
    assert "src/models/analytics.py" in files
    assert "tests/test_analytics_core.py" in files
    assert "tests/test_data_cleaner.py" in files
    assert "tests/test_api.py" in files
    assert "Dockerfile" in files
    assert "docker-compose.yml" in files
    assert "ci/ci-pipeline.yml" in files
    assert "Makefile" in files
    assert "requirements.txt" in files
    assert "README.md" in files

    # Verify that NO legacy agent files leaked into this pandas project
    assert "src/agent/react.py" not in files
    assert "src/tools/registry.py" not in files
    assert "tests/test_agent.py" not in files

    # Verify requirements.txt pins pandas and numpy
    assert "pandas>=2.2.0" in files["requirements.txt"]
    assert "numpy>=1.26.0" in files["requirements.txt"]
    assert "pyarrow>=15.0.0" in files["requirements.txt"]

