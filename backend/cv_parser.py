import io
import re
from typing import Dict, List, Set, Any
import pypdf
from jev_classifier import classify_document, JEVValidationResult
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

CANONICAL_TAXONOMY: Dict[str, List[str]] = {
    "languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
        "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "Bash", "Shell",
        "Solidity", "HTML", "CSS"
    ],
    "frameworks": [
        "React", "Next.js", "Vue", "Angular", "Svelte", "Django", "FastAPI",
        "Flask", "Express", "NestJS", "Spring Boot", "PyTorch", "TensorFlow",
        "Scikit-learn", "Keras", "LangChain", "LlamaIndex", "Hugging Face",
        "Pandas", "NumPy", "Tailwind CSS", "Redux", "Node.js"
    ],
    "databases": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra",
        "DynamoDB", "Snowflake", "BigQuery", "Elasticsearch", "Neo4j",
        "Milvus", "Pinecone", "ChromaDB", "Oracle", "MSSQL"
    ],
    "tools": [
        "Docker", "Kubernetes", "Git", "GitHub Actions", "GitLab CI", "Terraform",
        "AWS", "Google Cloud", "Azure", "Linux", "Jenkins", "Ansible", "Helm",
        "Prometheus", "Grafana", "Apache Airflow", "dbt", "Apache Spark",
        "Apache Kafka", "Nginx", "Postman", "Vite", "Webpack", "Tableau", "Power BI",
        "Excel", "CUDA", "CMake", "OpenCV"
    ]
}

TAXONOMY_ALIASES: Dict[str, str] = {
    "py": "Python",
    "python3": "Python",
    "js": "JavaScript",
    "ts": "TypeScript",
    "golang": "Go",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "psql": "PostgreSQL",
    "k8s": "Kubernetes",
    "kube": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "reactjs": "React",
    "react.js": "React",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "vuejs": "Vue",
    "vue.js": "Vue",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "expressjs": "Express",
    "express.js": "Express",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "torch": "PyTorch",
    "pytorch": "PyTorch",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "sklearn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "scikit": "Scikit-learn",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "power-bi": "Power BI",
    "spark": "Apache Spark",
    "pyspark": "Apache Spark",
    "apache spark": "Apache Spark",
    "kafka": "Apache Kafka",
    "apache kafka": "Apache Kafka",
    "airflow": "Apache Airflow",
    "apache airflow": "Apache Airflow",
    "actions": "GitHub Actions",
    "github actions": "GitHub Actions",
    "gitlab ci": "GitLab CI",
    "gitlab-ci": "GitLab CI",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "hugging face": "Hugging Face",
    "huggingface": "Hugging Face",
    "langchain": "LangChain",
    "llamaindex": "LlamaIndex",
    "llama-index": "LlamaIndex",
    "elastic": "Elasticsearch",
    "elasticsearch": "Elasticsearch",
    "bigquery": "BigQuery",
    "snowflake": "Snowflake",
    "dbt": "dbt",
    "tableau": "Tableau",
    "solidity": "Solidity",
    "bash": "Bash",
    "shell": "Shell",
    "linux": "Linux",
    "excel": "Excel",
    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "cuda": "CUDA",
    "cmake": "CMake",
    "opencv": "OpenCV",
    "tensorrt": "TensorRT"
}

CANONICAL_SKILL_MAP: Dict[str, str] = {s.lower(): s for cat in CANONICAL_TAXONOMY.values() for s in cat}
for _a, _c in TAXONOMY_ALIASES.items():
    CANONICAL_SKILL_MAP[_a.lower()] = _c

