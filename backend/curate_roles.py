import re
import json

CURATED_CANONICAL_ROLES = [
    # 1. AI & Intelligent Systems (ai_agents & ml_engineering)
    "AI Engineer",
    "AI Agent Engineer",
    "AI Architect",
    "AI Product Manager",
    "AI Safety Engineer",
    "AI/ML Engineer",
    "Machine Learning Engineer",
    "MLOps Engineer",
    "Data Scientist",
    "Deep Learning Engineer",
    "Computer Vision Engineer",
    "NLP Engineer",
    "Prompt Engineer",
    "RAG Systems Engineer",
    "Search & Recommendation Engineer",
    "Vector Database Engineer",

    # 2. Data Engineering & Analytics (data_engineering & data_analytics)
    "Data Engineer",
    "Data Architect",
    "Big Data Engineer",
    "Analytics Engineer",
    "Data Analyst",
    "Business Intelligence Engineer",
    "Quantitative Analyst",
    "Product Analyst",
    "Data Governance & Privacy Officer",
    "Database Administrator (DBA)",
    "Database Reliability Engineer",

    # 3. Backend, Distributed Systems & Systems (backend_systems)
    "Backend Engineer",
    "Distributed Systems Engineer",
    "API & Microservices Engineer",
    "Python Backend Engineer",
    "Go Backend Engineer",
    "Java Backend Engineer",
    "Node.js Backend Engineer",
    "Rust Systems Engineer",
    ".NET Backend Engineer",
    "Systems Engineer",
    "QA Automation Engineer",
    "Test Automation Architect",
    "DevTools Engineer",

    # 4. Frontend & Design Systems (frontend_ui)
    "Frontend Engineer",
    "Frontend Architect",
    "React Developer",
    "UI/UX Design Systems Engineer",
    "Product Designer (UI/UX)",
    "Web Performance Engineer",
    "Accessibility Engineer",

    # 5. Fullstack Engineering (fullstack_general)
    "Fullstack Engineer",
    "Software Engineer",
    "Senior Software Engineer",
    "Staff Software Engineer",
    "Integration Engineer",

    # 6. Cloud, DevOps & Platform Engineering (devops_platform)
    "DevOps Engineer",
    "Site Reliability Engineer (SRE)",
    "Cloud Architect",
    "Cloud Infrastructure Engineer",
    "Platform Engineer",
    "Kubernetes Administrator",
    "Linux Systems Administrator",
    "Release & Automation Engineer",
    "Chaos Engineer",

    # 7. Cybersecurity & Ethical Hacking (security_cyber)
    "Ethical Hacker",
    "Security Engineer",
    "Penetration Tester",
    "Cybersecurity Analyst",
    "Application Security Engineer",
    "Cloud Security Architect",
    "DevSecOps Engineer",
    "Incident Response Engineer",
    "Network Security Engineer",

    # 8. Mobile Application Engineering (mobile_dev)
    "Mobile Engineer",
    "iOS Swift Developer",
    "Android Kotlin Developer",
    "React Native Developer",
    "Flutter Mobile Developer",

    # 9. Embedded Systems, Firmware & IoT (embedded_systems)
    "Embedded Systems Engineer",
    "Firmware Engineer",
    "IoT Systems Engineer",
    "Robotics Software Engineer",
    "Real-Time Kernel Engineer",

    # 10. Blockchain & Web3 Protocols (blockchain_web3)
    "Blockchain Developer",
    "Smart Contract Engineer",
    "Web3 Protocol Engineer",
    "Solidity Developer",
    "DeFi Quantitative Architect",

    # 11. Marketplace, Fintech & Platforms (marketplace_systems)
    "Marketplace Systems Engineer",
    "Fintech Systems Engineer",
    "Payments & Ledger Engineer",
    "Dynamic Pricing & Matching Engineer",

    # 12. Technology Leadership & Architecture Strategy (tech_leadership_advisory)
    "Chief Technology Officer (CTO)",
    "VP of Engineering",
    "Head of Engineering",
    "Technical Director",
    "Enterprise Solutions Architect",
    "Technical Lead (Tech Lead)",
    "Technical Program Manager (TPM)"
]

CURATED_CANONICAL_ROLES = sorted(list(dict.fromkeys(CURATED_CANONICAL_ROLES)))
print(f"Total curated canonical roles: {len(CURATED_CANONICAL_ROLES)}")

def classify_test(role_name: str) -> str:
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

if __name__ == "__main__":
    from gap_analyzer import analyze_gap
    from role_archetype_engine import ARCHETYPE_REGISTRY
    
    candidate_skills = ["Python", "Docker", "Git", "SQL", "Linux", "FastAPI"]
    
    print("\n--- CLASSIFYING AND TESTING EVERY ROLE WITH ENHANCED CLASSIFIER ---")
    discipline_counts = {}
    failed_roles = []
    
    for idx, role in enumerate(CURATED_CANONICAL_ROLES, 1):
        arch = classify_test(role)
        discipline_counts[arch] = discipline_counts.get(arch, 0) + 1
        
        try:
            res = analyze_gap(candidate_skills, role, experience_years=1)
            score = res.get("match_percentage")
            dims = res.get("dimensions", [])
            projs = res.get("projects", [])
            
            assert 0 <= score <= 100
            assert len(dims) >= 3
            assert len(projs) == 4
            
            print(f"[{idx:02d}/{len(CURATED_CANONICAL_ROLES)}] PASS: {role:35} -> {arch:25}")
        except Exception as e:
            print(f"[{idx:02d}/{len(CURATED_CANONICAL_ROLES)}] FAIL: {role} -> Error: {e}")
            failed_roles.append((role, str(e)))
            
    print("\n--- ENHANCED DISCIPLINE BREAKDOWN ---")
    for d, c in sorted(discipline_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {d:25}: {c:2} roles")


