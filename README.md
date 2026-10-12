# SkillBridge AI platform

SkillBridge AI converts static text resumes into verifiable code repositories. The platform analyzes candidate qualifications against specific job descriptions, identifies technical skill gaps, proposes concrete portfolio projects, and provisions initialized code repositories via developer platform APIs.

## System architecture

The application uses a decoupled service architecture:
- Frontend: Next.js 14 App Router, React 18, Tailwind CSS, Lucide icons, and Recharts.
- Backend: FastAPI 0.115+, Pydantic v2 schemas, and CORS middleware.
- Resume extraction: Multi-engine parser using pdfplumber with fallback to pypdf.
- Competency benchmarking: Canonical technology taxonomy covering languages, frameworks, databases, and developer tools.
- Gap scoring engine: Mathematically weighted model applying 40% to core languages, 30% to frameworks, 20% to databases, and 10% to developer tools.
- Repository provisioning: GitHub REST API and GitLab API integrations with milestone ticket generation and local sandbox simulation.

## Prerequisites

- Node.js 20 or higher
- Python 3.11 or higher
- Git version control
- Optional: Docker and Docker Compose

## Environment configuration

### Backend configuration (`backend/.env`)
Copy the environment template:
```bash
cp backend/.env.example backend/.env
```

Available keys:
```env
NVIDIA_API_KEY=your_nvidia_nim_api_key_here
GITHUB_TOKEN=optional_default_github_token
DATABASE_URL=postgresql://user:pass@localhost:5432/skillbridge
```

### Frontend configuration (`frontend/.env.local`)
Copy the frontend template:
```bash
cp frontend/.env.example frontend/.env.local
```

Available keys:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8080
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=skillbridge_local_development_secret_32_chars
GITHUB_ID=optional_github_oauth_client_id
GITHUB_SECRET=optional_github_oauth_client_secret
```

## Local execution

### 1. Launch backend service
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### 2. Launch frontend application
```bash
cd frontend
npm install
npm run dev
```

Navigate to `http://localhost:3000` in your web browser.

## Docker execution

To run the full stack locally via Docker Compose:
```bash
docker compose up --build
```

The frontend runs on port 3000 and the backend API runs on port 8080.

## API reference

### Health check
- Method: `GET /api/health`
- Response: Returns operational status, available roles count, and LLM configuration flag.

### Role listing
- Method: `GET /api/roles`
- Response: Returns 15 pre-configured standard technology roles and their required competencies.

### Resume parse and benchmark
- Method: `POST /api/resume/parse`
- Form fields:
  - `file`: PDF document binary
  - `target_job`: Target technology role title
- Response: Structured candidate profile, contact links, detected experience years, weighted match score, category distributions, and 2 or 4 tailored project blueprints.

### Repository provisioning
- Method: `POST /api/provision`
- JSON payload:
  - `title`: Project title string
  - `tech_stack`: Array of technology labels
  - `roadmap`: Array of milestone task descriptions
  - `starter_files`: Key-value object mapping file paths to file contents
  - `token`: Personal access token, OAuth bearer token, or 'sandbox'
  - `provider`: 'github' or 'gitlab'
- Response: Created repository URL, commit hash, and milestone issues array.

## Automated test suites

### Run backend unit tests
```bash
cd backend
pytest tests/ -v
```

### Run frontend production build validation
```bash
cd frontend
npm run build
```
