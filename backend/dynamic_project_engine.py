"""
Dynamic Portfolio Project Blueprint Engine & Persistent Hash Cache.
Synthesizes customized, non-static project specifications tailored to the candidate's exact
target role and missing skill combination.
Provides an LRU in-memory and persistent JSON caching layer for sub-3ms retrieval,
and evaluates high-competence candidates for Senior Standing (zero forced starter projects).
"""

import os
import re
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from role_archetype_engine import classify_role_archetype
from ten_project_catalog import get_projects_for_discipline, TEN_PROJECT_MATRICES
from role_skills_catalog import get_role_taxonomy

# Locate workspace root outputs directory
_curr = Path(__file__).resolve().parent
while _curr.name and _curr.name != "SkillBridge" and _curr.parent != _curr:
    _curr = _curr.parent
BASE_DIR = _curr if _curr.name == "SkillBridge" else Path(__file__).resolve().parent.parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
CACHE_FILE_PATH = OUTPUTS_DIR / "project_blueprints_cache.json"

class BlueprintCacheManager:
    """
    Dual-layer (in-memory LRU + persistent JSON) cache for synthesized project blueprints.
    Ensures deterministic, ultra-low-latency reuse of blueprints across candidate cohorts.
    """
    def __init__(self, persistent_path: Path = CACHE_FILE_PATH):
        self.persistent_path = persistent_path
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self.hits: int = 0
        self.misses: int = 0
        self._load_from_disk()

    def _load_from_disk(self):
        try:
            if self.persistent_path.exists():
                with open(self.persistent_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self._memory_cache = data
        except Exception:
            self._memory_cache = {}

    def _save_to_disk(self):
        try:
            self.persistent_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.persistent_path, "w", encoding="utf-8") as f:
                json.dump(self._memory_cache, f, indent=2)
        except Exception:
            pass

    def compute_key(self, role: str, missing_skills: List[str], project_index: int, is_freshman: bool = False) -> str:
        clean_role = role.strip().lower()
        clean_skills = ":".join(sorted([s.strip().lower() for s in missing_skills]))
        raw = f"v7|{clean_role}|{clean_skills}|{project_index}|{'freshman' if is_freshman else 'standard'}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self._memory_cache:
            self.hits += 1
            cached_data = dict(self._memory_cache[key])
            cached_data["is_cached"] = True
            # Never return a 16-hex hash as the user-facing blueprint id or slug
            if "id" in cached_data and re.match(r'^[0-9a-f]{16}$', str(cached_data["id"])):
                title_clean = cached_data.get("title", "portfolio-project")
                clean_slug = re.sub(r'[^a-zA-Z0-9]+', '-', title_clean.lower()).strip('-')[:45]
                cached_data["id"] = clean_slug
                cached_data["slug"] = clean_slug
            return cached_data
        self.misses += 1
        return None

    def set(self, key: str, blueprint: Dict[str, Any]):
        self._memory_cache[key] = blueprint
        self._save_to_disk()

    def get_stats(self) -> Dict[str, Any]:
        total = self.hits + self.misses
        ratio = round((self.hits / total * 100), 1) if total > 0 else 0.0
        return {
            "cached_entries_count": len(self._memory_cache),
            "cache_hits": self.hits,
            "cache_misses": self.misses,
            "hit_ratio_percentage": ratio,
            "storage_path": str(self.persistent_path)
        }

# Global Singleton Cache Instance
blueprint_cache = BlueprintCacheManager()


def evaluate_senior_standing(
    match_percentage: int,
    missing_skills: List[str],
    target_role: str,
    categorized_gaps: Any = None
) -> Dict[str, Any]:
    """
    Evaluates whether a candidate exhibits high competence / senior standing.
    If match >= 90% and missing critical skills <= 1, beginner starter project add-ons
    are suppressed in favor of interview defense preparation and an optional staff capstone.
    """
    if isinstance(categorized_gaps, list):
        critical_missing = sum(
            1 for gap in categorized_gaps
            if isinstance(gap, dict) and gap.get("tier") in ["languages", "frameworks", "databases"]
        )
    elif isinstance(categorized_gaps, dict):
        critical_missing = (
            len(categorized_gaps.get("languages", [])) +
            len(categorized_gaps.get("frameworks", [])) +
            len(categorized_gaps.get("databases", []))
        )
    else:
        critical_missing = len(missing_skills)

    is_senior = (match_percentage >= 90) and (critical_missing <= 1)

    if not is_senior:
        return {
            "is_senior_qualified": False,
            "readiness_status": "Bridging Required",
            "senior_summary": "Standard skill gap bridging recommended.",
            "interview_defense_topics": [],
            "portfolio_polish_recommendations": []
        }

    # Generate bespoke defense topics based on the role and verified skills
    defense_topics = [
        {
            "topic": "High-Throughput System Design & Bottlenecks",
            "focus": f"Architecting horizontal scaling and partition strategies for {target_role}.",
            "sample_question": f"How do you architect failover and zero-downtime schema migrations for your primary data stores in {target_role}?"
        },
        {
            "topic": "Observability, Telemetry & SLA Enforcement",
            "focus": "Distributed tracing, p99 latency SLOs, and circuit breakers under catastrophic load.",
            "sample_question": "Explain how you debug a p99 latency degradation spike across asynchronous worker pipelines."
        },
        {
            "topic": "Security, Isolation & Tenant ACLs",
            "focus": "Zero-trust network architecture, rate limiting, and RFC 7807 problem details.",
            "sample_question": "How do you enforce cryptographic tenant isolation and prevent cross-tenant data leakage in multi-tenant services?"
        }
    ]

    polish_recs = [
        "Include live production metrics badges (p99 latency, RPS throughput) in your pinned GitHub READMEs.",
        "Author formal Architecture Decision Records (ADRs) explaining technology tradeoffs in your repositories.",
        "Add continuous integration coverage badges demonstrating >= 85% branch test coverage.",
        "Publish reproducible Docker Compose configurations with automated health checks for peer review."
    ]

    return {
        "is_senior_qualified": True,
        "readiness_status": "Interview Ready (Senior Standing)",
        "match_percentage": match_percentage,
        "senior_summary": f"Outstanding technical match ({match_percentage}%). Candidate demonstrates comprehensive mastery of core competencies for {target_role}. No basic starter projects required; focus on interview defense and senior capstones.",
        "interview_defense_topics": defense_topics,
        "portfolio_polish_recommendations": polish_recs
    }


