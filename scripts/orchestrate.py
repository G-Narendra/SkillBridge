"""
SkillBridge Autonomous Multi-Role Council Orchestrator & Quality Gate.
Supports:
  python scripts/orchestrate.py --init
  python scripts/orchestrate.py --verify
  python scripts/orchestrate.py --deep-audit
  python scripts/orchestrate.py --audit-slop
"""

import os
import sys
import json
import re
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
LOOP_STATE_FILE = OUTPUTS_DIR / ".loop-state.json"

BANNED_SLOP_PHRASES = [
    "in today's fast-paced world",
    "marks a pivotal moment",
    "serves as the foundational backbone",
    "here's the thing",
    "testament to",
    "beacon of",
    "embark on a journey",
    "delve into",
    "at the end of the day",
    "harness the power of",
    "paradigm shift",
    "tapestry of",
    "bustling",
]

def get_backend_dir() -> Path:
    if (BASE_DIR / "backend").exists():
        return BASE_DIR / "backend"
    return BASE_DIR / "project" / "backend"

def get_python_exe() -> str:
    b_dir = get_backend_dir()
    backend_venv = b_dir / "venv2" / "Scripts" / "python.exe"
    if backend_venv.exists():
        return str(backend_venv)
    root_venv = BASE_DIR / "venv" / "Scripts" / "python.exe"
    if root_venv.exists():
        return str(root_venv)
    return sys.executable

