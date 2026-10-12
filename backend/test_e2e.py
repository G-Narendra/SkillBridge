import os
import requests

BASE_URL = "http://127.0.0.1:8080"
PDF_PATH = r"E:\Moving\Desktop\SkillBridge\CV_Narendra_Gandikota_td_data-analyst.pdf"

def test_full_flow():
    print("=== Step 1: Health Check ===")
    r_health = requests.get(f"{BASE_URL}/api/health")
    assert r_health.status_code == 200, f"Health check failed: {r_health.status_code}"
    print("Health response:", r_health.json())

    print("\n=== Step 2: Role Profiles Check ===")
    r_roles = requests.get(f"{BASE_URL}/api/roles")
    assert r_roles.status_code == 200, f"Roles check failed: {r_roles.status_code}"
    roles = r_roles.json()["roles"]
    assert len(roles) >= 15, f"Expected at least 15 roles, got {len(roles)}"
    print(f"Verified {len(roles)} standard technology roles.")

    print("\n=== Step 3: Parse Resume for Multiple Roles ===")
    test_roles = ["Data Analyst", "AI Engineer", "Backend Engineer", "Fullstack Engineer"]

    for target_role in test_roles:
        with open(PDF_PATH, "rb") as f:
            files = {"file": ("resume.pdf", f, "application/pdf")}
            data = {"target_job": target_role}
            r_parse = requests.post(f"{BASE_URL}/api/resume/parse", files=files, data=data)

        assert r_parse.status_code == 200, f"Parse failed for {target_role}: {r_parse.text}"
        res = r_parse.json()

        print(f"\n--- Role: {target_role} ---")
        print("Candidate email:", res["contacts"]["email"])
        print("Candidate LinkedIn:", res["contacts"]["linkedin"])
        print("Candidate Portfolio:", res["contacts"]["portfolio"])
        print("Detected Experience:", res["experience_years"], "years")
        print("Detected Skills Count:", len(res["detected_skills"]))
        print("Match percentage:", res["match_percentage"], "%")
        print("Category Breakdown percentages:")
        for cat, details in res["category_breakdown"].items():
            print(f"  - {cat}: {details['percentage']}% (Matched: {len(details['matched'])}, Missing: {len(details['missing'])})")

        projects = res["projects"]
        print("Projects recommended:", len(projects))
        assert 2 <= len(projects) <= 4, f"Expected 2 to 4 projects, got {len(projects)}"

        for idx, p in enumerate(projects, 1):
            assert len(p["roadmap"]) == 4, f"Roadmap must have 4 milestones, got {len(p['roadmap'])}"
            assert "README.md" in p["starter_files"], "README.md starter file missing"
            assert ".gitignore" in p["starter_files"], ".gitignore starter file missing"
            print(f"  Project {idx}: {p['title']} ({p['difficulty']} - {p['hours']}h)")

    print("\n=== Step 4: Provision Repository Test (Sandbox Mode) ===")
    sample_project = res["projects"][0]
    prov_payload = {
        "title": sample_project["title"],
        "tech_stack": sample_project["tech_stack"],
        "roadmap": sample_project["roadmap"],
        "starter_files": sample_project["starter_files"],
        "token": "sandbox",
        "provider": "github"
    }
    r_prov = requests.post(f"{BASE_URL}/api/provision", json=prov_payload)
    assert r_prov.status_code == 200, f"Provisioning failed: {r_prov.text}"
    prov_data = r_prov.json()
    print("Provision status:", prov_data["status"])
    print("Repository URL:", prov_data["repo_url"])
    print("Initial commit hash:", prov_data["commit_hash"])
    print("Milestone issues count:", len(prov_data["issues_created"]))
    assert len(prov_data["issues_created"]) == 4, "Must create 4 milestone issues"

    print("\n=== All E2E Integration Checks Passed Successfully ===")

if __name__ == "__main__":
    test_full_flow()