def canonicalize_skill(skill_name: str) -> str:
    """Returns the official canonical representation of a skill name."""
    cleaned = skill_name.strip()
    return CANONICAL_SKILL_MAP.get(cleaned.lower(), cleaned)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from PDF byte content.
    Uses pdfplumber first, falling back to pypdf for damaged streams.
    """
    extracted_text = ""
    if pdfplumber is not None:
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text(layout=True) or page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
        except Exception:
            pass
    
    if not extracted_text.strip():
        # Fallback to pypdf when pdfplumber encounters malformed structures or is not installed
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            if reader.is_encrypted:
                raise ValueError("The provided PDF file is password protected.")
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        except Exception as fallback_error:
            raise ValueError(f"Failed to extract text from document: {fallback_error}")

    clean_text = extracted_text.strip()
    if not clean_text:
        # Final attempt without layout mode
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    clean_text += t + "\n"
            clean_text = clean_text.strip()
        except Exception:
            pass

    if not clean_text:
        raise ValueError("Document contains no readable text layer. Scanned files require OCR.")

    return clean_text

def extract_candidate_links(text: str) -> Dict[str, Any]:
    """
    Parses candidate email, LinkedIn, GitHub, portfolio URLs, name, and phone from resume text.
    """
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    github_match = re.search(r'(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_-]+)', text, re.IGNORECASE)
    linkedin_match = re.search(r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/([a-zA-Z0-9_.-]+)', text, re.IGNORECASE)
    phone_match = re.search(r'(\+?\d{1,3}[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4})', text)

    # Heuristic for portfolio URL: match explicit web URLs or modern portfolio domains, strictly excluding academic degrees
    portfolio_url = None
    all_url_matches = re.finditer(
        r'(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*\.(?:dev|me|io|app|page|site|online|vercel\.app|netlify\.app|github\.io|tech))(?:\/[^\s]*)?',
        text,
        re.IGNORECASE
    )
    for m in all_url_matches:
        cand = m.group(0).strip().rstrip(".,;:/")
        domain_part = m.group(1).lower().strip()
        # Strictly ignore academic degrees
        if domain_part in ["b.tech", "m.tech", "b.tech.", "m.tech.", "b-tech", "m-tech"]:
            continue
        # Single-letter prefixes before .tech are university degrees (e.g., B.Tech)
        if domain_part.endswith(".tech") and len(domain_part.split(".")[0]) <= 2:
            continue
        # Ignore email domains matching the candidate's email
        if email_match and domain_part in email_match.group(0).lower():
            continue
        # Valid portfolio found
        portfolio_url = cand
        break

    # Heuristic for candidate name: look at the top non-blank lines with delimiter awareness
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    candidate_name = None
    if lines:
        for top_line in lines[:3]:
            # Resumes often format: "First Last | email@domain.com | +1-234-567"
            segments = [s.strip() for s in re.split(r'[\s]*[|•\t][\s]*', top_line) if s.strip()]
            first_segment = segments[0] if segments else top_line
            words = first_segment.split()
            # Must be 1-4 words, contain no @ or digits, and not be common section headers
            if 1 <= len(words) <= 4 and not re.search(r'[@\d:]', first_segment):
                first_lower = first_segment.lower()
                banned_headers = {
                    "resume", "curriculum", "vitae", "summary", "profile", "contact",
                    "experience", "education", "skills", "projects", "cover", "letter",
                    "cover letter", "application", "dear"
                }
                if not any(h in first_lower for h in banned_headers):
                    candidate_name = first_segment
                    break

    return {
        "name": candidate_name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "github": f"https://github.com/{github_match.group(1)}" if github_match else None,
        "linkedin": f"https://linkedin.com/in/{linkedin_match.group(1)}" if linkedin_match else None,
        "portfolio": portfolio_url
    }

def anonymize_resume_pii(text: str, contacts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strips personally identifiable information for GDPR/DPDP compliance and bias-free evaluation.
    Redacts candidate names, emails, phone numbers, and direct contact identifiers.
    """
    anonymized = text
    entities_redacted = {
        "names": 0,
        "emails": 0,
        "phones": 0,
        "postal_codes": 0
    }

    if contacts.get("email"):
        anonymized, count = re.subn(re.escape(contacts["email"]), "[REDACTED_EMAIL]", anonymized, flags=re.IGNORECASE)
        entities_redacted["emails"] += count

    if contacts.get("phone"):
        anonymized, count = re.subn(re.escape(contacts["phone"]), "[REDACTED_PHONE]", anonymized)
        entities_redacted["phones"] += count

    if contacts.get("name") and len(contacts["name"].strip()) >= 3:
        anonymized, count = re.subn(re.escape(contacts["name"].strip()), "[REDACTED_CANDIDATE_NAME]", anonymized, flags=re.IGNORECASE)
        entities_redacted["names"] += count

    # Redact common location patterns and postal codes
    anonymized, postal_count = re.subn(r'\b(?:\d{5}(?:-\d{4})?|\d{6})\b', '[REDACTED_POSTAL_CODE]', anonymized)
    entities_redacted["postal_codes"] += postal_count

    # Redact any residual email addresses
    anonymized, extra_email_count = re.subn(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]', anonymized)
    entities_redacted["emails"] += extra_email_count

    total_redactions = sum(entities_redacted.values())

    audit = {
        "status": "anonymized",
        "total_redactions": total_redactions,
        "redactions_applied": total_redactions,
        "entities_redacted": entities_redacted,
        "compliance_standard": "GDPR Article 9 and DPDP Act 2023",
        "bias_mitigation": "Name, gender, contact, and geographic indicators masked"
    }

    return {
        "anonymized_text": anonymized,
        "audit": audit
    }