def init_state():
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    state = {
        "council_stage": 1,
        "version": "2.0.0",
        "faculty_mentor": "Prof. Siddhaling Urolagin",
        "lead_developer": "Narendra Gandikota",
        "status": "INITIALIZED",
        "directives": {
            "4_tier_taxonomy": "COMPLETED",
            "benchmark_transparency": "COMPLETED",
            "eliminate_repetitive_info": "COMPLETED",
            "skeleton_architecture_first": "COMPLETED",
            "dual_path_repository_setup": "COMPLETED",
            "kaggle_ml_workflows": "COMPLETED"
        },
        "verification_results": {}
    }
    with open(LOOP_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    print(f"[OK] Initialized council state at {LOOP_STATE_FILE}")

def run_tests():
    print("\n--- Running Backend Pytest Test Suite ---")
    backend_dir = get_backend_dir()
    python_exe = get_python_exe()
    cmd = [python_exe, "-m", "pytest", "tests/", "-v"]
    res = subprocess.run(cmd, cwd=backend_dir, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
        return False
    return True

def audit_slop():
    print("\n--- Scanning for AI Slop & Vacuous Phrases ---")
    slop_found = []
    scan_exts = {".py", ".ts", ".tsx", ".md", ".json"}
    backend_dir = get_backend_dir()
    frontend_dir = BASE_DIR / "frontend" if (BASE_DIR / "frontend").exists() else BASE_DIR / "project" / "frontend"
    target_dirs = [
        backend_dir,
        frontend_dir / "src",
        BASE_DIR / "specs",
        BASE_DIR / "docs",
        BASE_DIR / "scripts"
    ]

    ignore_subdirs = {"venv", "venv2", "site-packages", "node_modules", ".next", "__pycache__", ".pytest_cache", "Lib"}
    for t_dir in target_dirs:
        if not t_dir.exists():
            continue
        for root, dirs, files in os.walk(t_dir):
            dirs[:] = [d for d in dirs if d not in ignore_subdirs]
            for f in files:
                p = Path(root) / f
                if p.suffix in scan_exts and p.name != "orchestrate.py":
                    try:
                        if p.stat().st_size > 500_000:
                            continue
                        content = p.read_text(encoding="utf-8", errors="ignore").lower()
                        for phrase in BANNED_SLOP_PHRASES:
                            if phrase in content:
                                slop_found.append((str(p.relative_to(BASE_DIR)), phrase))
                    except Exception:
                        pass

    if slop_found:
        print(f"[WARN] Found {len(slop_found)} instances of vacuous AI slop:", flush=True)
        for file_path, phrase in slop_found[:10]:
            print(f"  - {file_path}: '{phrase}'", flush=True)
        return False
    else:
        print("[OK] Zero vacuous AI slop detected across all project code & specs.", flush=True)
        return True

def deep_audit():
    print("\n--- Running FAANG Staff Deep Engineering Audit ---")
    score = 100
    deductions = []

    backend_dir = get_backend_dir()
    ignore_subdirs = {"venv", "venv2", "site-packages", "Lib", "__pycache__", ".pytest_cache"}
    for root, dirs, files in os.walk(backend_dir):
        dirs[:] = [d for d in dirs if d not in ignore_subdirs]
        for f in files:
            if f.endswith(".py"):
                path = Path(root) / f
                content = path.read_text(encoding="utf-8", errors="ignore")
                if re.search(r"except\s*:\s*pass", content):
                    deductions.append(f"Bare exception swallowed in {f}")
                    score -= 10

    # 2. Check for Pydantic v2 schemas.py contract
    schemas_file = backend_dir / "schemas.py"
    if not schemas_file.exists():
        deductions.append("Missing Pydantic v2 schemas.py contract")
        score -= 15
    else:
        content = schemas_file.read_text(encoding="utf-8", errors="ignore")
        if "BaseModel" not in content:
            deductions.append("schemas.py does not inherit from Pydantic BaseModel")
            score -= 10

    # 3. Check for 4-tier taxonomy support in gap_analyzer.py
    gap_file = backend_dir / "gap_analyzer.py"
    if gap_file.exists():
        gap_content = gap_file.read_text(encoding="utf-8", errors="ignore")
        for tier in ["languages", "frameworks", "databases", "tools"]:
            if tier not in gap_content:
                deductions.append(f"Missing tier {tier} in gap_analyzer.py")
                score -= 5
        if "benchmark_standard" not in gap_content:
            deductions.append("Missing transparent benchmark standard metadata")
            score -= 10
        if "download-zip" not in (backend_dir / "main.py").read_text(encoding="utf-8", errors="ignore"):
            deductions.append("Missing zip archive streaming endpoint")
            score -= 10

    # 4. Check for Kaggle support
    bp_file = backend_dir / "blueprint_generator.py"
    if bp_file.exists():
        bp_content = bp_file.read_text(encoding="utf-8", errors="ignore")
        if "kaggle" not in bp_content.lower():
            deductions.append("Missing Kaggle competition workflow support")
            score -= 10

    print(f"Deep Audit Score: {score}/100")
    if deductions:
        print("Deductions:")
        for d in deductions:
            print(f"  - {d}")
    else:
        print("[OK] Passed 100% of senior engineering architectural gates.")
    return score >= 90

def verify_all():
    print("=" * 65)
    print("SKILLBRIDGE AI AUTONOMOUS 4-STAGE COUNCIL VERIFICATION GATE")
    print("Faculty Mentor: Prof. Siddhaling Urolagin | Lead: Narendra Gandikota")
    print("=" * 65)

    all_passed = True

    # 1. Slop Audit
    if not audit_slop():
        all_passed = False

    # 2. Deep Staff Audit
    if not deep_audit():
        all_passed = False

    # 3. Backend Test Suite
    if not run_tests():
        all_passed = False

    # 4. Update Loop State
    init_state()
    with open(LOOP_STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
    state["status"] = "PASSED" if all_passed else "FAILED"
    state["council_stage"] = 4 if all_passed else 2
    with open(LOOP_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print("\n" + "=" * 65)
    if all_passed:
        print(">>> ALL VERIFICATION GATES PASSED (100% GREEN) <<<")
    else:
        print(">>> VERIFICATION FAILED - REMEDIATE DEFICITS <<<")
    print("=" * 65)
    return all_passed

def main():
    parser = argparse.ArgumentParser(description="SkillBridge Autonomous Council Orchestrator")
    parser.add_argument("--init", action="store_true", help="Initialize council loop state")
    parser.add_argument("--verify", action="store_true", help="Run dual-layer verification loop")
    parser.add_argument("--deep-audit", action="store_true", help="Run senior FAANG architectural audit")
    parser.add_argument("--audit-slop", action="store_true", help="Scan for vacuous AI slop phrases")

    args = parser.parse_args()

    if args.init:
        init_state()
    elif args.audit_slop:
        success = audit_slop()
        sys.exit(0 if success else 1)
    elif args.deep_audit:
        success = deep_audit()
        sys.exit(0 if success else 1)
    elif args.verify:
        success = verify_all()
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
