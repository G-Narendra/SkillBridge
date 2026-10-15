"""
Role-Based Dynamic Metric Dimensions & Archetype Taxonomy Engine.
Provides domain-calibrated evaluation dimensions for all 465+ technology roles,
eliminating irrelevant metrics (e.g., databases for frontend engineers, web frameworks for SREs)
and establishing authentic, discipline-accurate competency benchmarking.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from cv_parser import canonicalize_skill

# The 12 Core Engineering Archetype Families
ARCHETYPE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "frontend_ui": {
        "id": "frontend_ui",
        "name": "Frontend & Interface Engineering",
        "rationale": "Evaluates component architecture, reactive state management, CSS layout/design tokens, and client runtime performance. Server-side relational database management is not a core competency and has been omitted to guarantee authentic, fair benchmarking.",
        "omitted_metrics": ["Relational & NoSQL Databases", "Server-Side Microservice Runtimes", "Big Data Platforms"],
        "dimensions": {
            "core_languages": {
                "label": "Core Web Languages",
                "weight": 0.30,
                "icon": "code",
                "default_skills": ["TypeScript", "JavaScript", "HTML"]
            },
            "ui_frameworks": {
                "label": "UI Frameworks & State",
                "weight": 0.35,
                "icon": "layers",
                "default_skills": ["React", "Next.js", "Vue", "Redux", "Tailwind CSS"]
            },
            "styling_design_systems": {
                "label": "Design Systems & Modern Styling",
                "weight": 0.20,
                "icon": "palette",
                "default_skills": ["Tailwind CSS", "CSS", "Sass", "Responsive Design", "Figma"]
            },
            "accessibility_performance": {
                "label": "Web Quality, WCAG & Tooling",
                "weight": 0.15,
                "icon": "check_circle",
                "default_skills": ["Git", "Vite", "Webpack", "Postman", "Jest"]
            }
        }
    },
    "backend_systems": {
        "id": "backend_systems",
        "name": "Backend & Distributed Systems",
        "rationale": "Evaluates server runtimes, concurrency, resilient data modeling, transactional storage, and microservice containerization. Client-side browser styling and mobile SDKs are omitted.",
        "omitted_metrics": ["Client UI Styling & CSS", "Mobile Application SDKs"],
        "dimensions": {
            "core_languages": {
                "label": "Core Systems Languages",
                "weight": 0.30,
                "icon": "code",
                "default_skills": ["Python", "Go", "Java", "SQL", "C++", "Rust"]
            },
            "service_frameworks": {
                "label": "Microservice Frameworks & APIs",
                "weight": 0.25,
                "icon": "layers",
                "default_skills": ["FastAPI", "Django", "Express", "Node.js", "Spring Boot"]
            },
            "databases_storage": {
                "label": "Databases, Caching & Storage",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["PostgreSQL", "Redis", "MongoDB", "MySQL", "Elasticsearch"]
            },
            "infra_deployment": {
                "label": "Containerization & Cloud Infra",
                "weight": 0.20,
                "icon": "wrench",
                "default_skills": ["Docker", "Kubernetes", "Git", "AWS", "Linux"]
            }
        }
    },
    "devops_platform": {
        "id": "devops_platform",
        "name": "DevOps, SRE & Platform Engineering",
        "rationale": "Evaluates declarative infrastructure as code, container clustering, CI/CD delivery pipelines, and distributed observability. Web application frontend frameworks and application relational databases are omitted.",
        "omitted_metrics": ["Web Frontend Frameworks", "Application Relational Databases", "Mobile UI kits"],
        "dimensions": {
            "iac_cloud": {
                "label": "Infrastructure as Code & Cloud",
                "weight": 0.35,
                "icon": "cloud",
                "default_skills": ["Terraform", "AWS", "Google Cloud", "Azure", "Ansible"]
            },
            "container_orchestration": {
                "label": "Containerization & Orchestration",
                "weight": 0.30,
                "icon": "server",
                "default_skills": ["Docker", "Kubernetes", "Helm", "Linux"]
            },
            "cicd_automation": {
                "label": "CI/CD & Scripting Automation",
                "weight": 0.20,
                "icon": "terminal",
                "default_skills": ["GitHub Actions", "GitLab CI", "Bash", "Python", "Git"]
            },
            "observability_telemetry": {
                "label": "Observability, SRE & Telemetry",
                "weight": 0.15,
                "icon": "activity",
                "default_skills": ["Prometheus", "Grafana", "Sentry", "Nginx"]
            }
        }
    },
    "data_analytics": {
        "id": "data_analytics",
        "name": "Data Analytics & Business Intelligence",
        "rationale": "Evaluates analytical queries, statistical data manipulation, enterprise data warehouse models, and executive dashboards. Web application development frameworks and low-level system kernels are omitted.",
        "omitted_metrics": ["Web Application Frameworks", "Low-Level Kernel APIs", "Microservice IPC"],
        "dimensions": {
            "query_languages": {
                "label": "Analytical Query Languages",
                "weight": 0.35,
                "icon": "code",
                "default_skills": ["SQL", "Python", "R"]
            },
            "data_manipulation": {
                "label": "Data Wrangling & Computation",
                "weight": 0.25,
                "icon": "cpu",
                "default_skills": ["Pandas", "NumPy", "Excel", "Scikit-learn"]
            },
            "warehouses_modeling": {
                "label": "Cloud Data Warehouses & Modeling",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["Snowflake", "BigQuery", "PostgreSQL", "dbt"]
            },
            "bi_visualization": {
                "label": "BI Dashboards & Visual Storytelling",
                "weight": 0.15,
                "icon": "bar-chart",
                "default_skills": ["Tableau", "Power BI", "Git"]
            }
        }
    },
    "data_engineering": {
        "id": "data_engineering",
        "name": "Data Engineering & Distributed Platforms",
        "rationale": "Evaluates distributed computation engines, batch/streaming pipelines, data lakes, and automated workflow orchestrators. Client-side UI frameworks and mobile SDKs are omitted.",
        "omitted_metrics": ["Client UI Frameworks", "Mobile Development SDKs", "CSS Styling"],
        "dimensions": {
            "distributed_computing": {
                "label": "Distributed Processing & Streaming",
                "weight": 0.35,
                "icon": "cpu",
                "default_skills": ["Apache Spark", "Apache Kafka", "Python", "Scala"]
            },
            "data_warehousing_lakes": {
                "label": "Data Warehouses & Lakehouses",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["Snowflake", "BigQuery", "PostgreSQL", "Redis"]
            },
            "pipeline_orchestration": {
                "label": "Pipeline Orchestration & Transformations",
                "weight": 0.25,
                "icon": "git-branch",
                "default_skills": ["Apache Airflow", "dbt", "Docker"]
            },
            "core_engineering": {
                "label": "Core Systems & Infrastructure",
                "weight": 0.15,
                "icon": "wrench",
                "default_skills": ["SQL", "Git", "Linux", "AWS"]
            }
        }
    },
    "ml_engineering": {
        "id": "ml_engineering",
        "name": "Machine Learning & Deep Learning",
        "rationale": "Evaluates mathematical modeling, neural network architectures, distributed inference runtimes, and vector stores. Web frontend presentation layers and relational schema tuning are omitted.",
        "omitted_metrics": ["Web Frontend UI", "CSS Design Systems", "Legacy Relational Schema Tuning"],
        "dimensions": {
            "ml_languages_math": {
                "label": "ML Programming & Numerical Math",
                "weight": 0.25,
                "icon": "code",
                "default_skills": ["Python", "C++", "SQL", "CUDA"]
            },
            "deep_learning_frameworks": {
                "label": "Model Training & Frameworks",
                "weight": 0.35,
                "icon": "cpu",
                "default_skills": ["PyTorch", "TensorFlow", "Scikit-learn", "Keras"]
            },
            "mlops_deployment": {
                "label": "Model Serving & MLOps Pipelines",
                "weight": 0.25,
                "icon": "server",
                "default_skills": ["FastAPI", "Docker", "Linux", "Git"]
            },
            "feature_vector_stores": {
                "label": "Feature Stores & Vector Retrieval",
                "weight": 0.15,
                "icon": "database",
                "default_skills": ["PostgreSQL", "Elasticsearch", "Redis"]
            }
        }
    },
    "ai_agents": {
        "id": "ai_agents",
        "name": "AI Agents, LLMs & Cognitive Systems",
        "rationale": "Evaluates multi-agent orchestration, tool usage, dense vector indexing, semantic search, and prompt guardrails. Legacy relational database administration and web styling are omitted.",
        "omitted_metrics": ["Legacy Relational DB Admin", "Browser CSS & Styling", "Mobile App SDKs"],
        "dimensions": {
            "agentic_frameworks": {
                "label": "Agentic Frameworks & Tool Use",
                "weight": 0.35,
                "icon": "cpu",
                "default_skills": ["LangChain", "LlamaIndex", "CrewAI", "FastAPI"]
            },
            "vector_rag_retrieval": {
                "label": "Vector Databases & Semantic Retrieval",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["Pinecone", "ChromaDB", "Milvus", "PostgreSQL"]
            },
            "llm_apis_guardrails": {
                "label": "Model APIs, Prompting & Guardrails",
                "weight": 0.25,
                "icon": "terminal",
                "default_skills": ["Python", "TypeScript", "SQL"]
            },
            "service_orchestration": {
                "label": "Async Microservices & Containerization",
                "weight": 0.15,
                "icon": "wrench",
                "default_skills": ["Docker", "Git", "Linux", "AWS"]
            }
        }
    },
    "security_cyber": {
        "id": "security_cyber",
        "name": "Cybersecurity & Application Security",
        "rationale": "Evaluates penetration testing tools, cryptographic protocols, OS hardening, and compliance automation. Web visual design systems and relational database tuning are omitted.",
        "omitted_metrics": ["Web Frontend Visual Design", "Relational Database Performance Tuning"],
        "dimensions": {
            "security_tooling": {
                "label": "Security Auditing & Pen-testing",
                "weight": 0.35,
                "icon": "shield",
                "default_skills": ["Linux", "Docker", "Git"]
            },
            "protocols_identity": {
                "label": "Protocols, Cryptography & Identity",
                "weight": 0.30,
                "icon": "key",
                "default_skills": ["PostgreSQL", "Elasticsearch"]
            },
            "defensive_hardening": {
                "label": "OS Hardening, WAF & Container Security",
                "weight": 0.20,
                "icon": "server",
                "default_skills": ["Kubernetes", "Linux"]
            },
            "security_automation": {
                "label": "Security Scripting & Automation",
                "weight": 0.15,
                "icon": "terminal",
                "default_skills": ["Python", "Bash", "Go", "C++"]
            }
        }
    },
    "mobile_dev": {
        "id": "mobile_dev",
        "name": "Mobile Application Engineering",
        "rationale": "Evaluates native mobile toolchains, client-side caching, reactive UI layouts, and app store release pipelines. Distributed backend cluster management and big data engines are omitted.",
        "omitted_metrics": ["Cloud Infrastructure Orchestration", "Distributed Big Data Systems"],
        "dimensions": {
            "mobile_languages": {
                "label": "Native & Cross-Platform Languages",
                "weight": 0.35,
                "icon": "smartphone",
                "default_skills": ["Swift", "Kotlin", "TypeScript", "JavaScript"]
            },
            "mobile_frameworks": {
                "label": "Mobile Frameworks & UI Kits",
                "weight": 0.35,
                "icon": "layers",
                "default_skills": ["React", "Node.js"]
            },
            "client_state_storage": {
                "label": "Client Persistence & Network Layer",
                "weight": 0.15,
                "icon": "database",
                "default_skills": ["SQLite", "Postman"]
            },
            "mobile_tooling_cicd": {
                "label": "Build Tooling & Distribution CI/CD",
                "weight": 0.15,
                "icon": "wrench",
                "default_skills": ["Git", "GitHub Actions", "Linux"]
            }
        }
    },
    "embedded_systems": {
        "id": "embedded_systems",
        "name": "Embedded, Firmware & Kernel Systems",
        "rationale": "Evaluates low-level languages, memory bounds, real-time operating systems, and hardware peripherals. Web application development and enterprise analytics are omitted.",
        "omitted_metrics": ["Web Application Frameworks", "Cloud SaaS Tooling", "Enterprise Relational DBs"],
        "dimensions": {
            "low_level_languages": {
                "label": "Low-Level Memory-Managed Languages",
                "weight": 0.40,
                "icon": "code",
                "default_skills": ["C++", "Rust", "Go", "Bash"]
            },
            "rtos_kernel": {
                "label": "RTOS, Kernel & Concurrency",
                "weight": 0.25,
                "icon": "cpu",
                "default_skills": ["Linux", "Node.js"]
            },
            "hardware_protocols": {
                "label": "Hardware Protocols & Peripheral Storage",
                "weight": 0.20,
                "icon": "database",
                "default_skills": ["SQLite", "Redis"]
            },
            "profiling_toolchains": {
                "label": "Toolchains, Debugging & Build Systems",
                "weight": 0.15,
                "icon": "wrench",
                "default_skills": ["Docker", "Git", "Prometheus"]
            }
        }
    },
    "blockchain_web3": {
        "id": "blockchain_web3",
        "name": "Blockchain & Smart Contract Systems",
        "rationale": "Evaluates smart contract security, gas optimization, cryptographic protocols, and Web3 RPC libraries. Traditional cloud cluster orchestration is omitted.",
        "omitted_metrics": ["Traditional Cloud Cluster Orchestration", "Enterprise BI Dashboards"],
        "dimensions": {
            "smart_contracts": {
                "label": "Smart Contract Languages & Gas",
                "weight": 0.40,
                "icon": "code",
                "default_skills": ["Solidity", "Rust", "TypeScript", "JavaScript"]
            },
            "web3_frameworks": {
                "label": "Web3 Frameworks & Node Services",
                "weight": 0.30,
                "icon": "layers",
                "default_skills": ["Next.js", "React", "Node.js"]
            },
            "decentralized_storage": {
                "label": "Protocol Persistence & Caching",
                "weight": 0.15,
                "icon": "database",
                "default_skills": ["PostgreSQL", "Redis"]
            },
            "security_auditing": {
                "label": "Security Auditing & Test Toolchains",
                "weight": 0.15,
                "icon": "shield",
                "default_skills": ["Git", "Docker", "Linux", "Postman"]
            }
        }
    },
    "fullstack_general": {
        "id": "fullstack_general",
        "name": "Fullstack & General Software Engineering",
        "rationale": "Balanced generalist rubric evaluating full-lifecycle delivery spanning client UI, server-side APIs, database modeling, and deployment pipelines.",
        "omitted_metrics": [],
        "dimensions": {
            "fullstack_languages": {
                "label": "Fullstack Languages",
                "weight": 0.25,
                "icon": "code",
                "default_skills": ["TypeScript", "JavaScript", "Python", "SQL"]
            },
            "frontend_ui": {
                "label": "Frontend UI & Client Architecture",
                "weight": 0.25,
                "icon": "layers",
                "default_skills": ["React", "Next.js", "FastAPI", "Node.js"]
            },
            "backend_services": {
                "label": "Databases & Data Modeling",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["PostgreSQL", "MongoDB", "Redis"]
            },
            "databases_devops": {
                "label": "DevOps & Deployment Pipelines",
                "weight": 0.25,
                "icon": "wrench",
                "default_skills": ["Docker", "Git", "GitHub Actions", "AWS"]
            }
        }
    }
}


def classify_role_archetype(role_name: str) -> str:
    """
    Classifies any target role name into its optimal Engineering Discipline Archetype.
    """
    r = role_name.lower().strip()

    # 1. AI Agents & LLMs
    if any(k in r for k in ["agent", "llm", "rag", "prompt", "cognitive", "langchain", "llamaindex"]):
        return "ai_agents"

    # 2. Machine Learning & Deep Learning
    if any(k in r for k in ["machine learning", "ml engineer", "deep learning", "computer vision", "nlp", "cuda"]):
        return "ml_engineering"

    # 3. Data Analytics & BI
    if any(k in r for k in ["data analyst", "analytics", "business intelligence", "bi ", "tableau", "power bi"]):
        return "data_analytics"

    # 4. Data Engineering & Big Data
    if any(k in r for k in ["data engineer", "big data", "etl", "spark", "pipeline", "streaming"]):
        return "data_engineering"

    # 5. DevOps, SRE & Platform
    if any(k in r for k in ["devops", "sre", "reliability", "infrastructure", "cloud architect", "platform engineer", "sysadmin"]):
        return "devops_platform"

    # 6. Frontend & UI/UX
    if any(k in r for k in ["frontend", "front-end", "ui developer", "ux engineer", "web designer", "react developer", "css"]):
        return "frontend_ui"

    # 7. Mobile Development
    if any(k in r for k in ["mobile", "ios", "android", "flutter", "react native", "swift"]):
        return "mobile_dev"

    # 8. Security & Cyber
    if any(k in r for k in ["security", "cyber", "penetration", "soc", "infosec", "appsec"]):
        return "security_cyber"

    # 9. Blockchain & Web3
    if any(k in r for k in ["blockchain", "solidity", "web3", "smart contract", "crypto", "defi", "ethereum"]):
        return "blockchain_web3"

    # 10. Embedded & Systems
    if any(k in r for k in ["embedded", "firmware", "kernel", "iot", "hardware", "rtos", "systems engineer"]):
        return "embedded_systems"

    # 11. Backend & Distributed Systems
    if any(k in r for k in ["backend", "back-end", "api engineer", "microservices", "distributed systems", "server"]):
        return "backend_systems"

    # 12. Fullstack & Generalist (Default)
    return "fullstack_general"


def get_role_archetype_definition(role_name: str) -> Dict[str, Any]:
    """
    Retrieves the complete archetype definition for a role, including dimensions, weights, and rationale.
    """
    archetype_id = classify_role_archetype(role_name)
    return ARCHETYPE_REGISTRY.get(archetype_id, ARCHETYPE_REGISTRY["fullstack_general"])


def build_dynamic_role_profile(
    role_name: str,
    raw_profile: Optional[Dict[str, List[str]]] = None
) -> Tuple[Dict[str, List[str]], Dict[str, float], Dict[str, Any]]:
    """
    Constructs a role-calibrated dimension profile, dynamic weights, and archetype metadata.
    Maps skills to the role's true domain dimensions rather than rigid 4 generic categories.
    """
    archetype = get_role_archetype_definition(role_name)
    arch_dimensions = archetype["dimensions"]

    dynamic_profile: Dict[str, List[str]] = {}
    dynamic_weights: Dict[str, float] = {}

    # If raw_profile provided (e.g. from role_profiles_465.json), map skills intelligently into archetype dimensions
    flat_skills: List[str] = []
    if raw_profile:
        for cat_skills in raw_profile.values():
            flat_skills.extend([canonicalize_skill(s) for s in cat_skills])
        flat_skills = list(dict.fromkeys(flat_skills))

    dimension_keys = list(arch_dimensions.keys())
    
    for idx, dim_key in enumerate(dimension_keys):
        dim_cfg = arch_dimensions[dim_key]
        dynamic_weights[dim_key] = dim_cfg["weight"]

        if flat_skills:
            # Map subset of skills proportionally to this dimension if matching defaults
            assigned = [s for s in flat_skills if s in dim_cfg["default_skills"]]
            if not assigned:
                # Fallback to chunking skills across dimensions
                chunk_size = max(1, len(flat_skills) // len(dimension_keys))
                start_i = idx * chunk_size
                assigned = flat_skills[start_i:start_i + chunk_size] or dim_cfg["default_skills"]
            dynamic_profile[dim_key] = list(dict.fromkeys(assigned))
        else:
            dynamic_profile[dim_key] = list(dict.fromkeys(dim_cfg["default_skills"]))

    return dynamic_profile, dynamic_weights, archetype