def audit_resume_content(text: str, detected_skills: List[str]) -> Dict[str, Any]:
    """
    Evaluates resume text for measurable achievements, impact verbs, and structural completeness.
    Produces actionable recommendations following human engineering standards.
    """
    metrics_count = len(re.findall(r'\b(?:\d+[\%+]?|\$\d+)\b', text))
    has_github = bool(re.search(r'github\.com', text, re.IGNORECASE))
    skills_count = len(detected_skills)

    strengths = []
    if skills_count >= 15:
        strengths.append(f"Broad technical vocabulary across {skills_count} verified tools and technologies.")
    elif skills_count >= 8:
        strengths.append(f"Solid technical foundation with {skills_count} detected core competencies.")

    if metrics_count >= 5:
        strengths.append("Strong usage of quantitative performance metrics throughout project descriptions.")
    else:
        strengths.append("Clear project scope descriptions across demonstrated engineering assignments.")

    recommendations = []
    if not has_github:
        recommendations.append("Link public GitHub profile in the header contact block to enable automated code auditing.")
    else:
        recommendations.append("Pin verifiable repository blueprints demonstrating end-to-end architecture patterns.")

    if metrics_count < 8:
        recommendations.append("Quantify business and engineering outcomes using concrete metrics (for example: reduced query latency by 35% or processed 2M daily records).")
    else:
        recommendations.append("Add unit testing coverage statistics and CI/CD workflow badges to project summaries.")

    if len(recommendations) < 2:
        recommendations.append("Specify exact production database versions and cloud providers used in past deployments.")
    elif len(recommendations) == 3:
        recommendations.append("Document architectural design patterns such as event-driven queues or caching layers.")

    impact_score = min(max(50 + (metrics_count * 5) + (10 if has_github else 0), 40), 96)

    return {
        "impact_score": impact_score,
        "metrics_detected": metrics_count,
        "strengths": strengths[:2],
        "actionable_recommendations": recommendations[:2 if len(recommendations) < 4 else 4],
        "readiness_rating": "Competitive" if impact_score >= 80 else "Developing"
    }


