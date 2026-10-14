# 📐 Architectural Specification: SkillBridge AI Platform (v2.0)
### Academic Lead: Professor Siddhaling Urolagin | Lead Developer: Narendra Gandikota
### Protocol: Autonomous 4-Stage Multi-Role Council | Standard: FAANG Senior Pedagogical Depth

---

## 1. Executive Summary & Root Problem Analysis

### 1.1 The Problem
Traditional student CVs rely on static bullet points and keyword optimization without verifiable code evidence. When students attempt to construct portfolios, existing AI tools either generate vague project ideas without structure or dump 100% completed code, robbing the student of the actual learning process.

### 1.2 Professor Siddhaling Urolagin's Five Directives
1. **Granular 4-Tier Taxonomy & Benchmark Transparency**:
   - Skills must be strictly partitioned into four technical tiers: **Languages**, **Frameworks**, **Databases**, and **Tools & Infrastructure**.
   - The platform must explicitly answer: *"Which baseline are you comparing with?"* Displaying sample sizes, standard names, and empirical distribution requirements.
2. **Eradication of Repetitive Information & AI Slop**:
   - Eliminate duplicated summaries, vague conversational preambles, and filler text across all dashboard views.
   - Deliver high-density data tables, quantifiable metrics, and actionable diagnostic guidance.
3. **Pedagogical Skeleton Architecture First**:
   - Never provide 100% solved solutions.
   - Scaffold production-grade **Skeleton Repositories**: strict typed schemas, method stubs with `# TODO(student)` invariant documentation, pre-written failing TDD test suites, and 4 milestone tracking issues.
4. **Dual-Path Provisioning Engine**:
   - **Path A**: Automated one-click GitHub/GitLab repository provisioning via OAuth/PAT.
   - **Path B**: Zero-OAuth Manual CLI setup with a downloadable skeleton ZIP and copy-paste terminal instructions.
5. **Kaggle API & Data Science Workflows**:
   - Provide native competition workflows for ML/AI and Data Science roles: dataset automation (`download_dataset.sh`), exploratory notebooks (`01_eda_baseline.ipynb`), and CLI submission pipelines.

---

## 2. Granular 4-Tier Taxonomy & Benchmark Transparency Model

### 2.1 The 4-Tier Partition
Every skill analyzed or recommended belongs exclusively to one of four canonical tiers:
1. `languages`: Python, TypeScript, JavaScript, Go, Java, C++, Rust, SQL, R, Bash, Scala, Solidity.
2. `frameworks`: FastAPI, Django, React, Next.js, Node.js, Express, PyTorch, TensorFlow, Scikit-learn, LangChain, LlamaIndex.
3. `databases`: PostgreSQL, Redis, MongoDB, Snowflake, BigQuery, Elasticsearch, Pinecone, ChromaDB, SQLite.
4. `tools_infrastructure`: Docker, Kubernetes, Git, GitHub Actions, GitLab CI, Terraform, AWS, Google Cloud, Linux, Prometheus.

### 2.2 Benchmark Baseline Transparency Matrix
Every evaluation calculates candidate proficiency against an empirical benchmark:
```python
class BenchmarkStandard(BaseModel):
    standard_name: str = Field(..., description="e.g. Mid-Level Backend Engineer Industry Baseline")
    sample_size: str = Field(..., description="e.g. Aggregated from 5,420+ Tier-1 Tech Job Postings")
    tier_distribution: Dict[str, List[str]] = Field(..., description="Required skills per tier")
    tier_weights: Dict[str, float] = Field(
        default={"languages": 0.40, "frameworks": 0.30, "databases": 0.20, "tools_infrastructure": 0.10}
    )
    percentile_threshold: int = Field(default=80, description="Minimum benchmark threshold for hireability")
```

---

## 3. Strict Pydantic v2 Domain Contracts