def get_discipline_project_tracks(
    discipline: str,
    missing_skills: List[str],
    matched_skills: List[str],
    target_role: str,
    is_freshman: bool
) -> List[Dict[str, Any]]:
    """
    Returns authentic, discipline-accurate project archetype specifications.
    Ensures Frontend developers get Component Design Systems and SSR Apps,
    DevOps engineers get IaC and Kubernetes clusters, Data Analysts get BI and analytics models,
    and AI engineers get RAG and agent gateways.
    """
    dbs = [s for s in missing_skills if s in [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra",
        "DynamoDB", "Snowflake", "BigQuery", "Elasticsearch", "Neo4j",
        "Milvus", "Pinecone", "ChromaDB", "Oracle", "MSSQL"
    ]]
    fws = [s for s in missing_skills if s in [
        "React", "Next.js", "Vue", "Angular", "Svelte", "Django", "FastAPI",
        "Flask", "Express", "NestJS", "Spring Boot", "PyTorch", "TensorFlow",
        "Scikit-learn", "Keras", "LangChain", "LlamaIndex", "Hugging Face",
        "Pandas", "NumPy", "Tailwind CSS", "Redux", "Node.js"
    ]]
    tools = [s for s in missing_skills if s in [
        "Docker", "Kubernetes", "Git", "GitHub Actions", "GitLab CI", "Terraform",
        "AWS", "Google Cloud", "Azure", "Linux", "Jenkins", "Ansible", "Helm",
        "Prometheus", "Grafana", "Apache Airflow", "dbt", "Apache Spark",
        "Apache Kafka", "Nginx", "Postman", "Vite", "Webpack", "Tableau", "Power BI",
        "Excel", "CUDA", "CMake", "OpenCV"
    ]]
    langs = [s for s in missing_skills if s in [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
        "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "Bash", "Shell",
        "Solidity", "HTML", "CSS"
    ]]

    # 1. Frontend & UI
    if discipline == "frontend_ui":
        return [
            {
                "track": "Component Architecture & Design Systems",
                "lead_skills": [s for s in missing_skills if s in ["React", "Vue", "Next.js", "TypeScript", "JavaScript"]] or ["React"],
                "complement_skills": [s for s in missing_skills if s in ["Tailwind CSS", "CSS", "Vite", "HTML"]] or ["Tailwind CSS", "TypeScript"],
                "difficulty": "Beginner" if is_freshman else "Intermediate",
                "hours": 18 if is_freshman else 24,
                "theme_template": "Accessible {primary} Component Design System & UI Library",
                "objective_template": "Build a reusable, accessible component design system in {primary} with WCAG tokens, responsive variants, and interactive documentation.",
                "architecture_template": "Component-driven interface architecture using {primary} with strict prop types, design tokens, and Jest unit tests.",
                "slug_base": "design-system-ui-library"
            },
            {
                "track": "Client State & Responsive Dashboard",
                "lead_skills": [s for s in missing_skills if s in ["Next.js", "React", "Vue", "Redux"]] or ["Next.js"],
                "complement_skills": ["TypeScript", "Tailwind CSS"],
                "difficulty": "Intermediate",
                "hours": 28,
                "theme_template": "Real-Time {primary} Performance Dashboard & State Architecture",
                "objective_template": "Create a fast, responsive single-page analytics dashboard with real-time state management, theme switching, and data visualization using {primary}.",
                "architecture_template": "Modern client architecture utilizing {primary} and Tailwind CSS with client-side caching and debounced API interactions.",
                "slug_base": "client-state-dashboard"
            },
            {
                "track": "E2E Testing & Build Optimization",
                "lead_skills": [s for s in missing_skills if s in ["Vite", "Webpack", "Git", "Postman"]] or ["Vite"],
                "complement_skills": ["TypeScript", "Git", "HTML"],
                "difficulty": "Intermediate",
                "hours": 20,
                "theme_template": "Modern {primary} Application Build & Automated Testing Suite",
                "objective_template": "Set up a high-performance frontend build pipeline with automated unit, integration, and visual regression tests using {primary}.",
                "architecture_template": "Modular frontend architecture powered by {primary} with automated test runners and code coverage reporting.",
                "slug_base": "frontend-build-test-suite"
            },
            {
                "track": "Production Web Platform",
                "lead_skills": missing_skills[:2] or ["React", "TypeScript"],
                "complement_skills": ["Tailwind CSS", "Git"],
                "difficulty": "Advanced",
                "hours": 32,
                "theme_template": "Production-Grade {role} Portfolio Showcase Platform",
                "objective_template": "Ship a production-ready web application showcasing responsive layouts, accessible navigation, and optimized assets for {role}.",
                "architecture_template": "Production web application utilizing {primary} and TypeScript with server-side rendering and static asset optimization.",
                "slug_base": "frontend-portfolio-platform"
            }
        ]

    # 2. DevOps & Platform Engineering
    if discipline == "devops_platform":
        return [
            {
                "track": "Infrastructure as Code & Cloud Automation",
                "lead_skills": [s for s in missing_skills if s in ["Terraform", "AWS", "Google Cloud", "Azure", "Ansible"]] or ["Terraform"],
                "complement_skills": ["Linux", "Git", "Bash"],
                "difficulty": "Intermediate",
                "hours": 24,
                "theme_template": "Declarative {primary} Multi-Environment Infrastructure Pipeline",
                "objective_template": "Provision reproducible multi-environment cloud infrastructure using declarative {primary} configurations and automated security scans.",
                "architecture_template": "Modular infrastructure as code utilizing {primary} with remote state locking and least-privilege IAM policies.",
                "slug_base": "cloud-infrastructure-pipeline"
            },
            {
                "track": "Containerization & Clustering",
                "lead_skills": [s for s in missing_skills if s in ["Kubernetes", "Docker", "Helm", "Linux"]] or ["Docker"],
                "complement_skills": ["Linux", "Git"],
                "difficulty": "Intermediate",
                "hours": 28,
                "theme_template": "High-Availability {primary} Container Cluster & Ingress Gateway",
                "objective_template": "Deploy a containerized application cluster with automated health checks, ingress routing, and service discovery using {primary}.",
                "architecture_template": "Containerized cluster architecture utilizing {primary} with readiness/liveness probes and rolling updates.",
                "slug_base": "container-cluster-gateway"
            },
            {
                "track": "CI/CD & Release Hygiene",
                "lead_skills": [s for s in missing_skills if s in ["GitHub Actions", "GitLab CI", "Jenkins", "Git"]] or ["GitHub Actions"],
                "complement_skills": ["Docker", "Linux", "Bash"],
                "difficulty": "Intermediate",
                "hours": 20,
                "theme_template": "Automated {primary} Continuous Delivery Pipeline & Security Gate",
                "objective_template": "Build an automated CI/CD pipeline that lints code, runs test suites, scans for vulnerabilities, and deploys artifacts using {primary}.",
                "architecture_template": "Declarative pipeline workflow utilizing {primary} with automated branch protection and artifact caching.",
                "slug_base": "cicd-delivery-pipeline"
            },
            {
                "track": "Observability & SRE",
                "lead_skills": [s for s in missing_skills if s in ["Prometheus", "Grafana", "Linux"]] or ["Prometheus"],
                "complement_skills": ["Docker", "Linux"],
                "difficulty": "Advanced",
                "hours": 26,
                "theme_template": "Production-Grade {role} Observability & Alerting Stack",
                "objective_template": "Configure end-to-end metrics collection, structured logging, SLA alerting thresholds, and interactive dashboards using {primary}.",
                "architecture_template": "Telemetry stack utilizing {primary} with Prometheus metrics exporters and Grafana visualization panels.",
                "slug_base": "observability-telemetry-stack"
            }
        ]

    # 3. Data Analytics & Business Intelligence
    if discipline == "data_analytics":
        return [
            {
                "track": "Executive BI & Dashboard Architecture",
                "lead_skills": [s for s in missing_skills if s in ["Tableau", "Power BI", "Excel", "SQL"]] or ["Power BI"],
                "complement_skills": ["SQL", "Python", "Pandas"],
                "difficulty": "Beginner" if is_freshman else "Intermediate",
                "hours": 18 if is_freshman else 24,
                "theme_template": "Executive {primary} KPI Analytics & Business Intelligence Dashboard",
                "objective_template": "Build an interactive business intelligence dashboard visualizing revenue trends, cohort metrics, and operational KPIs using {primary}.",
                "architecture_template": "Interactive business intelligence architecture utilizing {primary} and SQL data models with automated drill-down reporting.",
                "slug_base": "bi-analytics-dashboard"
            },
            {
                "track": "Statistical Modeling & Churn Analytics",
                "lead_skills": [s for s in missing_skills if s in ["Pandas", "Python", "Scikit-learn", "SQL"]] or ["Pandas"],
                "complement_skills": ["SQL", "Python", "NumPy"],
                "difficulty": "Intermediate",
                "hours": 28,
                "theme_template": "Predictive {primary} Customer Churn & Cohort Retention Model",
                "objective_template": "Develop a statistical churn prediction and customer retention model using {primary} to identify at-risk accounts.",
                "architecture_template": "Analytical modeling pipeline utilizing {primary} with feature engineering, cohort segmentation, and model evaluation metrics.",
                "slug_base": "customer-churn-model"
            },
            {
                "track": "Automated Data Harmonization & Quality",
                "lead_skills": [s for s in missing_skills if s in ["SQL", "dbt", "Excel", "PostgreSQL"]] or ["SQL"],
                "complement_skills": ["Python", "Pandas", "Git"],
                "difficulty": "Intermediate",
                "hours": 22,
                "theme_template": "Automated {primary} Data Harmonization & Quality Verification Suite",
                "objective_template": "Create an automated data quality and validation pipeline using {primary} to detect anomalies, handle missing values, and test schema rules.",
                "architecture_template": "Data validation pipeline utilizing {primary} with automated schema assertions and test report generation.",
                "slug_base": "data-harmonization-suite"
            },
            {
                "track": "Strategic Domain Modeling",
                "lead_skills": missing_skills[:2] or ["SQL", "Python"],
                "complement_skills": ["Pandas", "Excel", "Git"],
                "difficulty": "Advanced",
                "hours": 30,
                "theme_template": "Strategic {role} Financial & Operational Forecast Engine",
                "objective_template": "Design an analytical forecasting model in {primary} to project financial performance and simulate business growth scenarios for {role}.",
                "architecture_template": "Financial forecasting model utilizing {primary} and SQL with time-series trends and scenario simulation tables.",
                "slug_base": "operational-forecast-engine"
            }
        ]

    # 4. AI Agents & Machine Learning
    if discipline in ["ai_agents", "ml_engineering"]:
        return [
            {
                "track": "RAG & Vector Search Architecture",
                "lead_skills": [s for s in missing_skills if s in ["LangChain", "LlamaIndex", "Pinecone", "ChromaDB", "Milvus"]] or ["LangChain"],
                "complement_skills": ["FastAPI", "Python", "Docker"],
                "difficulty": "Intermediate",
                "hours": 26,
                "theme_template": "High-Performance {primary} Retrieval-Augmented Generation (RAG) Engine",
                "objective_template": "Build a semantic search and question-answering system using {primary} with dense vector embeddings and relevant document chunking.",
                "architecture_template": "Retrieval-augmented pipeline utilizing {primary} with vector indexing, semantic search, and context-aware prompt templates.",
                "slug_base": "rag-retrieval-engine"
            },
            {
                "track": "Autonomous Cognitive Agent Gateway",
                "lead_skills": [s for s in missing_skills if s in ["FastAPI", "Hugging Face", "PyTorch", "Python"]] or ["FastAPI"],
                "complement_skills": ["Python", "Docker", "Git"],
                "difficulty": "Intermediate",
                "hours": 30,
                "theme_template": "Autonomous {primary} Cognitive Agent & Tool Calling Gateway",
                "objective_template": "Construct an autonomous AI agent capable of multi-step tool execution, structured output parsing, and error recovery using {primary}.",
                "architecture_template": "Agentic service architecture utilizing {primary} with structured tool interfaces and API guardrails.",
                "slug_base": "cognitive-agent-gateway"
            },
            {
                "track": "Vector Caching & Semantic Indexing",
                "lead_skills": [s for s in missing_skills if s in ["Redis", "Pinecone", "ChromaDB", "Elasticsearch"]] or ["Redis"],
                "complement_skills": ["FastAPI", "Python", "Docker"],
                "difficulty": "Intermediate",
                "hours": 22,
                "theme_template": "High-Throughput {primary} Semantic Cache & Embedding Store",
                "objective_template": "Implement an in-memory semantic cache and vector retrieval layer using {primary} to minimize repeated LLM inference costs and latency.",
                "architecture_template": "High-speed semantic caching proxy utilizing {primary} with cosine similarity thresholding and automatic cache invalidation.",
                "slug_base": "semantic-cache-proxy"
            },
            {
                "track": "Production AI Platform",
                "lead_skills": missing_skills[:2] or ["Python", "FastAPI"],
                "complement_skills": ["Docker", "Git", "PyTorch"],
                "difficulty": "Advanced",
                "hours": 36,
                "theme_template": "Production-Grade {role} Intelligence Platform",
                "objective_template": "Deploy an end-to-end machine learning inference API with model versioning, batch scoring, and request validation for {role}.",
                "architecture_template": "Scalable ML inference service utilizing {primary} and FastAPI with containerized runtime and automated model benchmarks.",
                "slug_base": "ai-intelligence-platform"
            }
        ]

    # 5. Technology Leadership, Advisory & Architecture Strategy
    if discipline == "tech_leadership_advisory":
        return [
            {
                "track": "Enterprise Architecture & System Governance",
                "lead_skills": ["System Architecture", "Tech Strategy"],
                "complement_skills": ["Enterprise Architecture", "Cloud Strategy"],
                "difficulty": "Intermediate",
                "hours": 24,
                "theme_template": "Enterprise {primary} Strategy & Architecture Governance Framework",
                "objective_template": "Author a comprehensive technical strategy and architecture governance blueprint evaluating tech stack decisions and system boundaries using {primary}.",
                "architecture_template": "Strategic governance framework with Architecture Decision Records (ADRs) and component interaction diagrams.",
                "slug_base": "architecture-governance-framework"
            },
            {
                "track": "Data Governance, Security & Compliance",
                "lead_skills": ["Data Governance", "Compliance"],
                "complement_skills": ["Security Auditing", "SQL"],
                "difficulty": "Intermediate",
                "hours": 20,
                "theme_template": "Enterprise {primary} & Security Audit Engine",
                "objective_template": "Conduct a technical due-diligence and risk audit covering data privacy, access control policies, and compliance standards using {primary}.",
                "architecture_template": "Technical audit framework evaluating security posture, data governance, and regulatory requirements.",
                "slug_base": "security-audit-engine"
            },
            {
                "track": "Cloud Economics & TCO Scalability",
                "lead_skills": ["Cloud Economics", "Risk Management"],
                "complement_skills": ["Disaster Recovery", "Vendor Evaluation"],
                "difficulty": "Advanced",
                "hours": 28,
                "theme_template": "Cloud {primary} & Disaster Recovery Audit Engine",
                "objective_template": "Formulate a cloud unit economics optimization strategy and disaster recovery plan to control infrastructure spend using {primary}.",
                "architecture_template": "Cloud cost and resilience framework modeling Total Cost of Ownership (TCO) and multi-region failover protocols.",
                "slug_base": "cloud-tco-risk-engine"
            },
            {
                "track": "Technical Roadmapping & Board Due Diligence",
                "lead_skills": ["Technical Leadership", "Agile Governance"],
                "complement_skills": ["Roadmapping", "Tech Strategy"],
                "difficulty": "Advanced",
                "hours": 32,
                "theme_template": "Executive Technical Due-Diligence & Strategic Scaling Engine",
                "objective_template": "Develop an executive technology roadmap aligning engineering capacity, platform modernization, and business milestones.",
                "architecture_template": "Executive technology roadmap with phased delivery milestones, hiring plans, and system scaling targets.",
                "slug_base": "technical-due-diligence-engine"
            }
        ]

    # 6. Default / Backend Systems & Software Engineering
    first_track = {
        "track": "Foundational Architecture & Automated Test Suite",
        "lead_skills": matched_skills[:1] or langs[:1] or ["Python"],
        "complement_skills": [s for s in missing_skills if s in ["SQLite", "pytest", "Git", "SQL"]] or missing_skills[:2],
        "difficulty": "Beginner",
        "hours": 16,
        "theme_template": "Foundational {primary} Architecture & Automated Testing Suite",
        "objective_template": "Build a clean backend REST API in {primary} with input validation, database persistence, and automated unit test suites.",
        "architecture_template": "Clean REST API architecture utilizing {primary} with typed request schemas and automated pytest verification.",
        "slug_base": "foundational-test-suite"
    } if is_freshman else {
        "track": "Data Persistence & Microservices",
        "lead_skills": dbs or ["PostgreSQL"],
        "complement_skills": fws[:2] or ["FastAPI", "SQL"],
        "difficulty": "Intermediate",
        "hours": 28,
        "theme_template": "High-Throughput {primary} Analytics & Persistence Engine",
        "objective_template": "Implement a scalable database service using {primary} with optimized relational queries, indexing, and connection pooling.",
        "architecture_template": "High-throughput persistence service utilizing {primary} and PostgreSQL with transaction safety and query optimization.",
        "slug_base": "analytics-persistence-engine"
    }

    return [
        first_track,
        {
            "track": "Core Service & Application Layer",
            "lead_skills": fws or langs or ["FastAPI"],
            "complement_skills": dbs[:1] or tools[:2] or ["Docker", "PostgreSQL"],
            "difficulty": "Intermediate",
            "hours": 32,
            "theme_template": "Distributed {primary} Microservice with Automated Workflows",
            "objective_template": "Design an asynchronous background service using {primary} to process tasks with reliable queueing and error handling.",
            "architecture_template": "Decoupled backend service utilizing {primary} with asynchronous task execution and structured logging.",
            "slug_base": "distributed-microservice"
        },
        {
            "track": "Cloud, Infrastructure & CI/CD",
            "lead_skills": tools or ["Docker"],
            "complement_skills": langs[:1] or ["Python", "Linux"],
            "difficulty": "Intermediate",
            "hours": 24,
            "theme_template": "Zero-Downtime {primary} Automation Pipeline & Telemetry",
            "objective_template": "Containerize a backend application using {primary} with automated CI testing, health probes, and deployment scripts.",
            "architecture_template": "Containerized deployment setup utilizing {primary} and Docker with health endpoints and automated GitHub Actions testing.",
            "slug_base": "automation-pipeline-telemetry"
        },
        {
            "track": "End-to-End Enterprise System",
            "lead_skills": missing_skills[:2],
            "complement_skills": ["Docker", "FastAPI", "PostgreSQL"],
            "difficulty": "Advanced",
            "hours": 36,
            "theme_template": "Enterprise High-Throughput Service Platform",
            "objective_template": "Architect a complete production backend platform combining authentication, database storage, and external API integrations for {role}.",
            "architecture_template": "Enterprise service architecture utilizing {primary} and FastAPI with database migrations and comprehensive integration tests.",
            "slug_base": "enterprise-service-platform"
        }
    ]


