import os
import json
import logging
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv
try:
    from thefuzz import fuzz, process
except ImportError:
    fuzz = None
    process = None
from blueprint_generator import generate_production_blueprint_files

load_dotenv()
logger = logging.getLogger("skillbridge.analyzer")

ROLE_PROFILES: Dict[str, Dict[str, List[str]]] = {
    "Data Analyst": {
        "languages": ["Python", "SQL", "R"],
        "frameworks": ["Pandas", "NumPy", "Scikit-learn"],
        "databases": ["PostgreSQL", "Snowflake", "BigQuery"],
        "tools": ["Tableau", "Power BI", "dbt", "Git"]
    },
    "Backend Engineer": {
        "languages": ["Python", "Go", "Java", "SQL"],
        "frameworks": ["FastAPI", "Django", "Express", "Node.js"],
        "databases": ["PostgreSQL", "Redis", "MongoDB"],
        "tools": ["Docker", "Kubernetes", "Git", "AWS"]
    },
    "Machine Learning Engineer": {
        "languages": ["Python", "C++", "SQL"],
        "frameworks": ["PyTorch", "TensorFlow", "Scikit-learn", "FastAPI"],
        "databases": ["PostgreSQL", "Elasticsearch"],
        "tools": ["Docker", "Git", "AWS", "Linux"]
    },
    "AI Engineer": {
        "languages": ["Python", "TypeScript", "SQL"],
        "frameworks": ["PyTorch", "LangChain", "LlamaIndex", "Hugging Face"],
        "databases": ["Pinecone", "ChromaDB", "Milvus", "PostgreSQL"],
        "tools": ["Docker", "Git", "Linux", "AWS"]
    },
    "Frontend Engineer": {
        "languages": ["TypeScript", "JavaScript", "HTML", "CSS"],
        "frameworks": ["React", "Next.js", "Tailwind CSS", "Redux"],
        "databases": ["SQLite"],
        "tools": ["Git", "Vite", "Webpack", "Postman"]
    },
    "Fullstack Engineer": {
        "languages": ["TypeScript", "JavaScript", "Python", "SQL"],
        "frameworks": ["React", "Next.js", "FastAPI", "Node.js"],
        "databases": ["PostgreSQL", "MongoDB", "Redis"],
        "tools": ["Docker", "Git", "GitHub Actions", "AWS"]
    },
    "DevOps Engineer": {
        "languages": ["Python", "Bash", "Go"],
        "frameworks": ["Node.js"],
        "databases": ["Redis", "Elasticsearch"],
        "tools": ["Docker", "Kubernetes", "Terraform", "GitHub Actions", "Ansible", "AWS"]
    },
    "Cloud Architect": {
        "languages": ["Python", "Bash", "Go"],
        "frameworks": ["FastAPI"],
        "databases": ["DynamoDB", "PostgreSQL", "Snowflake"],
        "tools": ["AWS", "Google Cloud", "Azure", "Terraform", "Kubernetes"]
    },
    "Data Engineer": {
        "languages": ["Python", "SQL", "Scala"],
        "frameworks": ["Pandas", "NumPy"],
        "databases": ["PostgreSQL", "Snowflake", "BigQuery", "Redis"],
        "tools": ["Apache Spark", "Apache Airflow", "Apache Kafka", "dbt", "Docker"]
    },
    "Mobile Developer": {
        "languages": ["Swift", "Kotlin", "TypeScript", "JavaScript"],
        "frameworks": ["React", "Node.js"],
        "databases": ["SQLite"],
        "tools": ["Git", "GitHub Actions", "Postman", "Linux"]
    },
    "Security Engineer": {
        "languages": ["Python", "Bash", "Go", "C++"],
        "frameworks": ["FastAPI", "Flask"],
        "databases": ["Elasticsearch", "PostgreSQL"],
        "tools": ["Linux", "Docker", "Git", "Kubernetes"]
    },
    "Systems Engineer": {
        "languages": ["C++", "Rust", "Go", "Bash"],
        "frameworks": ["Node.js"],
        "databases": ["Redis", "SQLite"],
        "tools": ["Linux", "Docker", "Git", "Prometheus"]
    },
    "QA Automation Engineer": {
        "languages": ["Python", "TypeScript", "JavaScript", "Java"],
        "frameworks": ["FastAPI", "Express"],
        "databases": ["PostgreSQL", "MySQL"],
        "tools": ["Postman", "Git", "GitHub Actions", "Docker"]
    },
    "Site Reliability Engineer": {
        "languages": ["Go", "Python", "Bash"],
        "frameworks": ["FastAPI"],
        "databases": ["Redis", "Elasticsearch"],
        "tools": ["Kubernetes", "Terraform", "Prometheus", "Grafana", "Docker", "Linux"]
    },
    "Blockchain Developer": {
        "languages": ["Solidity", "TypeScript", "JavaScript", "Rust"],
        "frameworks": ["Next.js", "React", "Node.js"],
        "databases": ["PostgreSQL", "Redis"],
        "tools": ["Git", "Docker", "Linux", "Postman"]
    },
    "AI Agent Engineer": {
        "languages": ["Python", "TypeScript", "SQL"],
        "frameworks": ["LangChain", "LlamaIndex", "CrewAI", "FastAPI", "AutoGPT"],
        "databases": ["Pinecone", "ChromaDB", "PostgreSQL", "Redis"],
        "tools": ["Docker", "Git", "Linux", "OpenAI API"]
    }
}

