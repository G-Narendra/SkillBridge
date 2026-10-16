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
                "default_skills": ["Python", "SQL", "Go", "Java", "C++", "Rust"]
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
                "default_skills": ["PostgreSQL", "Redis", "MongoDB", "SQLite", "MySQL"]
            },
            "infra_deployment": {
                "label": "Containerization & Cloud Infra",
                "weight": 0.20,
                "icon": "wrench",
                "default_skills": ["Git", "Docker", "Linux", "Kubernetes", "AWS"]
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
        "name": "Cybersecurity, Ethical Hacking & Application Security",
        "rationale": "Evaluates penetration testing tools, cryptographic protocols, OS hardening, vulnerability assessment, and security automation. Web visual design systems, CSS/Tailwind, and general business analytics are omitted.",
        "omitted_metrics": ["Web Frontend Visual Design & CSS", "General Business Analytics", "Relational Database Performance Tuning"],
        "dimensions": {
            "security_tooling": {
                "label": "Security Auditing & Pen-Testing",
                "weight": 0.35,
                "icon": "shield",
                "default_skills": ["Burp Suite", "Nmap", "Wireshark", "Metasploit", "OWASP Top 10", "Linux"]
            },
            "protocols_identity": {
                "label": "Protocols, Cryptography & Network Security",
                "weight": 0.30,
                "icon": "key",
                "default_skills": ["TLS/SSL", "Cryptography", "SSH", "Packet Analysis", "VPN"]
            },
            "defensive_hardening": {
                "label": "OS Hardening, WAF & Container Security",
                "weight": 0.20,
                "icon": "server",
                "default_skills": ["Linux", "Docker", "WAF", "SQL Injection", "XSS Prevention"]
            },
            "security_automation": {
                "label": "Security Scripting & Exploit Analysis",
                "weight": 0.15,
                "icon": "terminal",
                "default_skills": ["Python", "Bash", "Go", "C", "Git"]
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
    "tech_leadership_advisory": {
        "id": "tech_leadership_advisory",
        "name": "Technology Leadership & Architecture Strategy",
        "rationale": "Evaluates strategic technology vision, system architecture governance, risk management, and organizational scaling. Routine implementation syntax is omitted to reflect executive and advisory scope.",
        "omitted_metrics": ["Routine Implementation Scripting", "Low-Level Database DDL", "Container Configuration"],
        "dimensions": {
            "tech_strategy": {
                "label": "Technology Strategy & Architecture",
                "weight": 0.35,
                "icon": "activity",
                "default_skills": ["System Architecture", "Tech Strategy", "Cloud Strategy", "Enterprise Architecture"]
            },
            "data_product_governance": {
                "label": "Data Governance & Compliance",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["Data Governance", "SQL", "Compliance", "Security Auditing"]
            },
            "operational_scale": {
                "label": "Scalability, Cloud Economics & Risk",
                "weight": 0.20,
                "icon": "cloud",
                "default_skills": ["Cloud Economics", "Risk Management", "Disaster Recovery", "Vendor Evaluation"]
            },
            "engineering_leadership": {
                "label": "Engineering Leadership & Roadmapping",
                "weight": 0.20,
                "icon": "shield",
                "default_skills": ["Technical Leadership", "Agile Governance", "Roadmapping", "Team Topologies"]
            }
        }
    },
    "marketplace_systems": {
        "id": "marketplace_systems",
        "name": "Marketplace Systems & Algorithmic Engineering",
        "rationale": "Evaluates two-sided supply/demand matching algorithms, dynamic surge pricing models, multi-party payment ledgers, and marketplace fraud prevention. Client UI styling and mobile SDKs are omitted.",
        "omitted_metrics": ["Client UI Styling & CSS", "Mobile Application SDKs", "Static CMS"],
        "dimensions": {
            "matching_dispatch": {
                "label": "Matching, Dispatch & Geospatial Engines",
                "weight": 0.30,
                "icon": "activity",
                "default_skills": ["Python", "Go", "Redis", "PostgreSQL", "SQL"]
            },
            "dynamic_pricing_auctions": {
                "label": "Dynamic Pricing, Auctions & Elasticity",
                "weight": 0.25,
                "icon": "trending_up",
                "default_skills": ["Python", "FastAPI", "Redis", "SQL", "Pandas"]
            },
            "escrow_ledgers_payments": {
                "label": "Multi-Party Escrow, Ledgers & Payouts",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["PostgreSQL", "FastAPI", "Redis", "Docker"]
            },
            "trust_reputation_fraud": {
                "label": "Trust, Reputation & Fraud Prevention",
                "weight": 0.20,
                "icon": "shield",
                "default_skills": ["Python", "Docker", "Apache Kafka", "Git", "pytest"]
            }
        }
    },
    "fullstack_general": {
        "id": "fullstack_general",
        "name": "Software Engineering",
        "rationale": "Evaluates core full-lifecycle software delivery covering application logic, interfaces, persistence, and deployment.",
        "omitted_metrics": [],
        "dimensions": {
            "fullstack_languages": {
                "label": "Languages",
                "weight": 0.25,
                "icon": "code",
                "default_skills": ["TypeScript", "JavaScript", "Python", "SQL"]
            },
            "frontend_ui": {
                "label": "Frontend & UI",
                "weight": 0.25,
                "icon": "layers",
                "default_skills": ["React", "Next.js", "Vue", "Tailwind CSS"]
            },
            "backend_services": {
                "label": "Databases & Storage",
                "weight": 0.25,
                "icon": "database",
                "default_skills": ["PostgreSQL", "MongoDB", "Redis"]
            },
            "databases_devops": {
                "label": "DevOps & Cloud",
                "weight": 0.25,
                "icon": "wrench",
                "default_skills": ["Docker", "Git", "GitHub Actions", "AWS"]
            }
        }
    }
}


def classify_role_archetype(role_name: str) -> str:
    """
    Classifies any target role name into its optimal Engineering Discipline Archetype (1 of 14).
    Guarantees authentic, domain-accurate competency benchmarking and project proposals.
    Uses regex word boundaries for short acronyms (e.g. cto, cso, qa, bi, k8s, soc) to prevent substring false positives.
    """
    r = role_name.lower().strip()

    def _has_kw(text: str, kw: str) -> bool:
        if len(kw) <= 4:
            return bool(re.search(r'\b' + re.escape(kw) + r'\b', text))
        return kw in text

    # 1. Marketplace, Matching & Platform Economics
    if any(_has_kw(r, k) for k in [
        "marketplace", "matching algorithm", "dispatch", "dynamic pricing", "ledger engineer",
        "two-sided", "fintech", "payments", "ecommerce", "e-commerce", "creator economy", "proptech", "edtech", "legaltech", "govtech"
    ]):
        return "marketplace_systems"

    # 2. Cybersecurity & Ethical Hacking
    if any(_has_kw(r, k) for k in [
        "security", "cyber", "penetration", "soc", "infosec", "appsec", "hacker", "hacking",
        "ethical hacker", "pentest", "red team", "blue team", "exploit", "vulnerability", "threat",
        "forensics", "malware", "incident response", "incident responder", "secops", "devsecops", "network security",
        "wireless security", "trust safety"
    ]):
        return "security_cyber"

    # 3. Blockchain & Web3 Protocols
    if any(_has_kw(r, k) for k in [
        "blockchain", "solidity", "web3", "smart contract", "crypto", "defi", "ethereum",
        "protocol engineer", "defi strategist"
    ]):
        return "blockchain_web3"

    # 4. Embedded Systems & Firmware
    if any(_has_kw(r, k) for k in [
        "embedded", "firmware", "kernel", "iot", "hardware", "rtos", "microcontroller", "robotics",
        "electrical engineer", "biomedical engineer", "energy systems", "defense tech"
    ]):
        return "embedded_systems"

    # 5. Mobile Application Engineering
    if any(_has_kw(r, k) for k in ["mobile", "ios", "android", "flutter", "react native", "swift"]):
        return "mobile_dev"

    # 6. AI Agents & Intelligent Systems
    if any(_has_kw(r, k) for k in [
        "ai engineer", "ai architect", "ai agents", "ai integration", "ai safety", "ai ethics",
        "agent", "llm", "rag", "prompt", "cognitive", "langchain", "llamaindex", "generative ai",
        "genai", "vector database", "vector db"
    ]):
        return "ai_agents"

    # 7. Machine Learning & Deep Learning
    if any(_has_kw(r, k) for k in [
        "machine learning", "ml engineer", "mlops", "ml ops", "ai/ml", "deep learning", "computer vision",
        "nlp", "cuda", "data scientist", "research scientist", "r&d scientist", "r d scientist",
        "recommendation", "search engineer", "deep researcher", "dataset engineer"
    ]):
        return "ml_engineering"

    # 8. Data Engineering & Lakehouses
    if any(_has_kw(r, k) for k in [
        "data engineer", "big data", "etl", "spark", "pipeline", "streaming", "data architect",
        "database administrator", "database admin", "database engineer", "database migration",
        "database reliability", "data governance", "data labeling", "data privacy", "gdpr dpo",
        "dbt", "snowflake", "lakehouse"
    ]):
        return "data_engineering"

    # 9. Data Analytics & Business Intelligence
    if any(_has_kw(r, k) for k in [
        "data analyst", "analytics", "business intelligence", "bi", "tableau", "power bi",
        "quantitative analyst", "fraud analyst", "churn analyst", "risk analyst", "product analyst",
        "business analyst", "web analytics", "kpi dashboard", "data visualization"
    ]):
        return "data_analytics"

    # 10. Frontend & UI/UX Design Systems
    if any(_has_kw(r, k) for k in [
        "frontend", "front-end", "ui developer", "ux engineer", "web designer", "react developer",
        "css", "design system", "product designer", "ui designer", "ux designer", "interaction designer",
        "user experience", "web performance", "accessibility", "onboarding designer", "prototyping"
    ]):
        return "frontend_ui"

    # 11. DevOps, SRE, Cloud & Platform
    if any(_has_kw(r, k) for k in [
        "devops", "sre", "reliability", "infrastructure", "cloud", "aws", "gcp", "azure", "vercel",
        "kubernetes", "k8s", "docker", "terraform", "platform engineer", "sysadmin", "systems administrator",
        "linux systems administrator", "monitoring engineer", "release engineer", "release manager",
        "chaos engineer", "it administrator", "it manager", "incident commander"
    ]):
        return "devops_platform"

    # 12. Technology Leadership, Architecture Strategy & Advisory
    if any(_has_kw(r, k) for k in [
        "cto", "vp engineering", "vp of engineering", "head of engineering", "director of engineering",
        "technical lead", "tech lead", "software architect", "enterprise architect", "solutions architect",
        "solution architect", "system designer", "advisory", "board member", "advisor", "executive", "cso",
        "strategy", "strategist", "governance", "tech leadership", "engineering leadership", "consultant",
        "technical program manager", "program manager", "product owner", "product manager", "head of product",
        "head of data", "information architect", "technical account manager", "technical director"
    ]):
        return "tech_leadership_advisory"

    # 13. Backend Systems & API Engineering
    if any(_has_kw(r, k) for k in [
        "backend", "back-end", "api engineer", "api gateway", "microservices", "distributed systems",
        "server", "java developer", "go developer", "python developer", "python backend", "php developer",
        "ruby developer", "rust developer", "sql developer", "dotnet", ".net", "c#", "c++", "systems engineer",
        "systems analyst", "qa", "quality assurance", "test engineer", "tester", "test automation",
        "technical support", "support engineer", "assessment engineer", "devtools", "sdk engineer",
        "content platform", "video audio", "voice engineer", "telemedicine", "tenant management",
        "salesforce", "shopify", "localization", "game developer", "technical artist", "automation engineer"
    ]):
        return "backend_systems"

    # 14. Software Engineering (Fullstack / Generalist)
    return "fullstack_general"


def get_role_archetype_definition(role_name: str) -> Dict[str, Any]:
    """
    Retrieves the complete archetype definition for a role, including dimensions, weights, and rationale.
    """
    archetype_id = classify_role_archetype(role_name)
    return ARCHETYPE_REGISTRY.get(archetype_id, ARCHETYPE_REGISTRY["fullstack_general"])


def build_dynamic_role_profile(
    role_name: str,
    raw_profile: Optional[Dict[str, List[str]]] = None,
    experience_years: int = 1,
    is_custom_jd: bool = False
) -> Tuple[Dict[str, List[str]], Dict[str, float], Dict[str, Any]]:
    """
    Constructs a role-calibrated dimension profile, dynamic weights, and archetype metadata.
    Supports experience-tiered benchmarks (Freshers 0-1 yrs evaluated on foundational skills;
    Seniors 5+ yrs on full production architecture) and custom Job Description requirements.
    """
    # 1. Custom Job Description Priority: Evaluate candidate directly against the extracted JD skills
    if is_custom_jd and raw_profile:
        active_dims: Dict[str, List[str]] = {}
        for cat, skills in raw_profile.items():
            clean_skills = [canonicalize_skill(s) for s in skills if s.strip()]
            if clean_skills:
                active_dims[cat] = sorted(list(dict.fromkeys(clean_skills)))

        if active_dims:
            total_dims = len(active_dims)
            weight_per_dim = round(1.0 / total_dims, 2)
            dynamic_weights = {k: weight_per_dim for k in active_dims.keys()}
            diff = round(1.0 - sum(dynamic_weights.values()), 2)
            if diff != 0:
                first_k = list(dynamic_weights.keys())[0]
                dynamic_weights[first_k] = round(dynamic_weights[first_k] + diff, 2)

            label_map = {
                "languages": "Languages",
                "frameworks": "Frameworks",
                "databases": "Databases & Storage",
                "tools": "Tools & Cloud"
            }

            custom_archetype = {
                "id": "custom_job_description",
                "name": "Custom Job Description Benchmark",
                "rationale": f"Qualifications evaluated strictly against the technical skills extracted directly from your custom job description.",
                "omitted_metrics": [],
                "dimensions": {
                    k: {
                        "label": label_map.get(k, k.replace("_", " ").title()),
                        "weight": dynamic_weights[k],
                        "icon": "code" if k == "languages" else "layers" if k == "frameworks" else "database" if k == "databases" else "wrench",
                        "default_skills": active_dims[k]
                    }
                    for k in active_dims.keys()
                }
            }
            return active_dims, dynamic_weights, custom_archetype

    # 2. Standard Role Profile with Archetype Taxonomy
    archetype = get_role_archetype_definition(role_name)
    arch_dimensions = archetype["dimensions"]

    dynamic_profile: Dict[str, List[str]] = {}
    dynamic_weights: Dict[str, float] = {}

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
            assigned = [s for s in flat_skills if s in dim_cfg["default_skills"]]
            if not assigned:
                assigned = [s for s in flat_skills if s.lower() in [d.lower() for d in dim_cfg["default_skills"]]]
            if not assigned:
                assigned = dim_cfg["default_skills"]
            dynamic_profile[dim_key] = list(dict.fromkeys(assigned))
        else:
            dynamic_profile[dim_key] = list(dict.fromkeys(dim_cfg["default_skills"]))

    # 3. Experience-Tier Calibration:
    # If candidate is a Fresher (<= 1 year), benchmark against core foundational skills (top 2 per dimension)
    if experience_years <= 1:
        for dim_key in dynamic_profile:
            skills = dynamic_profile[dim_key]
            if len(skills) > 2:
                dynamic_profile[dim_key] = skills[:2]

    return dynamic_profile, dynamic_weights, archetype
