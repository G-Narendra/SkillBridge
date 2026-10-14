import os
import json
import re

ROLES_JSON_PATH = r"e:\Moving\Desktop\SkillBridge\outputs\all_roles_skills.json"
OUTPUT_WORKSPACE_PATH = r"e:\Moving\Desktop\SkillBridge\outputs\million_dollar_400_role_perspectives.md"
OUTPUT_ARTIFACT_PATH = r"C:\Users\naren\.gemini\antigravity-ide\brain\8b7bb640-309a-4bbb-a58c-13e62f47be41\million_dollar_400_role_perspectives.md"

with open(ROLES_JSON_PATH, "r", encoding="utf-8") as f:
    roles_dict = json.load(f)

# Helper to classify roles into 12 strategic pillars
def get_category(role_name: str) -> str:
    r = role_name.lower()
    if any(k in r for k in ["ai-", "llm-", "machine-learning", "rag-", "nlp-", "prompt-", "data-labeling", "dataset-", "vector-", "computer-vision", "r-d-scientist", "deep-researcher", "research-scientist"]):
        return "1. AI, Machine Learning, Data Science & Analytics"
    elif any(k in r for k in ["data-", "analytics-", "database-", "sql-"]):
        return "1. AI, Machine Learning, Data Science & Analytics"
    elif any(k in r for k in ["backend-", "api-", "system", "software-", "go-", "python", "rust-", "java-", "ruby", "php", "dotnet", "csharp", "swift", "embedded-", "firmware", "hardware", "biomedical", "mechanical", "electrical"]):
        return "2. Software Engineering, Systems & Core Architecture"
    elif any(k in r for k in ["frontend-", "mobile-", "ios-", "android-", "react", "web-", "javascript", "game-", "level-", "narrative-"]):
        return "3. Frontend, Mobile & Client-Side Experiences"
    elif any(k in r for k in ["devops-", "cloud-", "kubernetes-", "infrastructure-", "network-", "platform-", "linux-", "it-", "telecommunications", "wireless"]):
        return "4. DevOps, Cloud & Platform Infrastructure"
    elif any(k in r for k in ["security-", "devsecops-", "penetration-", "ethical-hacker", "compliance-", "privacy-", "gdpr", "infosec-", "risk-", "fraud-", "trust-safety", "trade-compliance", "regulatory-"]):
        return "5. Cybersecurity, Risk & Compliance"
    elif any(k in r for k in ["qa-", "test", "sre-", "site-reliability", "chaos-", "incident-", "monitoring-", "reliability-", "performance-engineer", "web-performance"]):
        return "6. Reliability, Quality Assurance & Chaos Engineering"
    elif any(k in r for k in ["product-", "cpo", "ux-", "ui-", "interaction-", "design-", "visual-", "graphic-", "animator", "motion-", "prototyping-", "onboarding-", "information-architect", "cli-ux", "accessibility-"]):
        return "7. Product Management, UX & Industrial Design"
    elif any(k in r for k in ["technical-writer", "documentation-", "developer-advocate", "developer-relations", "content-", "copywriter", "copy-editor", "curriculum-", "instructional-", "training-", "mentor-", "writer"]):
        return "8. Developer Relations, Content & Education"
    elif any(k in r for k in ["recruiter", "talent-", "recruiting-", "hr-", "head-of-people", "global-hr", "diversity-", "payroll-", "succession-"]):
        return "9. Talent Acquisition, Recruiting & People Operations"
    elif any(k in r for k in ["sales-", "account-executive", "b2b-", "enterprise-", "customer-success", "customer-support", "customer-onboarding", "customer-experience", "partnership-", "partner-", "channel-", "business-development", "key-account"]):
        return "10. Sales, Enterprise Go-To-Market & Partnerships"
    elif any(k in r for k in ["marketing-", "cmo", "growth-", "seo-", "conversion-", "brand-", "media-buyer", "pr-", "public-relations", "social-media", "influencer-", "event-", "inbound-", "demand-", "affiliate-", "referral-", "user-acquisition", "retention-"]):
        return "11. Marketing, Growth & Brand Strategy"
    else:
        return "12. Executive Leadership, Finance, Legal, Operations & Strategy"

# Group roles
grouped = {}
for role_name, skills in sorted(roles_dict.items()):
    cat = get_category(role_name)
    grouped.setdefault(cat, []).append((role_name, skills))

print("Grouped counts:")
for cat, items in sorted(grouped.items()):
    print(f"  {cat}: {len(items)} roles")

with open(ROLES_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(roles_dict, f, indent=2)

print("Setup verified successfully.")