# Dynamically integrate all 465+ roles from the comprehensive skill catalog
PROFILES_465_PATH = os.path.join(os.path.dirname(__file__), "role_profiles_465.json")
if os.path.exists(PROFILES_465_PATH):
    try:
        with open(PROFILES_465_PATH, "r", encoding="utf-8") as _fp:
            _loaded_profiles = json.load(_fp)
            for _rname, _rdata in _loaded_profiles.items():
                if "categories" in _rdata and _rdata["categories"]:
                    ROLE_PROFILES[_rname] = _rdata["categories"]
                    # Register normalized variants
                    _clean = _rname.replace("Ai ", "AI ").replace(" Ml", " ML").replace("Api ", "API ")
                    ROLE_PROFILES[_clean] = _rdata["categories"]
            # Ensure AI Agent Engineer variations map cleanly
            if "Ai Agents Engineer" in ROLE_PROFILES and "AI Agent Engineer" not in ROLE_PROFILES:
                ROLE_PROFILES["AI Agent Engineer"] = ROLE_PROFILES["Ai Agents Engineer"]
    except Exception as _e:
        logger.warning(f"Failed to load role_profiles_465.json: {_e}")

WEIGHTS: Dict[str, float] = {
    "languages": 0.40,
    "frameworks": 0.30,
    "databases": 0.20,
    "tools": 0.10
}

def is_skill_present(required_skill: str, candidate_skills: List[str], threshold: int = 85) -> bool:
    """
    Evaluates whether a candidate possesses a required skill using exact and fuzzy matching.
    Protects short skill names from incorrect substring collisions.
    """
    req_lower = required_skill.lower().strip()
    
    # Exact match check
    for cand in candidate_skills:
        cand_lower = cand.lower().strip()
        if req_lower == cand_lower:
            return True

    # Short skill names like R, C, Go, SQL require exact token match
    if len(req_lower) <= 2:
        return False

    for cand in candidate_skills:
        cand_lower = cand.lower().strip()
        # Word boundary or token containment
        if req_lower in cand_lower.split():
            return True
        if cand_lower in req_lower.split():
            return True

    # Fuzzy match using token sort ratio if available
    if process and fuzz and candidate_skills:
        try:
            best = process.extractOne(required_skill, candidate_skills, scorer=fuzz.token_sort_ratio)
            if best and best[1] >= threshold:
                return True
        except Exception:
            pass

    return False