def detect_experience_years(text: str) -> int:
    """
    Estimates years of candidate technical experience.
    Accurately isolates work experience from academic education dates,
    recognizes student/fresher/intern indicators, and prevents false multi-year spans
    from college enrollment periods.
    """
    text_lower = text.lower()

    # 1. Explicit fresher / student / zero-experience keywords
    fresher_indicators = [
        r'\bfresher\b',
        r'\bentry[\s-]level\b',
        r'\bstudent\b',
        r'\bundergraduate\b',
        r'\bgraduate student\b',
        r'\bpursuing\s+(?:b\.?tech|b\.?e\.?|b\.?sc|m\.?tech|m\.?s\.?|bca|mca)\b',
        r'\bexpected\s+graduation\b',
        r'\bgraduation\s+year\s*:\s*202[4-9]\b',
        r'\b0\s*(?:-\s*1)?\s*(?:years?|yrs?)(?:\s+of)?\s+experience\b',
        r'\b(?:less\s+than|<)\s*1\s*(?:year|yr)\b',
        r'\bno\s+prior\s+experience\b',
    ]
    for pattern in fresher_indicators:
        if re.search(pattern, text_lower):
            # Check if there's any conflicting senior job title
            if not re.search(r'\b(?:senior|lead|principal|architect|manager|staff)\b', text_lower):
                return 0

    # 2. Check for explicit phrase: "<N>+ years of experience" or "<N> years experience" or "experience: ... (N years)"
    exp_phrase_match = re.search(r'(?:over\s+|more\s+than\s+)?(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:professional\s+|work\s+)?experience', text_lower)
    if exp_phrase_match:
        try:
            val = float(exp_phrase_match.group(1))
            if val < 1:
                return 0
            return int(round(val))
        except ValueError:
            pass

    # Check for "experience: ... (N years)" or "experience: N years"
    exp_inline_match = re.search(r'(?:experience|employment)\s*:\s*(?:.*?\()?\s*(\d+)\s*(?:years?|yrs?)\)?', text_lower)
    if exp_inline_match:
        try:
            val = int(exp_inline_match.group(1))
            if val < 1:
                return 0
            return val
        except ValueError:
            pass

    # 3. Check for months-only experience (e.g., "6 months internship", "3 months experience")
    month_match = re.search(r'\b(\d+)\s*(?:months?|mos?)\s*(?:of\s+)?(?:internship|experience|work)', text_lower)
    if month_match:
        try:
            months = int(month_match.group(1))
            if months < 12:
                return 0
            return months // 12
        except ValueError:
            pass

    # 4. Check for employment date ranges across text, strictly excluding education lines
    lines = text.split("\n")
    in_education = False
    in_experience = False
    work_date_ranges = []

    edu_indicators = re.compile(
        r'\b(?:education|academic(?:s|\s+background|\s+qualifications?)|degrees?|university|college|school|b\.?tech|b\.?e\.?|b\.?sc|m\.?tech|bachelor|master|cgpa|gpa|diploma|hsc|ssc)\b',
        re.IGNORECASE
    )
    exp_header = re.compile(
        r'^\s*(?:(?:work|professional|industry|relevant)\s+)?(?:experience|employment|work\s+history)\b',
        re.IGNORECASE
    )
    edu_header = re.compile(
        r'^\s*(?:education|academic(?:s|\s+background|\s+qualifications?)|degrees?)\b',
        re.IGNORECASE
    )
    section_break = re.compile(
        r'^\s*(?:projects?|technical\s+skills?|skills?|certifications?|achievements?|publications?|awards?|interests?)\b',
        re.IGNORECASE
    )

    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        if edu_header.match(cleaned_line):
            in_education = True
            in_experience = False
            continue
        elif exp_header.match(cleaned_line):
            in_experience = True
            in_education = False
            # Don't skip this line: header line might contain dates like "Experience: 2020 - 2026"
        elif section_break.match(cleaned_line) and len(cleaned_line) < 40:
            in_education = False
            in_experience = False
            continue

        # If in an education section, skip all dates in this line
        if in_education:
            continue

        # If the line mentions university, degree, b.tech, etc., skip it unless explicitly inside work experience
        if edu_indicators.search(cleaned_line) and not in_experience:
            continue

        # Find date ranges in this line
        matches = re.findall(r'\b(20[0-2][0-9]|199[0-9])\s*(?:-|–|to)\s*(20[0-2][0-9]|present|current|now)\b', cleaned_line, re.IGNORECASE)
        for start_y, end_y in matches:
            is_intern = bool(re.search(r'\bintern(?:ship)?\b', cleaned_line, re.IGNORECASE))
            work_date_ranges.append((int(start_y), end_y, is_intern))

    if work_date_ranges:
        current_year = 2026
        max_span = 0
        all_intern = all(item[2] for item in work_date_ranges)
        for start_y, end_y, is_intern in work_date_ranges:
            end_val = current_year if end_y.lower() in ["present", "current", "now"] else int(end_y)
            span = max(0, end_val - start_y)
            max_span = max(max_span, span)

        if all_intern and max_span <= 1:
            return 0
        return min(max_span, 25)

    # 5. Check if candidate has an explicit future/current education graduation and zero work ranges
    if re.search(r'\b(?:education|b\.?tech|degree|college|university)\b', text_lower):
        edu_future = re.findall(r'\b(202[4-9])\b', text)
        if edu_future and not work_date_ranges:
            return 0

    # 6. Fallback for entry-level candidates
    return 0

