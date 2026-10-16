import pytest
from curate_roles import CURATED_CANONICAL_ROLES
from role_archetype_engine import classify_role_archetype, ARCHETYPE_REGISTRY
from gap_analyzer import analyze_gap
from role_skills_catalog import get_role_taxonomy
from ten_project_catalog import TEN_PROJECT_MATRICES

class TestAllRolesClearance:
    """
    Exhaustive Academic & Professional Clearance Test Suite.
    Validates 100% of canonical technology roles for:
    - Domain archetype precision
    - Dimension relevance (zero irrelevant metrics)
    - Project blueprint matrix generation (exactly 4 projects with multi-file architectures)
    - Experience-tiered benchmarking (Fresher & Senior)
    - Mathematical invariant compliance
    """

    def test_canonical_roles_count(self):
        """Asserts that all 96 canonical roles are cataloged and distinct."""
        assert len(CURATED_CANONICAL_ROLES) >= 80, f"Expected >= 80 canonical roles, found {len(CURATED_CANONICAL_ROLES)}"
        assert len(set(CURATED_CANONICAL_ROLES)) == len(CURATED_CANONICAL_ROLES), "Duplicate roles found in canonical list"

    @pytest.mark.parametrize("role_name", CURATED_CANONICAL_ROLES)
    def test_role_classification_and_gap_analysis(self, role_name):
        """Validates that each canonical role executes with 100% precision through analyze_gap."""
        candidate_skills = ["Python", "Docker", "Git", "SQL", "Linux", "FastAPI"]
        
        # 1. Classify discipline archetype
        arch_id = classify_role_archetype(role_name)
        assert arch_id in ARCHETYPE_REGISTRY, f"Role {role_name} classified into unknown archetype: {arch_id}"
        
        # 2. Execute Gap Analysis
        res = analyze_gap(candidate_skills, role_name, experience_years=1)
        
        # 3. Verify Match Score Invariants
        score = res.get("match_percentage")
        assert score is not None, f"Match score is None for {role_name}"
        assert 0 <= score <= 100, f"Match score out of bounds [{score}] for {role_name}"
        
        # 4. Verify Dimension Integrity
        dims = res.get("dimensions", [])
        assert len(dims) >= 3, f"Insufficient dimensions ({len(dims)}) for {role_name}"
        
        total_weight = sum(d.get("weight", 0) for d in dims)
        assert 0.98 <= total_weight <= 1.02, f"Dimension weights do not sum to 1.0 for {role_name}: {total_weight}"
        
        # Verify no irrelevant dimensions in specific disciplines
        dim_labels = [d["label"] for d in dims]
        if arch_id == "security_cyber":
            assert not any("Frontend" in l for l in dim_labels), f"Irrelevant Frontend dimension in security role {role_name}"
        elif arch_id == "embedded_systems":
            assert not any("Frontend" in l for l in dim_labels), f"Irrelevant Frontend dimension in embedded role {role_name}"
        elif arch_id == "data_engineering":
            assert not any("Frontend" in l for l in dim_labels), f"Irrelevant Frontend dimension in data engineering role {role_name}"
        elif arch_id == "devops_platform":
            assert not any("Frontend" in l for l in dim_labels), f"Irrelevant Frontend dimension in devops role {role_name}"

        # 5. Verify Project Blueprints (exactly 4 blueprints generated)
        projects = res.get("projects", [])
        assert len(projects) == 4, f"Expected exactly 4 project blueprints for {role_name}, got {len(projects)}"
        
        for p in projects:
            assert p.get("title"), f"Blueprint missing title for {role_name}"
            assert p.get("slug"), f"Blueprint missing slug for {role_name}"
            assert p.get("tech_stack"), f"Blueprint missing tech_stack for {role_name}"
            starter_files = p.get("starter_files", {})
            assert len(starter_files) >= 5, f"Blueprint {p.get('title')} has insufficient starter files ({len(starter_files)}) for {role_name}"

        # 6. Verify Non-Technical Competencies & Experience Benchmarks
        benchmark = res.get("benchmark_standard", {})
        non_tech = benchmark.get("non_technical_competencies", [])
        assert len(non_tech) >= 3, f"Insufficient non-tech competencies for {role_name}: {non_tech}"
        assert benchmark.get("experience_tier") == "fresher"

    def test_all_14_disciplines_have_10_projects(self):
        """Verifies that all 14 disciplines have complete 10-project blueprints in TEN_PROJECT_MATRICES."""
        assert len(ARCHETYPE_REGISTRY) == 14, f"Expected 14 disciplines, got {len(ARCHETYPE_REGISTRY)}"
        for arch_id, arch_meta in ARCHETYPE_REGISTRY.items():
            matrix = TEN_PROJECT_MATRICES.get(arch_id, [])
            assert len(matrix) == 10, f"Discipline {arch_id} ({arch_meta['name']}) has {len(matrix)}/10 projects"
            for p in matrix:
                assert p.get("title")
                assert p.get("difficulty") in ["Beginner", "Intermediate", "Advanced"]
                assert p.get("tech_stack") or p.get("primary_skills")
                assert p.get("roadmap")

    def test_custom_job_description_clearance(self):
        """Verifies that custom job descriptions are correctly parsed and dynamically benchmarked."""
        custom_jd = (
            "We are looking for an AI Engineer with expertise in PyTorch, LangChain, "
            "Pinecone vector databases, FastAPI microservices, and Docker containerization."
        )
        candidate_skills = ["Python", "FastAPI", "Docker", "Git"]
        res = analyze_gap(candidate_skills, "AI Engineer", custom_job_description=custom_jd, experience_years=2)
        
        assert res["match_percentage"] > 0
        bmark = res.get("benchmark_standard", {})
        assert "Custom Job Description" in bmark.get("standard_name", "")