def build_deterministic_blueprints(missing_skills: List[str], role: str) -> List[Dict[str, Any]]:
    """
    Generates two or four complete portfolio project blueprints addressing identified missing skills.
    Includes technical stack, roadmap milestones, and repository starter files.
    """
    blueprints: List[Dict[str, Any]] = []

    # Partition missing skills into thematic tracks
    missing_dbs = [s for s in missing_skills if s in [
        "PostgreSQL", "Snowflake", "BigQuery", "Redis", "MongoDB", "DynamoDB",
        "Elasticsearch", "Pinecone", "Milvus", "ChromaDB", "MySQL", "SQLite"
    ]]
    missing_frameworks = [s for s in missing_skills if s in [
        "Pandas", "NumPy", "Scikit-learn", "PyTorch", "TensorFlow", "FastAPI",
        "Django", "Express", "Node.js", "React", "Next.js", "LangChain",
        "LlamaIndex", "Hugging Face", "Tailwind CSS", "Redux"
    ]]
    missing_tools = [s for s in missing_skills if s in [
        "Tableau", "Power BI", "dbt", "Apache Spark", "Apache Airflow",
        "Apache Kafka", "Docker", "Kubernetes", "Terraform", "GitHub Actions",
        "AWS", "Linux", "Git", "Prometheus", "Grafana"
    ]]
    missing_languages = [s for s in missing_skills if s in [
        "Python", "SQL", "R", "Go", "Java", "TypeScript", "JavaScript",
        "C++", "Rust", "Solidity", "Bash", "Scala"
    ]]

    # Blueprint 1: Core System or Data Pipeline addressing databases and storage
    if missing_dbs or "SQL" in missing_skills or "Snowflake" in missing_skills:
        primary_db = missing_dbs[0] if missing_dbs else "PostgreSQL"
        stack = [primary_db] + [s for s in missing_skills if s != primary_db][:4]
        if len(stack) < 3:
            stack.extend(["Docker", "FastAPI", "SQL"])
        stack = list(dict.fromkeys(stack))

        title = f"Data Pipeline and Analytics Engine with {primary_db}"
        objective = f"Build an automated data ingestion and transformation system using {primary_db} to demonstrate structured schema design and high query performance."
        architecture = f"Event-driven ETL architecture utilizing {primary_db} for storage, containerized with Docker, and exposed through a REST query interface."
        roadmap = [
            f"Milestone 1: Design dimensional schema and configure {primary_db} connection pooling",
            "Milestone 2: Implement batch ingestion pipeline with input data validation",
            "Milestone 3: Develop analytical query endpoints with caching and indexing",
            "Milestone 4: Write automated integration tests and package deployment configuration"
        ]
        starter_readme = f"""# {title}

## Objective
{objective}

## Architecture
{architecture}

## Technical Stack
{chr(10).join(f"- {item}" for item in stack)}

## Roadmap
{chr(10).join(f"{idx+1}. {step}" for idx, step in enumerate(roadmap))}

## Verification
Run integration tests:
```bash
pytest tests/ -v
```
"""
        blueprints.append({
            "title": title,
            "objective": objective,
            "difficulty": "Intermediate",
            "hours": 28,
            "target_skills_covered": [primary_db] + [s for s in missing_skills if s in stack and s != primary_db][:2],
            "tech_stack": stack,
            "architecture_outline": architecture,
            "roadmap": roadmap,
            "starter_files": generate_production_blueprint_files(title, stack, roadmap, role)
        })

    # Blueprint 2: Service layer or Framework application
    if missing_frameworks or missing_languages:
        target_fw = missing_frameworks[0] if missing_frameworks else (missing_languages[0] if missing_languages else "FastAPI")
        stack = [target_fw] + [s for s in missing_skills if s != target_fw][:4]
        if len(stack) < 3:
            stack.extend(["Docker", "PostgreSQL", "Git"])
        stack = list(dict.fromkeys(stack))

        title = f"Production Service Architecture with {target_fw}"
        objective = f"Construct a scalable application demonstrating {target_fw} design patterns, structured error handling, and test suites."
        architecture = f"Layered domain-driven service architecture with controller routing, service boundaries, and persistent data access."
        roadmap = [
            f"Milestone 1: Scaffold {target_fw} project structure and configuration management",
            "Milestone 2: Implement core business logic domain entities and validation",
            "Milestone 3: Build authentication layer and rate limiting middleware",
            "Milestone 4: Establish continuous integration pipeline and Docker packaging"
        ]
        starter_readme = f"""# {title}

## Objective
{objective}

## Architecture
{architecture}

## Technical Stack
{chr(10).join(f"- {item}" for item in stack)}

## Roadmap
{chr(10).join(f"{idx+1}. {step}" for idx, step in enumerate(roadmap))}

## Setup
Install dependencies and launch service:
```bash
docker compose up --build
```
"""
        blueprints.append({
            "title": title,
            "objective": objective,
            "difficulty": "Intermediate",
            "hours": 32,
            "target_skills_covered": [target_fw] + [s for s in missing_skills if s in stack and s != target_fw][:2],
            "tech_stack": stack,
            "architecture_outline": architecture,
            "roadmap": roadmap,
            "starter_files": generate_production_blueprint_files(title, stack, roadmap, role)
        })

    # Blueprint 3: Tooling, Infrastructure, or Analytics Workflow
    if missing_tools or len(blueprints) < 2:
        tool_focus = missing_tools[0] if missing_tools else "Docker"
        stack = [tool_focus] + [s for s in missing_skills if s != tool_focus][:4]
        if len(stack) < 3:
            stack.extend(["Git", "Linux", "Python"])
        stack = list(dict.fromkeys(stack))

        title = f"Automated Workflow and Deployment Engine with {tool_focus}"
        objective = f"Establish an automated deployment and observability pipeline using {tool_focus} to enforce reproducible execution environments."
        architecture = f"Declarative infrastructure automation workflow with validation checks, automated staging deployment, and health monitoring."
        roadmap = [
            f"Milestone 1: Define declarative configuration scripts using {tool_focus}",
            "Milestone 2: Create automated linting and security scanning checks",
            "Milestone 3: Build reproducible staging environment with telemetry",
            "Milestone 4: Document disaster recovery procedures and runtime validation"
        ]
        blueprints.append({
            "title": title,
            "objective": objective,
            "difficulty": "Advanced",
            "hours": 36,
            "target_skills_covered": [tool_focus] + [s for s in missing_skills if s in stack and s != tool_focus][:2],
            "tech_stack": stack,
            "architecture_outline": architecture,
            "roadmap": roadmap,
            "starter_files": generate_production_blueprint_files(title, stack, roadmap, role)
        })

    # Blueprint 4: Advanced Specialization project (if 4 needed)
    if len(missing_skills) >= 4 or len(blueprints) < 2:
        special_focus = missing_skills[-1] if missing_skills else "Python"
        stack = [special_focus] + missing_skills[:3]
        if len(stack) < 3:
            stack.extend(["PostgreSQL", "Docker", "Git"])
        stack = list(dict.fromkeys(stack))

        title = f"End-to-End {role} Verification Platform"
        objective = f"Implement a comprehensive capstone platform combining {special_focus} with foundational tools to demonstrate full professional readiness for the {role} role."
        architecture = "Full lifecycle modular system featuring clean separation of data models, processing handlers, and automated test coverage."
        roadmap = [
            f"Milestone 1: Architect modular system interfaces focusing on {special_focus}",
            "Milestone 2: Implement core processing engine and database persistence",
            "Milestone 3: Create verification test suites with boundary condition checks",
            "Milestone 4: Build automated deployment pipeline and technical documentation"
        ]
        blueprints.append({
            "title": title,
            "objective": objective,
            "difficulty": "Advanced",
            "hours": 40,
            "target_skills_covered": [special_focus] + [s for s in missing_skills if s in stack and s != special_focus][:2],
            "tech_stack": stack,
            "architecture_outline": architecture,
            "roadmap": roadmap,
            "starter_files": generate_production_blueprint_files(title, stack, roadmap, role)
        })

    # Ensure exactly 3 to 4 blueprints returned as mandated by Master Prompt
    if len(blueprints) > 4:
        blueprints = blueprints[:4]
    elif len(blueprints) < 3:
        while len(blueprints) < 3:
            idx = len(blueprints) + 1
            extra_skill = missing_skills[idx % len(missing_skills)] if missing_skills else "Python"
            extra_title = f"{role} Enterprise Architecture Benchmark {idx}"
            extra_stack = list(dict.fromkeys([extra_skill, "FastAPI", "Docker", "PostgreSQL", "Prometheus"]))
            extra_roadmap = [
                f"Milestone 1: Scaffold resilient service foundations with {extra_skill}",
                "Milestone 2: Implement domain logic with input boundary validation",
                "Milestone 3: Construct automated testing suite and error telemetry",
                "Milestone 4: Package containerized environment and CI workflow"
            ]
            blueprints.append({
                "title": extra_title,
                "objective": f"Enterprise architecture implementation targeting production readiness in {role} standards.",
                "difficulty": "Intermediate",
                "hours": 32,
                "target_skills_covered": [extra_skill],
                "tech_stack": extra_stack,
                "architecture_outline": "Production microservice scaffold with separation of concerns and automated testing.",
                "roadmap": extra_roadmap,
                "starter_files": generate_production_blueprint_files(extra_title, extra_stack, extra_roadmap, role)
            })

    return blueprints