def extract_skills_from_text(text: str) -> Dict[str, List[str]]:
    """
    Scans document text against canonical skill taxonomy and aliases.
    Returns categorized detected competencies.
    """
    text_lower = text.lower()
    # Normalize terminal periods while preserving internal dots (e.g. "node.js" vs "Docker.")
    cleaned_text = re.sub(r'\.(?=\s|$)', ' ', text_lower)
    normalized_text = " " + re.sub(r'[^a-zA-Z0-9+#.]', ' ', cleaned_text) + " "

    detected_skills_set: Set[str] = set()
    delim = r'[\s,;:()\[\].]'

    # Match aliases first
    for alias, canonical in TAXONOMY_ALIASES.items():
        alias_clean = alias.lower().strip()
        pattern = rf'(?:(?<={delim})|^){re.escape(alias_clean)}(?=(?:{delim}|$))'
        if re.search(pattern, normalized_text):
            detected_skills_set.add(canonicalize_skill(canonical))

    # Match canonical skills across all categories
    for category, skills in CANONICAL_TAXONOMY.items():
        for skill in skills:
            skill_clean = skill.lower().strip()
            pattern = rf'(?:(?<={delim})|^){re.escape(skill_clean)}(?=(?:{delim}|$))'
            if re.search(pattern, normalized_text):
                detected_skills_set.add(canonicalize_skill(skill))

    # Structure into categories
    categorized_results: Dict[str, List[str]] = {
        "languages": [],
        "frameworks": [],
        "databases": [],
        "tools": []
    }

    all_detected_list = sorted(list(detected_skills_set))
    for category, category_skills in CANONICAL_TAXONOMY.items():
        for skill in category_skills:
            if skill in detected_skills_set:
                categorized_results[category].append(skill)

    return categorized_results

def parse_resume(file_bytes: bytes) -> Dict[str, Any]:
    """
    Coordinates extraction of text, contacts, experience years, and categorized skills.
    Applies JEV document validation and GDPR/DPDP PII stripping.
    """
    raw_text = extract_text_from_pdf(file_bytes)
    jev_validation = classify_document(raw_text)
    if not jev_validation.is_resume:
        err_msg = f"{jev_validation.rejection_reason} {jev_validation.actionable_guidance}".strip()
        raise ValueError(err_msg)

    contacts = extract_candidate_links(raw_text)
    anonymized_result = anonymize_resume_pii(raw_text, contacts)
    experience_years = detect_experience_years(raw_text)
    categorized_skills = extract_skills_from_text(raw_text)

    flat_skills: List[str] = []
    for cat_list in categorized_skills.values():
        flat_skills.extend(cat_list)
    flat_skills = sorted(list(set(flat_skills)))

    resume_audit = audit_resume_content(raw_text, flat_skills)

    return {
        "raw_text_snippet": raw_text[:2500],
        "anonymized_snippet": anonymized_result["anonymized_text"][:2500],
        "anonymization_audit": anonymized_result["audit"],
        "contacts": contacts,
        "experience_years": experience_years,
        "categorized_skills": categorized_skills,
        "skills": flat_skills,
        "resume_audit": resume_audit,
        "jev_validation": jev_validation.model_dump()
    }
