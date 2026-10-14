import os
import yaml
import json
import re

ROLES_DIR = r"e:\Moving\Desktop\SkillBridge\skills\roles"
OUTPUT_PROFILES_JSON = r"e:\Moving\Desktop\SkillBridge\project\backend\role_profiles_465.json"

# Common technology dictionaries for categorization
KNOWN_LANGUAGES = {
    "python", "javascript", "typescript", "golang", "go", "java", "c++", "c", "c#", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "solidity", "r", "bash", "shell", "sql",
    "html", "css", "dart", "elixir", "haskell", "clojure", "perl", "lua"
}

KNOWN_DATABASES = {
    "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
    "cassandra", "dynamodb", "snowflake", "bigquery", "pinecone", "chromadb", "milvus",
    "weaviate", "qdrant", "neo4j", "oracle", "mssql", "mariadb", "couchdb", "cockroachdb"
}

KNOWN_FRAMEWORKS = {
    "react", "next.js", "nextjs", "vue", "angular", "fastapi", "flask", "django", "express",
    "node.js", "nodejs", "pytorch", "tensorflow", "keras", "scikit-learn", "langchain",
    "llamaindex", "hugging face", "huggingface", "spring", "spring boot", "rails", "ruby on rails",
    "laravel", "asp.net", "dotnet", ".net", "flutter", "react native", "tailwind", "tailwind css",
    "bootstrap", "redux", "graphql", "grpc", "pandas", "numpy", "opencv", "spark", "dbt"
}

KNOWN_TOOLS = {
    "docker", "kubernetes", "k8s", "git", "github", "gitlab", "terraform", "ansible",
    "aws", "amazon web services", "azure", "gcp", "google cloud", "linux", "jenkins",
    "github actions", "prometheus", "grafana", "datadog", "postman", "figma", "jira",
    "confluence", "linear", "airflow", "kafka", "rabbitmq", "celery", "sentry", "trivy"
}

roles = sorted([d for d in os.listdir(ROLES_DIR) if os.path.isdir(os.path.join(ROLES_DIR, d))])
print(f"Processing {len(roles)} roles...")

role_profiles = {}

for role_slug in roles:
    role_title = role_slug.replace("-", " ").title()
    sdir = os.path.join(ROLES_DIR, role_slug, "skills")
    
    languages = set()
    frameworks = set()
    databases = set()
    tools = set()
    raw_skills = set()
    objectives = []
    
    if os.path.exists(sdir):
        for fname in os.listdir(sdir):
            if not fname.endswith(".yaml"):
                continue
            fpath = os.path.join(sdir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as fp:
                    data = yaml.safe_load(fp)
                    if not isinstance(data, dict):
                        continue
                    
                    # Skill name & title
                    sname = data.get("name", fname.replace(".yaml", ""))
                    if not sname.endswith("strict-reviewer"):
                        raw_skills.add(sname.replace("-", " ").title())
                    
                    obj = data.get("objective")
                    if obj and len(objectives) < 2:
                        objectives.append(obj)
                    
                    # Inspect tools
                    tools_field = data.get("tools", {})
                    if isinstance(tools_field, dict):
                        for k, v in tools_field.items():
                            if isinstance(v, list):
                                for item in v:
                                    tname = item.get("name", "") if isinstance(item, dict) else str(item)
                                    words = re.findall(r'[a-zA-Z0-9#\+\.-]+', tname)
                                    for w in words:
                                        wl = w.lower()
                                        if wl in KNOWN_LANGUAGES:
                                            languages.add(w.title() if wl != "sql" else "SQL")
                                        elif wl in KNOWN_FRAMEWORKS:
                                            frameworks.add(w)
                                        elif wl in KNOWN_DATABASES:
                                            databases.add(w)
                                        elif wl in KNOWN_TOOLS:
                                            tools.add(w)
            except Exception:
                pass

    # Provide sensible domain baselines if empty
    r_lower = role_slug.lower()
    if any(k in r_lower for k in ["python", "data", "ai", "machine-learning", "analyst", "vision"]):
        languages.add("Python")
        languages.add("SQL")
    if any(k in r_lower for k in ["frontend", "react", "web", "ui", "javascript", "fullstack"]):
        languages.add("TypeScript")
        languages.add("JavaScript")
        frameworks.add("React")
        frameworks.add("Next.js")
    if any(k in r_lower for k in ["go-", "golang"]):
        languages.add("Go")
    if any(k in r_lower for k in ["rust-"]):
        languages.add("Rust")
    if any(k in r_lower for k in ["java-"]):
        languages.add("Java")
    if any(k in r_lower for k in ["devops", "cloud", "sre", "infrastructure", "systems"]):
        languages.add("Bash")
        tools.add("Docker")
        tools.add("Linux")
        tools.add("Git")

    # Default fallbacks
    if not languages:
        languages.add("Python" if "engineer" in r_lower or "developer" in r_lower else "SQL")
    if not databases:
        databases.add("PostgreSQL")
    if not tools:
        tools.add("Git")
        tools.add("Docker")
    if not frameworks:
        frameworks.add("FastAPI" if "backend" in r_lower or "api" in r_lower else "Pandas")

    role_profiles[role_title] = {
        "slug": role_slug,
        "name": role_title,
        "skills_count": len(raw_skills),
        "raw_skills": sorted(list(raw_skills)),
        "categories": {
            "languages": sorted(list(languages)),
            "frameworks": sorted(list(frameworks)),
            "databases": sorted(list(databases)),
            "tools": sorted(list(tools))
        },
        "objectives": objectives
    }

with open(OUTPUT_PROFILES_JSON, "w", encoding="utf-8") as f:
    json.dump(role_profiles, f, indent=2)

print(f"Exported {len(role_profiles)} role profiles to {OUTPUT_PROFILES_JSON}")