def generate_llm_blueprints(missing_skills: List[str], role: str) -> Optional[List[Dict[str, Any]]]:
    """
    Attempts to generate project blueprints using NVIDIA NIM Llama-3.1 API.
    Returns None on failure to trigger deterministic fallback.
    """
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None

    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a technical software architect.
Generate exactly 2 or 4 tailored portfolio projects for a candidate targeting the role '{role}'.
The candidate is missing these specific technical skills: {', '.join(missing_skills)}.

Return a strict JSON object with this exact structure:
{{
  "projects": [
    {{
      "title": "Clear descriptive project title",
      "objective": "Two sentence objective explaining what the system achieves",
      "difficulty": "Intermediate",
      "hours": 30,
      "target_skills_covered": ["Skill1", "Skill2"],
      "tech_stack": ["Tech1", "Tech2", "Tech3", "Tech4"],
      "architecture_outline": "Two sentence architectural summary",
      "roadmap": [
        "Milestone 1: Project setup and initial data contracts",
        "Milestone 2: Core processing logic implementation",
        "Milestone 3: Integration testing and validation",
        "Milestone 4: Deployment packaging and documentation"
      ],
      "starter_files": {{
        "README.md": "# Project Title\\n\\n## Objective\\n...",
        ".gitignore": ".env\\n__pycache__/\\n"
      }}
    }}
  ]
}}
Do not write markdown formatting around the JSON. Return only the raw JSON.
"""

    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [
            {"role": "system", "content": "You output only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2048
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"].strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            data = json.loads(content)
            projects = data.get("projects", [])
            if len(projects) in [2, 4]:
                return projects
    except Exception as e:
        logger.warning(f"LLM blueprint generation failed: {e}. Using deterministic engine.")

    return None

def analyze_gap(candidate_skills: List[str], target_role: str) -> Dict[str, Any]:
    """
    Evaluates candidate skills against the role taxonomy using weighted formula:
    Languages: 40%, Frameworks: 30%, Databases: 20%, Tools: 10%.
    Produces category-specific breakdowns and 2 or 4 project proposals.
    """
    profile = ROLE_PROFILES.get(target_role)
    if not profile:
        # Dynamic fallback profile for custom roles
        profile = {
            "languages": ["Python", "SQL", "TypeScript"],
            "frameworks": ["FastAPI", "React", "Node.js"],
            "databases": ["PostgreSQL", "Redis"],
            "tools": ["Docker", "Git", "Linux", "AWS"]
        }

    category_breakdown: Dict[str, Dict[str, Any]] = {}
    all_matched: List[str] = []
    all_missing: List[str] = []
    weighted_total_score = 0.0

    for category, required_list in profile.items():
        matched_in_cat: List[str] = []
        missing_in_cat: List[str] = []

        for req in required_list:
            if is_skill_present(req, candidate_skills):
                matched_in_cat.append(req)
                all_matched.append(req)
            else:
                missing_in_cat.append(req)
                all_missing.append(req)

        count_total = len(required_list)
        count_matched = len(matched_in_cat)
        cat_pct = round((count_matched / count_total * 100)) if count_total > 0 else 100
        category_weight = WEIGHTS.get(category, 0.25)
        weighted_total_score += (cat_pct * category_weight)

        category_breakdown[category] = {
            "matched": matched_in_cat,
            "missing": missing_in_cat,
            "percentage": cat_pct,
            "total_required": count_total
        }

    overall_match_percentage = min(max(round(weighted_total_score), 0), 100)
    all_matched = sorted(list(set(all_matched)))
    all_missing = sorted(list(set(all_missing)))

    # Mathematical Euclidean Competency Deficit: Delta = sum(w_k * max(0, d_k - s_k))
    # where d_k = 100.0 (full required competency) and s_k = candidate score percentage
    deficit_delta = 0.0
    category_deficits: Dict[str, float] = {}
    euclidean_squared_sum = 0.0

    for category, bdown in category_breakdown.items():
        s_k = float(bdown["percentage"])
        d_k = 100.0
        diff = max(0.0, d_k - s_k)
        w_k = WEIGHTS.get(category, 0.25)
        cat_deficit = round(w_k * diff, 2)
        category_deficits[category] = cat_deficit
        deficit_delta += cat_deficit
        euclidean_squared_sum += (w_k * (diff / 100.0)) ** 2

    euclidean_distance = round((euclidean_squared_sum ** 0.5), 4)
    deficit_delta = round(deficit_delta, 1)

    # Try LLM first, falling back to deterministic generator
    projects = generate_llm_blueprints(all_missing, target_role)
    if not projects:
        projects = build_deterministic_blueprints(all_missing, target_role)

    # Ensure every blueprint contains production-grade multi-file architectures
    for p in projects:
        if not p.get("starter_files") or len(p.get("starter_files", {})) < 5:
            p["starter_files"] = generate_production_blueprint_files(
                p.get("title", f"{target_role} Architecture Platform"),
                p.get("tech_stack", []),
                p.get("roadmap", []),
                target_role
            )

    # Multi-role comparative analysis across adjacent engineering roles
    related_roles = [r for r in ["Data Analyst", "AI Engineer", "Backend Engineer", "Fullstack Engineer", "Data Engineer", "Machine Learning Engineer"] if r != target_role][:4]
    multi_role_benchmarks = []
    for other_role in related_roles:
        other_profile = ROLE_PROFILES.get(other_role, {})
        other_score = 0.0
        other_matched = []
        other_missing = []
        for cat, reqs in other_profile.items():
            matched_count = 0
            for r in reqs:
                if is_skill_present(r, candidate_skills):
                    matched_count += 1
                    other_matched.append(r)
                else:
                    other_missing.append(r)
            if reqs:
                other_score += (matched_count / len(reqs) * 100) * WEIGHTS.get(cat, 0.25)
        multi_role_benchmarks.append({
            "role": other_role,
            "match_percentage": min(max(round(other_score), 0), 100),
            "top_matched": other_matched[:3],
            "top_missing": other_missing[:3]
        })

    return {
        "target_role": target_role,
        "match_percentage": overall_match_percentage,
        "competency_deficit_delta": deficit_delta,
        "category_deficits": category_deficits,
        "euclidean_distance": euclidean_distance,
        "deficit_formula": "Delta = sum(w_k * max(0, d_k - s_k))",
        "matched_skills": all_matched,
        "missing_skills": all_missing,
        "category_breakdown": category_breakdown,
        "multi_role_benchmarks": multi_role_benchmarks,
        "projects": projects
    }