```python
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, HttpUrl

class TechnicalTier(str, Enum):
    LANGUAGES = "languages"
    FRAMEWORKS = "frameworks"
    DATABASES = "databases"
    TOOLS_INFRASTRUCTURE = "tools_infrastructure"

class SkillVerificationLevel(str, Enum):
    NONE = "None"
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

class ExtractedSkill(BaseModel):
    name: str = Field(..., description="Canonical name of technical competency")
    tier: TechnicalTier = Field(..., description="4-tier technical categorization")
    level: SkillVerificationLevel = Field(default=SkillVerificationLevel.INTERMEDIATE)
    verified: bool = Field(default=True, description="Found in candidate CV text")

class CompetencyGapItem(BaseModel):
    tier: TechnicalTier = Field(..., description="Categorical skill tier")
    skill: str = Field(..., description="Identified missing or deficient technical skill")
    current_proficiency: float = Field(..., ge=0, le=100, description="Candidate score percentage")
    required_benchmark: float = Field(..., ge=0, le=100, description="Industry baseline requirement")
    deficit_delta: float = Field(..., description="Gap percentage delta (required - current)")
    priority: str = Field(..., pattern="^(CRITICAL|HIGH|MEDIUM|LOW)$")
    pedagogical_reasoning: str = Field(..., description="Factual justification for necessity in target role")

class MilestoneSprintIssue(BaseModel):
    issue_number: int = Field(..., ge=1, le=4)
    title: str = Field(..., description="Sprint objective title")
    user_story: str = Field(..., description="Agile engineering user story")
    acceptance_criteria: List[str] = Field(..., description="Actionable testable checklist")
    definition_of_done: str = Field(..., description="Verification condition")

class SkeletonProjectBlueprint(BaseModel):
    id: str = Field(..., description="Unique slug identifier")
    title: str = Field(..., description="Project engineering title")
    difficulty: str = Field(..., description="Foundational | Intermediate | Production Cloud")
    estimated_hours: int = Field(..., ge=10, le=80)
    target_skills_covered: List[str] = Field(..., min_length=1)
    tech_stack: List[str] = Field(..., min_length=2)
    architecture_outline: str = Field(..., description="Architectural design pattern summary")
    is_kaggle_track: bool = Field(default=False, description="Flag indicating ML/Data Science competition workflow")
    roadmap: List[str] = Field(..., min_length=4, max_length=4)
    milestone_issues: List[MilestoneSprintIssue] = Field(..., min_length=4, max_length=4)
    starter_files: Dict[str, str] = Field(..., description="Skeleton files: type contracts, stubs, and failing test harness")
    manual_cli_commands: List[str] = Field(..., description="Sequential terminal commands for zero-OAuth setup")

class SkillBridgeAnalysisResponse(BaseModel):
    candidate_name: str
    target_role: str
    overall_match_percentage: int = Field(..., ge=0, le=100)
    competency_deficit_delta: float = Field(..., description="Euclidean deficit score")
    benchmark_standard: BenchmarkStandard
    tier_distribution: Dict[TechnicalTier, List[ExtractedSkill]]
    competency_gaps: List[CompetencyGapItem]
    blueprints: List[SkeletonProjectBlueprint]
    adjacent_role_benchmarks: List[Dict[str, Any]]
```

---

## 4. Pedagogical Skeleton Architecture Specification

Every generated project must strictly adhere to the **Skeleton-First Principle**:
1. **Strict Type Contracts**: All data structures, API requests, and response envelopes are fully defined using immutable Pydantic models or TypeScript interfaces.
2. **Method Stubs with Invariant Contracts**:
   ```python
   def resolve_topological_dag(tasks: List[TaskNode]) -> List[TaskNode]:
       """
       Topologically sorts task dependencies using Kahn's algorithm.
       
       Invariants:
       - Must detect circular dependencies and raise CyclicDependencyError.
       - Independent tasks must preserve priority ordering.
       """
       # TODO(student): Implement topological sort according to Milestone 2 requirements.
       # Reference: docs/architecture/dag-resolution.md
       raise NotImplementedError("TODO(student): Implement topological sort in Milestone 2")
   ```
3. **Pre-written Failing TDD Test Suite**:
   Running `pytest tests/ -v` on fresh clone must fail with descriptive pedagogical error messages:
   ```text
   FAILED tests/test_dag.py::test_kahn_topological_sort - NotImplementedError: TODO(student): Implement topological sort in Milestone 2
   FAILED tests/test_dag.py::test_cycle_rejection - NotImplementedError: TODO(student): Implement cycle rejection
   ```