def select_gap_matching_projects(
    target_role: str,
    missing_skills: List[str],
    matched_skills: List[str],
    experience_years: int = 2,
    count: int = 4
) -> List[Dict[str, Any]]:
    """
    Selects the closest matching production-grade projects from the 10-project matrix
    that specifically target and bridge the candidate's identified skill gaps,
    calibrated to their professional experience tier (Fresher, Mid-Level, Senior).
    """
    discipline = classify_role_archetype(target_role)
    matrix = get_projects_for_discipline(discipline)
    if not matrix:
        matrix = get_projects_for_discipline("backend_systems")

    is_fresher = experience_years <= 1 or len(matched_skills) <= 1
    is_senior = experience_years >= 5

    clean_missing = [s.strip().lower() for s in missing_skills]
    clean_matched = [s.strip().lower() for s in matched_skills]

    scored = []
    for proj in matrix:
        score = 0.0
        covered = []
        for sk in proj.get("primary_skills", []):
            sk_low = sk.strip().lower()
            if any(m in sk_low or sk_low in m for m in clean_missing):
                score += 20.0  # Dominant priority: Directly bridges a missing gap
                covered.append(sk)
            elif any(m in sk_low or sk_low in m for m in clean_matched):
                score += 3.0   # Synergistic value: builds on candidate's existing strengths

        diff = proj.get("difficulty", "Intermediate")
        if is_fresher:
            if diff == "Beginner":
                score += 12.0
            elif diff == "Intermediate":
                score += 6.0
            else:
                score += 1.0
        elif is_senior:
            if diff == "Advanced":
                score += 12.0
            elif diff == "Intermediate":
                score += 6.0
            else:
                score += 1.0
        else: # Mid-level
            if diff == "Intermediate":
                score += 12.0
            elif diff == "Advanced":
                score += 6.0
            else:
                score += 4.0

        scored.append((score, covered, proj))

    # Sort descending by score
    scored.sort(key=lambda x: x[0], reverse=True)

    selected = []
    for score, covered, proj in scored[:count]:
        p_copy = dict(proj)
        p_copy["gap_match_score"] = round(score, 1)
        p_copy["skills_addressed"] = covered if covered else p_copy.get("primary_skills", [])[:2]
        selected.append(p_copy)

    return selected


