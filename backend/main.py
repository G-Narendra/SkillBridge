import os
import io
import re
import zipfile
import uuid
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from cv_parser import parse_resume
from gap_analyzer import analyze_gap, ROLE_PROFILES
from github_provisioner import provision_repository

load_dotenv()

app = FastAPI(
    title="SkillBridge AI API",
    description="Transforms static candidate resumes into verifiable code repositories.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class ProvisionRequest(BaseModel):
    title: str = Field(..., description="Project proposal title")
    tech_stack: List[str] = Field(..., description="Technical stack badges")
    roadmap: List[str] = Field(..., description="Step-by-step development roadmap")
    starter_files: Optional[Dict[str, str]] = Field(default=None, description="Starter scaffold files")
    token: Optional[str] = Field(default="default", description="Developer platform personal access token, 'default' for system token, or 'sandbox'")
    provider: Optional[str] = Field(default="github", description="Target platform: github or gitlab")

@app.get("/")
async def root_status():
    """
    SkillBridge AI Backend root endpoint.
    """
    return {
        "status": "healthy",
        "service": "SkillBridge AI Backend",
        "health": "/api/health",
        "docs": "/docs",
        "roles_available": len(ROLE_PROFILES),
        "version": "1.0.0"
    }

@app.get("/health")
@app.get("/api/health")
async def health_check():
    """
    Returns runtime operational status of backend services.
    """
    return {
        "status": "healthy",
        "service": "SkillBridge AI Backend",
        "roles_available": len(ROLE_PROFILES),
        "nvidia_configured": bool(os.getenv("NVIDIA_API_KEY"))
    }

@app.get("/api/roles")
async def get_available_roles():
    """
    Returns standard technology roles supported by the platform.
    """
    roles_list = []
    for role_name, categories in ROLE_PROFILES.items():
        roles_list.append({
            "name": role_name,
            "required_skills_count": sum(len(skills) for skills in categories.values()),
            "categories": categories
        })
    return {"roles": roles_list}

@app.post("/api/resume/parse")
async def parse_and_analyze_resume(
    file: UploadFile = File(..., description="Candidate PDF resume document"),
    target_job: str = Form(..., description="Target job title"),
    job_description: Optional[str] = Form(None, description="Optional custom job requirements or description")
):
    """
    Extracts candidate competencies from PDF resume and benchmarks qualifications against target role.
    Calculates weighted match score and generates tailored project proposals.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported document format. Please upload a PDF file."
        )

    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded PDF file is empty."
            )
        
        parsed_resume = parse_resume(content)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document parsing error: {str(e)}"
        )

    candidate_skills = parsed_resume["skills"]
    gap_result = analyze_gap(candidate_skills, target_job, custom_job_description=job_description)

    session_id = str(uuid.uuid4())

    return {
        "session_id": session_id,
        "contacts": parsed_resume["contacts"],
        "anonymized_snippet": parsed_resume.get("anonymized_snippet", ""),
        "anonymization_audit": parsed_resume.get("anonymization_audit", {}),
        "anonymized_resume": parsed_resume.get("anonymization_audit", {}),
        "experience_years": parsed_resume["experience_years"],
        "detected_skills": candidate_skills,
        "categorized_skills": parsed_resume["categorized_skills"],
        "target_role": target_job,
        "match_percentage": gap_result["match_percentage"],
        "competency_deficit_delta": gap_result.get("competency_deficit_delta", 0.0),
        "category_deficits": gap_result.get("category_deficits", {}),
        "euclidean_distance": gap_result.get("euclidean_distance", 0.0),
        "deficit_formula": gap_result.get("deficit_formula", "Delta = sum(w_k * max(0, d_k - s_k))"),
        "benchmark_standard": gap_result.get("benchmark_standard", {}),
        "competency_gaps": gap_result.get("competency_gaps", []),
        "matched_skills": gap_result["matched_skills"],
        "missing_skills": gap_result["missing_skills"],
        "category_breakdown": gap_result["category_breakdown"],
        "multi_role_benchmarks": gap_result.get("multi_role_benchmarks", []),
        "resume_audit": parsed_resume.get("resume_audit", {}),
        "projects": gap_result["projects"]
    }

@app.get("/api/github/status")
async def github_status_endpoint():
    """
    Returns platform environment GitHub connectivity status and candidate user profile.
    """
    from github_provisioner import get_github_status
    status_data = get_github_status()
    status_data["instant_connect_available"] = bool(status_data.get("valid"))
    status_data["device_flow_available"] = True
    return status_data

@app.post("/api/github/platform/connect")
async def connect_platform_account_endpoint():
    """
    Instantly authorizes the platform-verified GitHub account without requiring user token entry.
    """
    from github_provisioner import get_github_status
    status_data = get_github_status()
    if not status_data.get("valid"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Platform GitHub account is not configured."
        )
    return {
        "valid": True,
        "login": status_data.get("login"),
        "name": status_data.get("name"),
        "avatar_url": status_data.get("avatar_url"),
        "html_url": status_data.get("html_url"),
        "public_repos": status_data.get("public_repos", 0),
        "scopes": status_data.get("scopes", []),
        "source": "platform",
        "raw_token": "default"
    }

class DevicePollRequest(BaseModel):
    device_code: str = Field(..., description="Device authorization code")

@app.post("/api/auth/github/device/init")
async def device_flow_init_endpoint():
    """
    Initiates GitHub Device Authorization flow allowing browser authorization without manual PAT creation.
    """
    from github_provisioner import initiate_github_device_flow
    res = initiate_github_device_flow()
    return res

@app.post("/api/auth/github/device/poll")
async def device_flow_poll_endpoint(request: DevicePollRequest):
    """
    Polls device code status until user approves on github.com/login/device.
    """
    from github_provisioner import poll_github_device_flow
    res = poll_github_device_flow(request.device_code)
    return res

@app.get("/api/auth/github/oauth-url")
async def github_oauth_url_endpoint():
    """
    Returns standard GitHub OAuth authorization URL if OAuth App is configured.
    """
    client_id = os.getenv("GITHUB_CLIENT_ID") or os.getenv("GITHUB_ID")
    if client_id:
        url = f"https://github.com/login/oauth/authorize?client_id={client_id}&scope=repo,read:user"
        return {"configured": True, "url": url}
    return {"configured": False, "url": None}

class ValidateTokenRequest(BaseModel):
    token: str = Field(..., description="Developer platform personal access token, 'default' for system token, or 'sandbox'")

@app.post("/api/github/validate-token")
async def validate_github_token_endpoint(request: ValidateTokenRequest):
    """
    Validates GitHub or GitLab credentials and returns connected user account details.
    """
    from github_provisioner import validate_github_token
    result = validate_github_token(request.token)
    if not result.get("valid"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("error", "Invalid developer credentials.")
        )
    return result

@app.post("/api/provision")
async def provision_repository_endpoint(request: ProvisionRequest):
    """
    Provisions an initialized code repository on GitHub or GitLab containing
    project specification, scaffold files, and milestone issue tickets.
    """
    if not request.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project title is required."
        )

    try:
        result = provision_repository(
            project_title=request.title,
            tech_stack=request.tech_stack,
            roadmap=request.roadmap,
            starter_files=request.starter_files,
            token=request.token or "default",
            provider=request.provider or "github"
        )
        return result
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(val_err)
        )
    except RuntimeError as run_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(run_err)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Repository provisioning failed: {str(e)}"
        )

class DownloadZipRequest(BaseModel):
    title: Optional[str] = None
    starter_files: Optional[Dict[str, str]] = None
    blueprint: Optional[Dict[str, Any]] = None

@app.post("/api/blueprint/download-zip")
async def download_blueprint_zip(request: DownloadZipRequest):
    """
    Packages project skeleton files into an in-memory zip archive for direct local download.
    Provides zero-OAuth manual local setup workflow for students.
    Supports both direct {title, starter_files} and wrapped {blueprint: {...}} payloads.
    """
    files = request.starter_files
    title = request.title
    if request.blueprint:
        files = files or request.blueprint.get("starter_files", {})
        title = title or request.blueprint.get("title", "skillbridge-skeleton")

    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Starter files dictionary cannot be empty."
        )

    clean_slug = re.sub(r'[^a-zA-Z0-9_-]', '-', (title or "project-skeleton").lower()).strip('-') or "project-skeleton"
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path, file_content in files.items():
            normalized_path = f"{clean_slug}/{file_path.lstrip('/')}"
            zip_file.writestr(normalized_path, file_content)

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{clean_slug}-skeleton.zip"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@app.post("/api/webhooks/github")
async def github_webhook_endpoint(request: Request):
    """
    Ingests live GitHub webhook events, evaluating repository AST modularity and CI pass rates.
    """
    from telemetry_service import process_github_webhook
    event_type = request.headers.get("X-GitHub-Event", "push")
    try:
        body = await request.json()
    except Exception:
        body = {}
    return process_github_webhook(event_type, body)

@app.get("/api/portfolio/card/{username}")
async def get_portfolio_card_endpoint(username: str, role: Optional[str] = "Ai Agents Engineer"):
    """
    Returns verified Digital Portfolio Card scannable by technical hiring managers in <15 seconds.
    Features verified badges, AST modularity grades, and CI test pass rates.
    """
    from telemetry_service import synthesize_portfolio_card
    return synthesize_portfolio_card(username=username, target_role=role or "Ai Agents Engineer")