4. **Four Sequential Milestone Issues**:
   - **Milestone 1**: Data Schemas, Config & Invariant Contracts
   - **Milestone 2**: Core Domain Algorithms & State Transitions
   - **Milestone 3**: API Boundary Routing, HTTP Contracts & RFC 7807 Errors
   - **Milestone 4**: Container Isolation, TDD Harness Green & CI/CD Pipeline

---

## 5. Dual-Path Repository Provisioning Specification

### 5.1 Path A: Automated Cloud OAuth API
- One-click GitHub/GitLab REST API provisioning.
- Single atomic Git commit containing skeleton files.
- Creates four milestone issues directly on student's repository.

### 5.2 Path B: Zero-OAuth Manual CLI Workflow
- Endpoint: `/api/blueprint/{blueprint_id}/download-zip` (or client-side Zip archive generation).
- Modal CLI Instructions Drawer providing copy-paste script:
  ```bash
  # Step 1: Create local directory and initialize Git
  mkdir {project_slug} && cd {project_slug}
  git init -b main

  # Step 2: Unzip skeleton files into project folder
  # (Extract downloaded {project_slug}-skeleton.zip here)

  # Step 3: Run failing test harness to observe initial Red state
  pytest tests/ -v

  # Step 4: Create remote repository and push code
  gh repo create {project_slug} --public --source=. --remote=origin --push
  ```

---

## 6. Kaggle ML Workflow Specification

When `target_role` is **Data Analyst**, **Data Scientist**, **Machine Learning Engineer**, or **AI Engineer**:
1. Project blueprints include Kaggle competition structure:
   ```text
   ├── data/
   │   └── download_dataset.sh        # Automated Kaggle CLI dataset fetcher
   ├── notebooks/
   │   └── 01_eda_baseline.ipynb      # EDA scaffold with metric calculation stubs
   ├── src/
   │   ├── features.py                # Feature pipeline contract with student stubs
   │   └── train.py                   # Model training scaffold with MLflow/Weights & Biases
   ├── submissions/
   │   └── submit_predictions.sh      # Kaggle CLI submission automation script
   └── tests/
       └── test_feature_pipeline.py   # Failing unit tests for data leakage checks
   ```

---

## 7. High-Density, Non-Repetitive UI Specification

### 7.1 Visual Layout Architecture
1. **Benchmark Context Banner**:
   `Compared with: Tier-1 Tech Mid-Level {Role} Baseline (Aggregated from 5,420+ Industry Job Descriptions)`
2. **4-Tier Granular Capability Grid**:
   Four clean columns: **Languages (40%)**, **Frameworks (30%)**, **Databases (20%)**, **Tools & Infra (10%)** showing verified candidate skills alongside benchmark requirements.
3. **High-Density Gap Diagnostic Matrix**:
   Structured tabular comparison displaying: `Skill | Tier | Current % | Required Benchmark % | Delta % | Action Plan`.
4. **Scoped Project Blueprint Cards**:
   3 to 4 distinct cards (Foundational $\to$ Intermediate $\to$ Cloud Enterprise) with clear toggle for:
   - `[Provision into GitHub]` (Automated)
   - `[Manual Setup & CLI Guide]` (Zero OAuth)
   - `[Download Skeleton ZIP]`

---

## 8. Acceptance Verification Gates

| Check | Requirement | Verification Method |
|---|---|---|
| **Gate 1: 4-Tier Taxonomy** | Zero skills outside the 4 canonical tiers | Unit test in `test_gap_analyzer.py` |
| **Gate 2: Benchmark Source** | Exact benchmark name & sample size rendered | Playwright assertion on live UI |
| **Gate 3: Zero AI Slop** | No conversational filler words in UI or docs | Regex audit via verification script |
| **Gate 4: Skeleton First** | Skeletons contain `TODO(student)` and failing TDD tests | Pytest execution asserting failure |
| **Gate 5: Dual Path Provisioning** | Manual CLI drawer and ZIP download functional | Browser E2E & ZIP stream validation |
| **Gate 6: Kaggle Workflow** | Kaggle tracks scaffold data scripts & notebooks | File structure inspection |
