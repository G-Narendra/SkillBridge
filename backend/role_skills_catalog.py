"""
SkillBridge AI - Curated Technical & Non-Technical Role Taxonomy.
Defines industry-standard technical stacks and professional/soft competencies
for all core IT and Engineering disciplines across experience tiers.
"""

from typing import Dict, List, Any

# Standardized Non-Technical Competency Framework
NON_TECH_COMPETENCY_DEFINITIONS = {
    "system_design": {
        "name": "System Design & Tradeoff Analysis",
        "description": "Ability to evaluate scalability bottlenecks, partition strategies, CAP theorem tradeoffs, and caching patterns.",
        "eval_criteria": "Clear Architecture Decision Records (ADRs), sequence diagrams, and capacity modeling."
    },
    "code_review_hygiene": {
        "name": "Code Review & Git Hygiene",
        "description": "Conducting constructive code reviews, enforcing modularity, atomic git commits, and semantic versioning.",
        "eval_criteria": "Descriptive PR descriptions, conventional commits, and automated lint/test validation."
    },
    "agile_delivery": {
        "name": "Agile Iteration & Milestone Delivery",
        "description": "Decomposing complex requirements into user stories, estimating effort, and executing iterative sprints.",
        "eval_criteria": "Phased implementation roadmaps, DoD (Definition of Done), and issue tracking."
    },
    "technical_writing": {
        "name": "Technical Documentation & RFCs",
        "description": "Authoring structured technical specifications, onboarding guides, API docs, and runbooks.",
        "eval_criteria": "Clear OpenAPI/Swagger specs, reproducible README instructions, and post-mortem analysis."
    },
    "incident_response": {
        "name": "Incident Response & Root Cause Analysis",
        "description": "Diagnosing production outages, tracking SLA/SLO violations, and formulating 5-Whys post-mortems.",
        "eval_criteria": "Structured logging, synthetic health probes, alert runbooks, and failure mitigation plans."
    },
    "security_compliance": {
        "name": "Security Mindset & Data Governance",
        "description": "Enforcing principle of least privilege, input sanitization, secret management, and compliance standards.",
        "eval_criteria": "Zero hardcoded secrets (.env.example), non-root Docker execution, and OWASP Top 10 defenses."
    },
    "stakeholder_collaboration": {
        "name": "Cross-Functional Collaboration & Mentorship",
        "description": "Translating business needs into engineering constraints and mentoring junior team members.",
        "eval_criteria": "Clear business context in project summaries and constructive feedback loops."
    }
}