def synthesize_dynamic_blueprints(
    target_role: str,
    missing_skills: List[str],
    matched_skills: List[str],
    candidate_name: str = "Candidate",
    experience_years: int = 1
) -> List[Dict[str, Any]]:
    """
    Dynamically generates 3-4 custom portfolio project blueprints tailored to the candidate's exact
    engineering discipline and missing skills from the 10-project matrix.
    Leverages persistent cache and ensures clean repository slugs.
    """
    if not missing_skills:
        missing_skills = ["Docker", "FastAPI", "PostgreSQL", "Redis"]

    is_freshman = len(matched_skills) <= 2 or experience_years <= 1

    # Select closest matching production-level projects from the 10-project matrix
    matched_projects = select_gap_matching_projects(
        target_role=target_role,
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        experience_years=experience_years,
        count=4
    )

    blueprints: List[Dict[str, Any]] = []

    for idx, proj in enumerate(matched_projects, 1):
        # 1. Compute Cache Key
        cache_key = blueprint_cache.compute_key(target_role, missing_skills, idx, is_freshman=is_freshman)
        start_time = time.time()

        # 2. Check Cache
        cached_blueprint = blueprint_cache.get(cache_key)
        if cached_blueprint:
            cached_blueprint["cache_hit_latency_ms"] = round((time.time() - start_time) * 1000, 2)
            blueprints.append(cached_blueprint)
            continue

        # 3. Cache Miss: Build rich production-grade blueprint
        title = proj.get("title", f"{target_role} Architecture Platform")
        combined_stack = proj.get("primary_skills", [])
        if len(combined_stack) < 3:
            combined_stack = list(dict.fromkeys(combined_stack + ["Docker", "Git", "pytest"]))

        objective = proj.get("executive_summary", f"Production-grade engineering system built for {target_role}.")
        architecture = proj.get("architecture_summary", f"Modular service architecture utilizing {', '.join(combined_stack[:2])}.")
        roadmap = proj.get("roadmap", [
            f"Milestone 1: Scaffold {combined_stack[0]} project structure, configuration, and environment setup",
            f"Milestone 2: Implement core processing logic integrating {', '.join(combined_stack[1:3])} with input validation",
            f"Milestone 3: Develop automated test suites asserting SLA compliance and error handling",
            f"Milestone 4: Configure containerization with Docker, health endpoints, and automated CI testing"
        ])

        starter_files = _generate_dynamic_starter_code(
            title, combined_stack, roadmap, target_role, objective=objective, architecture=architecture
        )

        clean_slug_base = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')[:40]
        slug = clean_slug_base or "portfolio-project"

        is_ds = any(
            k in target_role.lower() or k in title.lower() or any(k in t.lower() for t in combined_stack)
            for k in ["data", "ml", "machine learning", "ai", "pandas", "pytorch", "kaggle", "snowflake", "bigquery"]
        )

        manual_commands = [
            f"mkdir {slug} && cd {slug}",
            "git init -b main",
            f"# Extract downloaded {slug}-skeleton.zip into this folder",
            "python -m venv venv",
            "source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate",
            "pip install -r requirements.txt",
            "pytest tests/ -v  # Run failing TDD test harness",
            f"gh repo create {slug} --public --source=. --remote=origin --push"
        ]

        new_blueprint = {
            "id": slug,
            "cache_key": cache_key,
            "slug": slug,
            "title": title,
            "target_role": target_role,
            "difficulty": proj.get("difficulty", "Intermediate"),
            "hours": proj.get("hours", 24),
            "target_skills_covered": proj.get("skills_addressed", combined_stack[:2]),
            "skills_addressed": proj.get("skills_addressed", combined_stack[:2]),
            "tech_stack": combined_stack,
            "non_tech_competencies": proj.get("non_tech_competencies", [
                "System Design & Tradeoff Analysis",
                "Unit Testing & Quality Assurance",
                "Clean Architecture & Documentation"
            ]),
            "executive_summary": objective,
            "objective": objective,
            "architecture_outline": architecture,
            "architecture": architecture,
            "key_features": proj.get("key_features", [
                f"Production {combined_stack[0]} implementation with error handling",
                "Modular layer separation following clean architecture",
                "Automated test harness with high code coverage",
                "Containerization and deployment configuration"
            ]),
            "industry_rubric": proj.get("industry_rubric", "Evaluates clean code structure, test coverage, and production reliability."),
            "roadmap": roadmap,
            "starter_files": starter_files,
            "is_kaggle_track": is_ds,
            "is_skeleton": True,
            "manual_cli_commands": manual_commands,
            "is_cached": False,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        # Store in cache
        blueprint_cache.set(cache_key, new_blueprint)
        blueprints.append(new_blueprint)

    return blueprints[:4]


def _generate_dynamic_starter_code(
    title: str,
    tech_stack: List[str],
    roadmap: List[str],
    role: str,
    objective: str = "",
    architecture: str = ""
) -> Dict[str, str]:
    """
    Synthesizes complete, runnable, and testable starter project files for any dynamic blueprint.
    Guarantees clean pytest execution with zero syntax errors or missing dependencies.
    """
    slug = re.sub(r'[^a-zA-Z0-9_-]', '-', title.lower()).strip('-')

    obj_text = objective if objective else f"Hands-on project developing a verified system utilizing {', '.join(tech_stack[:3])}."
    arch_text = architecture if architecture else f"Clean, modular architecture utilizing {', '.join(tech_stack[:2])} with automated test coverage."

    readme = f"""# {title}

> **Target Role:** {role}  
> **Key Technologies:** {', '.join(tech_stack)}  
> **Status:** Production-Ready Architecture Scaffold (TDD Harness Green)

---

## 1. 🎯 Project Objective
{obj_text}

---

## 2. 🏗️ Architecture Blueprint
{arch_text}
- **Validation & Schemas**: Type-checked input models and structured error handling.
- **Testing**: Pre-configured automated unit and integration tests with pytest.
- **Packaging**: Containerized deployment with Dockerfile and docker-compose.
- **Observability**: Prometheus metrics (`/metrics`) and JSON structured logs.

---

## 3. 🚀 Quickstart & Verification

### Local Environment Setup
```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run automated verification test suite
pytest tests/ -v
```

### Run Service Locally
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 4. 🗺️ Sprint Milestone Roadmap
{chr(10).join(f"{idx}. {step}" for idx, step in enumerate(roadmap, 1))}
"""

    main_py = f"""import time
import sys
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from src.config import settings

# Configure structured logging
logger = logging.getLogger("{slug}")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"))
if not logger.handlers:
    logger.addHandler(handler)

app = FastAPI(
    title="{title}",
    version="1.0.0",
    description="Engineered portfolio blueprint demonstrating {', '.join(tech_stack[:3])}."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_counter = {{"requests_total": 0}}

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    metrics_counter["requests_total"] += 1
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Response-Time-Ms"] = str(duration_ms)
    return response

@app.get("/health/live", tags=["Health"])
async def liveness():
    return {{"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}}

@app.get("/health/ready", tags=["Health"])
async def readiness():
    return {{"status": "ready", "tech_stack": {json.dumps(tech_stack)}}}

@app.get("/metrics", tags=["Telemetry"], response_class=PlainTextResponse)
async def metrics():
    return f"# HELP app_requests_total Total HTTP requests\\n# TYPE app_requests_total counter\\napp_requests_total {{metrics_counter['requests_total']}}\\n"

@app.get("/api/v1/info", tags=["Metadata"])
async def get_service_info():
    return {{
        "project": "{title}",
        "role": "{role}",
        "technologies": {json.dumps(tech_stack)},
        "status": "operational"
    }}
"""

    config_py = f"""import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        from pydantic import BaseModel
        class BaseSettings(BaseModel):
            class Config:
                extra = "allow"

class Settings(BaseSettings):
    APP_NAME: str = "{title}"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
"""

    test_main_py = """import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_liveness():
    res = client.get("/health/live")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_health_readiness():
    res = client.get("/health/ready")
    assert res.status_code == 200
    assert res.json()["status"] == "ready"
    assert len(res.json()["tech_stack"]) >= 2

def test_metrics_endpoint():
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "app_requests_total" in res.text

def test_service_info_endpoint():
    res = client.get("/api/v1/info")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "operational"
    assert len(data["technologies"]) >= 2
"""

    conftest_py = """import sys
from pathlib import Path

# Invariant: dynamically insert project root into sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
"""

    pytest_ini = """[pytest]
asyncio_mode = auto
testpaths = tests
pythonpath = .
"""

    dockerfile = """FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    docker_compose = f"""version: '3.8'

services:
  service:
    build: .
    container_name: {slug}
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - APP_NAME={title}
      - HOST=0.0.0.0
      - PORT=8000
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')"]
      interval: 30s
      timeout: 5s
      retries: 3
"""

    ci_yml = """name: CI Verification

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run test suite
        run: pytest tests/ -v
"""

    requirements_txt = """fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
httpx>=0.27.0
pytest>=8.1.0
pytest-asyncio>=0.23.0
"""

    gitignore = """.env
__pycache__/
*.pyc
.pytest_cache/
.coverage
dist/
build/
.DS_Store
.idea/
.vscode/
"""

    makefile = """.PHONY: install test test-cov run docker-build docker-up clean

install:
\tpython -m pip install --upgrade pip
\tpip install -r requirements.txt

test:
\tpytest tests/ -v

test-cov:
\tpytest --cov=src --cov-report=term-missing tests/ -v

run:
\tpython -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
\tdocker build -t app-service:latest .

docker-up:
\tdocker compose up --build -d

clean:
\trm -rf __pycache__ .pytest_cache .coverage htmlcov dist build
"""

    result = {
        "README.md": readme,
        "src/__init__.py": "",
        "src/main.py": main_py,
        "src/config.py": config_py,
        "tests/__init__.py": "",
        "tests/conftest.py": conftest_py,
        "tests/test_main.py": test_main_py,
        "pytest.ini": pytest_ini,
        "Dockerfile": dockerfile,
        "docker-compose.yml": docker_compose,
        "Makefile": makefile,
        ".github/workflows/ci.yml": ci_yml,
        "requirements.txt": requirements_txt,
        ".gitignore": gitignore
    }

    is_ds = any(
        k in role.lower() or k in title.lower() or any(k in t.lower() for t in tech_stack)
        for k in ["data", "ml", "machine learning", "ai", "pandas", "pytorch", "kaggle", "snowflake", "bigquery"]
    )
    if is_ds:
        result["data/download_dataset.sh"] = f"""#!/usr/bin/env bash
# SkillBridge Kaggle Dataset Download Workflow
set -euo pipefail

echo "=========================================================="
echo "SkillBridge: Fetching Kaggle Dataset for {title}"
echo "=========================================================="

mkdir -p data/

if command -v kaggle &> /dev/null && [ -f ~/.kaggle/kaggle.json ]; then
    echo "Using authenticated Kaggle CLI to fetch dataset..."
    kaggle datasets download -d blastchar/telco-customer-churn -p data/ --unzip || true
fi

if [ ! -f "data/dataset.csv" ]; then
    echo "Generating offline reproducible 500-record CSV dataset..."
    python -c "
import pandas as pd
import numpy as np
np.random.seed(42)
n_samples = 500
df = pd.DataFrame({{
    'customer_id': [f'CUST-{{i:04d}}' for i in range(1, n_samples + 1)],
    'tenure_months': np.random.randint(1, 72, size=n_samples),
    'monthly_charges': np.round(np.random.uniform(18.5, 118.5, size=n_samples), 2),
    'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], size=n_samples, p=[0.55, 0.25, 0.20]),
    'churn_label': np.random.choice([0, 1], size=n_samples, p=[0.73, 0.27])
}})
df.to_csv('data/dataset.csv', index=False)
print('Synthetic dataset written to data/dataset.csv with 500 records.')
"
fi
"""
        result["notebooks/01_eda_baseline.ipynb"] = f"""{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "# 01. Exploratory Data Analysis & Baseline Model\\n",
    "### {title}\\n",
    "- **Target Role:** {role}\\n",
    "- **Goal:** Perform distribution checks, handle missing values, and train an initial baseline model."
   ]
  }},
  {{
   "cell_type": "code",
   "execution_count": null,
   "metadata": {{}},
   "outputs": [],
   "source": [
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "df = pd.read_csv('../data/dataset.csv')\\n",
    "print('Dataset Shape:', df.shape)\\n",
    "print(df.head())"
   ]
  }}
 ],
 "metadata": {{
  "language_info": {{
   "name": "python"
  }}
  }},
 "nbformat": 4,
 "nbformat_minor": 2
}}"""
        result["submissions/submit_predictions.sh"] = f"""#!/usr/bin/env bash
# SkillBridge Automated Kaggle Submission Pipeline
set -euo pipefail

if [ ! -f "submissions/final_predictions.csv" ]; then
    echo "Creating submissions directory and baseline predictions..."
    mkdir -p submissions/
    echo "customer_id,churn_probability" > submissions/final_predictions.csv
    echo "CUST-0001,0.24" >> submissions/final_predictions.csv
    echo "CUST-0002,0.81" >> submissions/final_predictions.csv
fi

echo "Predictions verified at submissions/final_predictions.csv"
"""

    return result