# Curated IT & Technical Role Registry with Tech & Non-Tech Stacks
TECH_ROLES_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "Marketplace Engineer": {
        "discipline": "marketplace_systems",
        "archetype": "marketplace_systems",
        "description": "Designs and implements two-sided supply/demand matching engines, dynamic surge pricing models, multi-party escrow ledgers, and marketplace fraud defenses.",
        "technical_stack": {
            "languages": ["Python", "Go", "SQL"],
            "frameworks": ["FastAPI", "Pandas"],
            "databases": ["Redis", "PostgreSQL"],
            "tools": ["Docker", "Apache Kafka", "Git", "pytest"]
        },
        "non_technical_competencies": [
            "Two-Sided Marketplace Liquidity & Cold-Start Strategy",
            "Geospatial Indexing & Bipartite Matching Tradeoffs",
            "Multi-Party Financial Escrow & Double-Entry Accounting",
            "Trust, Reputation & Anti-Disintermediation Fraud Prevention"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Bipartite matching syntax, Redis geospatial queries, basic CRUD APIs, SQL models"},
            "mid_level": {"target_score": 80, "focus": "Dynamic surge pricing, double-entry ledger transactions, Stripe Connect webhooks, Kafka streaming"},
            "senior": {"target_score": 85, "focus": "Uber/DoorDash scale H3 dispatching, market-clearing auction equilibrium, distributed fault tolerance"}
        }
    },
    "Backend Engineer": {
        "discipline": "backend_systems",
        "archetype": "backend_systems",
        "description": "Designs, implements, and maintains scalable server-side systems, microservices, databases, and APIs.",
        "technical_stack": {
            "languages": ["Python", "SQL", "Go", "Java", "TypeScript"],
            "frameworks": ["FastAPI", "Django", "Express", "Spring Boot", "Node.js"],
            "databases": ["PostgreSQL", "Redis", "MongoDB", "MySQL", "Elasticsearch"],
            "tools": ["Docker", "Git", "Linux", "Kubernetes", "Postman", "pytest"]
        },
        "non_technical_competencies": [
            "System Design & Tradeoff Analysis",
            "Code Review & Git Hygiene",
            "Technical Documentation & RFCs",
            "Security Mindset & Data Governance"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Clean OOP/Procedural syntax, CRUD APIs, unit testing, SQL queries"},
            "mid_level": {"target_score": 80, "focus": "Layered architecture, connection pooling, Redis caching, Docker, CI/CD"},
            "senior": {"target_score": 85, "focus": "Distributed consensus, horizontal scaling, partition sharding, disaster recovery"}
        }
    },
    "Frontend Engineer": {
        "discipline": "frontend_ui",
        "archetype": "frontend_ui",
        "description": "Constructs responsive, high-performance, and accessible user interfaces and web applications.",
        "technical_stack": {
            "languages": ["TypeScript", "JavaScript", "HTML", "CSS"],
            "frameworks": ["React", "Next.js", "Vue", "Redux Toolkit", "Tailwind CSS"],
            "databases": ["LocalStorage", "IndexedDB", "Supabase", "Firebase"],
            "tools": ["Git", "Vite", "Webpack", "Figma", "Jest", "Playwright", "Postman"]
        },
        "non_technical_competencies": [
            "User Experience Empathy & Accessibility (WCAG)",
            "Code Review & Git Hygiene",
            "Design System Alignment & Token Governance",
            "Cross-Functional Collaboration & Mentorship"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Semantic HTML, responsive CSS Grid/Flexbox, React state/props, unit tests"},
            "mid_level": {"target_score": 80, "focus": "Next.js App Router, global state management, client caching, performance audits"},
            "senior": {"target_score": 85, "focus": "Micro-frontends, core web vitals optimization, enterprise design systems"}
        }
    },
    "Fullstack Engineer": {
        "discipline": "fullstack_general",
        "archetype": "fullstack_general",
        "description": "Bridges frontend client experiences with robust backend persistence, business logic, and deployment.",
        "technical_stack": {
            "languages": ["TypeScript", "JavaScript", "Python", "SQL"],
            "frameworks": ["React", "Next.js", "FastAPI", "Node.js", "Express", "Tailwind CSS"],
            "databases": ["PostgreSQL", "Redis", "MongoDB", "SQLite"],
            "tools": ["Docker", "Git", "GitHub Actions", "AWS", "Linux", "Postman", "pytest"]
        },
        "non_technical_competencies": [
            "System Design & Tradeoff Analysis",
            "Agile Iteration & Milestone Delivery",
            "Technical Documentation & RFCs",
            "Security Mindset & Data Governance"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "End-to-end CRUD application, basic JWT auth, database migrations, git"},
            "mid_level": {"target_score": 80, "focus": "Fullstack Next.js + FastAPI, Redis cache, automated CI/CD pipeline, Docker"},
            "senior": {"target_score": 85, "focus": "Decoupled architecture, multi-tenant RBAC, performance profiling, high availability"}
        }
    },
    "Data Analyst": {
        "discipline": "data_analytics",
        "archetype": "data_analytics",
        "description": "Transforms raw operational data into actionable business intelligence, KPI dashboards, and statistical models.",
        "technical_stack": {
            "languages": ["SQL", "Python", "R", "DAX"],
            "frameworks": ["Pandas", "NumPy", "Scikit-learn", "Matplotlib", "Seaborn"],
            "databases": ["Snowflake", "BigQuery", "PostgreSQL", "dbt", "MySQL"],
            "tools": ["Tableau", "Power BI", "Excel", "Git", "Jupyter", "Airflow"]
        },
        "non_technical_competencies": [
            "Executive Visual Storytelling & KPI Definition",
            "Business Domain Translation & Metric Defense",
            "Data Quality Governance & Validation",
            "Cross-Functional Stakeholder Communication & Mentorship"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Complex SQL joins, window functions, Pandas data wrangling, clean dashboard charts"},
            "mid_level": {"target_score": 80, "focus": "Cohort retention modeling, dbt transformations, automated data validation pipelines"},
            "senior": {"target_score": 85, "focus": "Predictive forecasting engines, enterprise data warehouse star schemas, executive presentations"}
        }
    },
    "Data Engineer": {
        "discipline": "data_engineering",
        "archetype": "data_engineering",
        "description": "Builds high-throughput batch and streaming data pipelines, lakehouses, and distributed ETL platforms.",
        "technical_stack": {
            "languages": ["Python", "SQL", "Scala", "Java", "Bash"],
            "frameworks": ["Apache Spark", "Apache Kafka", "dbt", "Pandas"],
            "databases": ["Snowflake", "BigQuery", "PostgreSQL", "Redis", "Cassandra", "Delta Lake"],
            "tools": ["Apache Airflow", "Docker", "Kubernetes", "Git", "AWS", "Terraform"]
        },
        "non_technical_competencies": [
            "System Design & Tradeoff Analysis",
            "Data Quality Governance & Validation",
            "Incident Response & Root Cause Analysis",
            "Technical Documentation & RFCs"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "SQL transformations, Python ETL scripts, basic Airflow DAGs, schema definitions"},
            "mid_level": {"target_score": 80, "focus": "Distributed Spark processing, Kafka streaming, automated schema drift detection"},
            "senior": {"target_score": 85, "focus": "Multi-terabyte lakehouse architectures, zero-data-loss recovery, FinOps query optimization"}
        }
    },
    "DevOps Engineer": {
        "discipline": "devops_platform",
        "archetype": "devops_platform",
        "description": "Automates cloud infrastructure provisioning, container orchestration, CI/CD delivery pipelines, and observability.",
        "technical_stack": {
            "languages": ["Bash", "Python", "Go", "YAML"],
            "frameworks": ["FastAPI"],
            "databases": ["Redis", "Elasticsearch", "PostgreSQL"],
            "tools": ["Terraform", "Docker", "Kubernetes", "Helm", "GitHub Actions", "AWS", "Linux", "Prometheus", "Grafana", "Ansible"]
        },
        "non_technical_competencies": [
            "Incident Response & Root Cause Analysis",
            "Security Mindset & Data Governance",
            "Technical Documentation & RFCs",
            "System Design & Tradeoff Analysis"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Docker multi-stage builds, basic GitHub Actions CI, Linux administration, Bash scripts"},
            "mid_level": {"target_score": 80, "focus": "Terraform modular IaC, Kubernetes ingress/probes, Prometheus alerting, staging/prod isolation"},
            "senior": {"target_score": 85, "focus": "GitOps with ArgoCD, zero-downtime canary rollouts, multi-cloud disaster recovery, IAM Zero-Trust"}
        }
    },
    "Site Reliability Engineer": {
        "discipline": "devops_platform",
        "archetype": "devops_platform",
        "description": "Applies software engineering principles to infrastructure and operations to ensure high reliability and uptime.",
        "technical_stack": {
            "languages": ["Go", "Python", "Bash", "SQL"],
            "frameworks": ["FastAPI"],
            "databases": ["Redis", "Elasticsearch", "TimescaleDB"],
            "tools": ["Kubernetes", "Terraform", "Prometheus", "Grafana", "Datadog", "Docker", "Linux", "Git", "Sentry"]
        },
        "non_technical_competencies": [
            "Incident Response & Root Cause Analysis",
            "System Design & Tradeoff Analysis",
            "Technical Writing & Post-Mortem Documentation",
            "Security Mindset & Data Governance"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Linux performance tools (top, iostat), Docker healthchecks, Prometheus scrape configs"},
            "mid_level": {"target_score": 80, "focus": "SLO/SLI error budget monitoring, automated circuit breakers, synthetic probe suites"},
            "senior": {"target_score": 85, "focus": "Chaos engineering (Chaos Mesh), automated self-healing clusters, multi-region active-active failover"}
        }
    },
    "Machine Learning Engineer": {
        "discipline": "ml_engineering",
        "archetype": "ml_engineering",
        "description": "Designs, trains, and operationalizes predictive machine learning and deep learning models at scale.",
        "technical_stack": {
            "languages": ["Python", "C++", "SQL", "CUDA"],
            "frameworks": ["PyTorch", "TensorFlow", "Scikit-learn", "Hugging Face", "Keras"],
            "databases": ["PostgreSQL", "Redis", "Elasticsearch", "Pinecone"],
            "tools": ["Docker", "MLflow", "FastAPI", "Git", "Linux", "Weights & Biases", "Jupyter"]
        },
        "non_technical_competencies": [
            "System Design & Tradeoff Analysis",
            "Data Quality Governance & Validation",
            "Technical Documentation & RFCs",
            "Code Review & Git Hygiene"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Supervised learning models, train/test validation, feature scaling, model metrics (ROC-AUC, F1)"},
            "mid_level": {"target_score": 80, "focus": "Deep learning architectures (CNN/Transformers), FastAPI model serving, Docker, MLflow tracking"},
            "senior": {"target_score": 85, "focus": "Distributed model training (DDP), TensorRT quantization, real-time feature stores, drift monitoring"}
        }
    },
    "AI Agent Engineer": {
        "discipline": "ai_agents",
        "archetype": "ai_agents",
        "description": "Builds autonomous cognitive AI agents, multi-agent tool execution platforms, and dense RAG retrieval systems.",
        "technical_stack": {
            "languages": ["Python", "TypeScript", "SQL"],
            "frameworks": ["LangChain", "LlamaIndex", "CrewAI", "FastAPI", "AutoGPT"],
            "databases": ["Pinecone", "ChromaDB", "Milvus", "PostgreSQL", "Redis"],
            "tools": ["Docker", "Git", "Linux", "OpenAI API", "Hugging Face", "Postman"]
        },
        "non_technical_competencies": [
            "System Design & Tradeoff Analysis",
            "Security Mindset & Prompt Injection Defense",
            "Technical Documentation & RFCs",
            "Agile Iteration & Milestone Delivery"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Prompt engineering, function calling, basic OpenAI API integrations, chunking & embeddings"},
            "mid_level": {"target_score": 80, "focus": "Hybrid RAG (BM25 + Dense vector search), multi-tool agent execution, semantic caching"},
            "senior": {"target_score": 85, "focus": "Hierarchical multi-agent supervisor systems, self-healing reflection loops, evaluation harnesses (Ragas)"}
        }
    },
    "Security Engineer": {
        "discipline": "security_cyber",
        "archetype": "security_cyber",
        "description": "Protects digital assets through vulnerability assessments, penetration testing, threat modeling, and defensive hardening.",
        "technical_stack": {
            "languages": ["Python", "Bash", "Go", "C++"],
            "frameworks": ["FastAPI", "Flask"],
            "databases": ["Elasticsearch", "PostgreSQL"],
            "tools": ["Linux", "Docker", "Git", "Kubernetes", "Wireshark", "Burp Suite", "Trivy", "Nmap"]
        },
        "non_technical_competencies": [
            "Security Mindset & Threat Modeling (STRIDE)",
            "Incident Response & Root Cause Analysis",
            "Technical Documentation & Security Runbooks",
            "Code Review & Vulnerability Triage"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "OWASP Top 10 vulnerabilities, secure coding practices, port scanning, network protocols"},
            "mid_level": {"target_score": 80, "focus": "Automated SAST/DAST CI/CD integration, container vulnerability audits, OAuth2/JWT security"},
            "senior": {"target_score": 85, "focus": "Zero-Trust enterprise architecture, automated red-teaming harnesses, SOC2 compliance governance"}
        }
    },
    "Ethical Hacker": {
        "discipline": "security_cyber",
        "archetype": "security_cyber",
        "description": "Performs offensive penetration testing, red teaming, exploit analysis, vulnerability assessments, and security hardening to discover and eliminate system weaknesses.",
        "technical_stack": {
            "languages": ["Python", "Bash", "Go", "C"],
            "frameworks": ["Burp Suite", "Metasploit", "OWASP Top 10", "Scapy"],
            "databases": ["Redis"],
            "tools": ["Nmap", "Wireshark", "Linux", "Docker", "Git", "Kali Linux"]
        },
        "non_technical_competencies": [
            "Offensive Security Mindset & Kill-Chain Analysis",
            "Responsible Disclosure & Proof-of-Concept Reporting",
            "Technical Due Diligence & Threat Modeling",
            "Root Cause Remediation & Security Advisory"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Network port reconnaissance, OWASP Top 10 web vulnerabilities, SQLi/XSS fuzzing, traffic inspection"},
            "mid_level": {"target_score": 80, "focus": "Automated penetration testing scripts, custom exploit development, lateral movement auditing, WAF evasion"},
            "senior": {"target_score": 85, "focus": "Zero-day vulnerability discovery, advanced red-team C2 orchestration, kernel privilege escalation, enterprise threat emulation"}
        }
    },
    "Cloud Architect": {
        "discipline": "devops_platform",
        "archetype": "devops_platform",
        "description": "Architects resilient, secure, and cost-effective multi-tier cloud platforms and disaster recovery topologies.",
        "technical_stack": {
            "languages": ["Python", "Bash", "Go", "YAML"],
            "frameworks": ["FastAPI"],
            "databases": ["PostgreSQL", "Redis", "DynamoDB", "Snowflake"],
            "tools": ["AWS", "Google Cloud", "Azure", "Terraform", "Kubernetes", "Docker", "Linux", "Git"]
        },
        "non_technical_competencies": [
            "System Design & Tradeoff Analysis",
            "Cloud FinOps & Cost Optimization",
            "Security Mindset & Data Governance",
            "Technical Documentation & RFCs"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Cloud core services (VPC, EC2, S3, RDS), IAM permissions, basic Terraform modules"},
            "mid_level": {"target_score": 80, "focus": "Multi-AZ high availability architectures, serverless event architectures, cost budgeting"},
            "senior": {"target_score": 85, "focus": "Multi-region active-active topology, hybrid cloud connectivity, enterprise FinOps governance"}
        }
    },
    "CTO": {
        "discipline": "tech_leadership_advisory",
        "archetype": "tech_leadership_advisory",
        "description": "Provides executive technology vision, enterprise architecture governance, engineering strategy, and organizational scaling.",
        "technical_stack": {
            "languages": ["System Architecture", "Cloud Strategy"],
            "frameworks": ["Agile Governance", "RFC Processes"],
            "databases": ["Data Governance", "FinOps"],
            "tools": ["AWS", "Security Auditing", "Disaster Recovery", "GitHub"]
        },
        "non_technical_competencies": [
            "Executive Technology Vision & Roadmapping",
            "System Design & Architectural Tradeoff Analysis",
            "Cloud FinOps & Resource Allocation",
            "Engineering Team Scaling & Culture Governance"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 75, "focus": "Technical leadership fundamentals, architecture design patterns, code review standards"},
            "mid_level": {"target_score": 80, "focus": "Cross-team RFC governance, tech debt prioritization, cloud infrastructure cost audits"},
            "senior": {"target_score": 90, "focus": "Enterprise tech vision, multi-year product roadmapping, board-level technical defense"}
        }
    },
    "Mobile Developer": {
        "discipline": "mobile_dev",
        "archetype": "mobile_dev",
        "description": "Constructs native and cross-platform mobile applications, reactive UI layouts, client state persistence, and app store release pipelines.",
        "technical_stack": {
            "languages": ["Swift", "Kotlin", "TypeScript", "JavaScript"],
            "frameworks": ["React Native", "Flutter", "SwiftUI", "Jetpack Compose"],
            "databases": ["SQLite", "Room", "CoreData", "Firebase"],
            "tools": ["Git", "GitHub Actions", "Xcode", "Android Studio", "Fastlane", "Postman"]
        },
        "non_technical_competencies": [
            "Mobile App Lifecycle & Memory Optimization",
            "Offline-First Sync & Conflict Resolution",
            "App Store Guidelines & Release Hygiene",
            "Mobile Analytics, Crash Reporting & User Privacy"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "Clean UI components, basic navigation, REST API integration, local SQLite storage"},
            "mid_level": {"target_score": 80, "focus": "State management (Redux/Combine), background tasks, push notifications, offline caching"},
            "senior": {"target_score": 85, "focus": "Mobile architecture modularity, app launch time profiling, automated Fastlane CI/CD matrix"}
        }
    },
    "Embedded Systems Engineer": {
        "discipline": "embedded_systems",
        "archetype": "embedded_systems",
        "description": "Develops bare-metal firmware, real-time operating system (RTOS) tasks, low-level device drivers, and hardware communication protocols.",
        "technical_stack": {
            "languages": ["C", "C++", "Rust", "Assembly", "Bash"],
            "frameworks": ["FreeRTOS", "Zephyr", "Embedded Linux"],
            "databases": ["SQLite", "EEPROM", "Flash File Systems"],
            "tools": ["Git", "GDB", "Make", "CMake", "Oscilloscope", "Logic Analyzer", "Docker"]
        },
        "non_technical_competencies": [
            "Real-Time Determinism & Safety-Critical Engineering",
            "Hardware-Software Co-Design & Schematic Interpretation",
            "Memory Footprint & Ultra-Low-Power Budgeting",
            "Hardware Telemetry, Logic Analysis & In-Circuit Debugging"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "C syntax, GPIO/UART peripherals, basic interrupt handling, register bit-masking"},
            "mid_level": {"target_score": 80, "focus": "FreeRTOS tasks and queues, SPI/I2C/CAN bus drivers, memory-mapped I/O, DMA transfers"},
            "senior": {"target_score": 85, "focus": "Secure bootloaders with ECDSA, Linux kernel character drivers, hard real-time scheduling"}
        }
    },
    "Blockchain Developer": {
        "discipline": "blockchain_web3",
        "archetype": "blockchain_web3",
        "description": "Designs and audits smart contracts, decentralized finance (DeFi) protocols, cryptographic primitives, and Web3 RPC indexers.",
        "technical_stack": {
            "languages": ["Solidity", "Rust", "TypeScript", "JavaScript"],
            "frameworks": ["Foundry", "Hardhat", "Ethers.js", "Viem", "Next.js"],
            "databases": ["The Graph", "PostgreSQL", "IPFS", "Redis"],
            "tools": ["Git", "Slither", "Docker", "MetaMask", "Linux"]
        },
        "non_technical_competencies": [
            "Smart Contract Security & Reentrancy Defenses",
            "EVM Gas Optimization & Opcode Economics",
            "Decentralized Protocol Governance & Technical RFCs",
            "Cryptographic Key Management & Multi-Sig Custody"
        ],
        "experience_benchmarks": {
            "fresher": {"target_score": 70, "focus": "ERC-20/ERC-721 token standards, Solidity syntax, basic unit tests with Foundry"},
            "mid_level": {"target_score": 80, "focus": "Automated AMM constant product math, Slither static analysis, subgraph event indexing"},
            "senior": {"target_score": 85, "focus": "Cross-chain bridges, account abstraction (ERC-4337), formal verification, MEV resistance"}
        }
    }
}

DISCIPLINE_FLAGSHIP_ROLES: Dict[str, str] = {
    "marketplace_systems": "Marketplace Engineer",
    "backend_systems": "Backend Engineer",
    "frontend_ui": "Frontend Engineer",
    "fullstack_general": "Fullstack Engineer",
    "data_analytics": "Data Analyst",
    "data_engineering": "Data Engineer",
    "devops_platform": "DevOps Engineer",
    "security_cyber": "Security Engineer",
    "ai_agents": "AI Agent Engineer",
    "ml_engineering": "Machine Learning Engineer",
    "mobile_dev": "Mobile Developer",
    "embedded_systems": "Embedded Systems Engineer",
    "blockchain_web3": "Blockchain Developer",
    "tech_leadership_advisory": "CTO"
}


def get_role_taxonomy(role_name: str) -> Dict[str, Any]:
    """Retrieves standard taxonomy metadata for a role, with discipline archetype fallback."""
    if role_name in TECH_ROLES_TAXONOMY:
        return TECH_ROLES_TAXONOMY[role_name]
    
    r_low = role_name.lower().strip()
    for r_k, r_val in TECH_ROLES_TAXONOMY.items():
        if r_k.lower() == r_low or r_k.lower() in r_low or r_low in r_k.lower():
            return r_val
            
    # Discipline-aware fallback for uncataloged technical roles
    try:
        from role_archetype_engine import classify_role_archetype
        discipline = classify_role_archetype(role_name)
        flagship_role = DISCIPLINE_FLAGSHIP_ROLES.get(discipline, "Fullstack Engineer")
        if flagship_role in TECH_ROLES_TAXONOMY:
            base_tax = TECH_ROLES_TAXONOMY[flagship_role]
            return {
                **base_tax,
                "description": f"Engineering role delivering {discipline.replace('_', ' ')} solutions for {role_name}."
            }
    except Exception:
        pass

    return TECH_ROLES_TAXONOMY["Fullstack Engineer"]
