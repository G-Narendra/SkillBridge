"""
JEV Document Classifier & Ingestion Gate (Just-in-Time Evaluator & Validator).
Evaluates incoming document text against structural, semantic, and stylistic resume indicators.
Rejects non-resume uploads (invoices, academic research papers, source code, legal agreements)
prior to downstream parsing and competency benchmarking.
"""

import re
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class JEVValidationResult(BaseModel):
    is_resume: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    document_type: str
    detected_sections: List[str]
    missing_critical_sections: List[str]
    rejection_reason: Optional[str] = None
    actionable_guidance: Optional[str] = None
    positive_signals_count: int
    negative_signals_count: int

# Positive Section Anchors typical of Resumes & CVs
RESUME_SECTION_PATTERNS = {
    "experience": r'\b(experience|work\s+experience|employment\s+history|professional\s+experience|work\s+history|career\s+history|internship|practical\s+training|projects?|technical\s+projects?|personal\s+projects?|portfolio|capstone)\b',
    "education": r'\b(education|academic\s+background|qualifications|degrees?|diploma|bachelor|master|phd|b\.?tech|b\.?s\.?|m\.?s\.?|university|college|gpa)\b',
    "skills": r'\b(skills|technical\s+skills|technical\s+stack|core\s+competencies|technologies|proficiencies|programming\s+languages|tools\s+(&|and)\s+technologies|core\s+technologies)\b',
    "projects": r'\b(projects|personal\s+projects|academic\s+projects|technical\s+projects|open\s+source|portfolio|hackathons?|capstone)\b',
    "certifications": r'\b(certifications?|licenses?|credentials?|accreditations?|courses?|training)\b',
    "summary_objective": r'\b(summary|professional\s+summary|profile|about\s+me|career\s+objective|executive\s+summary|objective)\b'
}

# Chronological Employment / Education Date Span Patterns
DATE_SPAN_PATTERN = r'\b(20[0-2][0-9]|199[0-9])\s*(?:-|–|—|to)\s*(?:present|current|20[0-2][0-9]|199[0-9])\b'
EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_PATTERN = r'(?:\+\d{1,3}[\s-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,5}'

# Distinctive Non-Resume Negative Classification Markers
NEGATIVE_DOCUMENT_TAXONOMY = {
    "invoice": {
        "keywords": [
            r'\binvoice\b', r'\binvoice\s+(?:number|no|#)\b', r'\bbill(?:ed)?\s+to\b', r'\bship\s+to\b',
            r'\bamount\s+due\b', r'\btotal\s+due\b', r'\bsubtotal\b', r'\btax\s+invoice\b',
            r'\bdue\s+date\b', r'\bpayment\s+(?:terms|due)\b', r'\bremit\s+to\b', r'\bwire\s+transfer\b',
            r'\bunit\s+price\b', r'\bqty\b'
        ],
        "label": "invoice or billing statement",
        "guidance": "Uploaded document appears to be an invoice, bill, or financial receipt. Please upload a professional CV or resume."
    },
    "academic_paper": {
        "keywords": [
            r'\babstract\b', r'\bintroduction\b', r'\brelated\s+work\b', r'\bmethodology\b',
            r'\bexperimental\s+results\b', r'\bconclusion\s+and\s+future\s+work\b', r'\breferences\b',
            r'\bproceedings\s+of\b', r'\bietf\b', r'\bieee\b', r'\bacm\b', r'\barxiv:\b', r'\bdoi:\b', r'\bet\s+al\.'
        ],
        "label": "academic research paper or journal article",
        "guidance": "Uploaded document appears to be an academic paper or published manuscript. Please upload a personal CV or student resume."
    },
    "legal_contract": {
        "keywords": [
            r'\bwhereas\b', r'\bparty\s+of\s+the\s+first\s+part\b', r'\bindemnification\b',
            r'\bgoverning\s+law\b', r'\bconfidential\s+information\s+shall\s+mean\b',
            r'\bnon-disclosure\s+agreement\b', r'\bin\s+witness\s+whereof\b', r'\bhereby\s+agrees?\b'
        ],
        "label": "legal contract or non-disclosure agreement",
        "guidance": "Uploaded document appears to be a legal agreement or contract. Please upload your curriculum vitae or resume."
    },
    "cover_letter": {
        "keywords": [
            r'\bcover\s+letter\b', r'\bdear\s+(?:hiring\s+manager|recruiter|team|sir|madam|mr\.|ms\.|mrs\.|dr\.)\b',
            r'\bi\s+am\s+writing\s+to\s+(?:apply|express\s+my\s+interest|submit\s+my\s+application)\b',
            r'\bplease\s+(?:find|accept)\s+(?:attached|enclosed)\s+(?:my\s+)?(?:resume|cv|application)\b',
            r'\bthank\s+you\s+for\s+your\s+time\s+and\s+consideration\b', r'\bsincerely\b',
            r'\byours\s+(?:sincerely|faithfully|truly)\b', r'\blook\s+forward\s+to\s+(?:hearing\s+from\s+you|the\s+opportunity)\b',
            r'\bexcited\s+to\s+apply\s+for\b', r'\bapplication\s+for\s+the\s+position\b'
        ],
        "label": "cover letter",
        "guidance": "The uploaded file appears to be a cover letter. Please upload your CV or resume containing your work experience and technical skills to proceed."
    },
    "job_description": {
        "keywords": [
            r'\bjob\s+description\b', r'\brole\s+overview\b', r'\bwhat\s+you(?:\'ll|\s+will)\s+do\b',
            r'\bwhat\s+we(?:\'re|\s+are)\s+looking\s+for\b', r'\bresponsibilities\s+(?:and|&)\s+requirements\b',
            r'\bkey\s+responsibilities\b', r'\babout\s+the\s+(?:company|role|team)\b',
            r'\bequal\s+opportunity\s+employer\b', r'\bcompensation\s+(?:and|&)\s+benefits\b'
        ],
        "label": "job description",
        "guidance": "The uploaded file appears to be a job description. Please upload your personal resume or CV to benchmark your skills."
    },
    "source_code": {
        "keywords": [
            r'#include\s+<', r'public\s+static\s+void\s+main', r'def\s+[a-zA-Z_]\w*\s*\(',
            r'function\s+[a-zA-Z_]\w*\s*\(', r'import\s+react\s+from', r'from\s+[a-zA-Z_]\w*\s+import',
            r'console\.log\(', r'System\.out\.println\(', r'package\s+[a-zA-Z_]'
        ],
        "label": "raw source code file or configuration script",
        "guidance": "Uploaded document contains raw source code rather than a formatted resume. Please provide a standard resume document."
    }
}

def classify_document(text: str) -> JEVValidationResult:
    """
    Evaluates whether raw document text represents a genuine resume/CV.
    Computes confidence score and returns structured validation status.
    """
    clean_text = text.strip()
    if len(clean_text) < 60:
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.05,
            document_type="unrelated_document",
            detected_sections=[],
            missing_critical_sections=["experience", "education", "skills"],
            rejection_reason="The uploaded document contains insufficient text (< 60 characters).",
            actionable_guidance="Please upload a complete resume with at least your work history, education, and technical skills.",
            positive_signals_count=0,
            negative_signals_count=0
        )

    text_lower = clean_text.lower()

    # 1. Evaluate Negative Document Signatures
    negative_scores: Dict[str, int] = {}
    for doc_type, config in NEGATIVE_DOCUMENT_TAXONOMY.items():
        matches = 0
        for pattern in config["keywords"]:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches += 1
        negative_scores[doc_type] = matches

    dominant_neg_type, max_neg_matches = max(negative_scores.items(), key=lambda x: x[1])

    # 2. Evaluate Positive Resume Structural Signals
    detected_sections: List[str] = []
    for section_name, pattern in RESUME_SECTION_PATTERNS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            detected_sections.append(section_name)

    has_date_spans = bool(re.search(DATE_SPAN_PATTERN, clean_text, re.IGNORECASE))
    has_email = bool(re.search(EMAIL_PATTERN, clean_text))
    has_phone = bool(re.search(PHONE_PATTERN, clean_text))

    positive_signals = len(detected_sections)
    if has_date_spans:
        positive_signals += 2
    if has_email:
        positive_signals += 1
    if has_phone:
        positive_signals += 1

    # 3. Check for Essential Pillars (Student Projects & Certifications count as valid pillars)
    has_experience = ("experience" in detected_sections) or ("projects" in detected_sections)
    has_education = ("education" in detected_sections) or ("certifications" in detected_sections)
    has_skills = ("skills" in detected_sections)

    missing_critical = []
    if not has_experience:
        missing_critical.append("experience or projects")
    if not has_education:
        missing_critical.append("education or certifications")
    if not has_skills:
        missing_critical.append("technical skills")

    # Explicit Cover Letter check (unambiguous rejection without robotic jargon)
    has_cover_letter_markers = (
        bool(re.search(r'\bcover\s+letter\b', text_lower)) or
        bool(re.search(r'\bdear\s+(?:hiring|recruiter|team|sir|madam|mr\.|ms\.|mrs\.|dr\.)', text_lower)) or
        bool(re.search(r'\bi\s+am\s+writing\s+to\s+(?:apply|express\s+my\s+interest|submit)', text_lower))
    )
    if (dominant_neg_type == "cover_letter" and max_neg_matches >= 2) or has_cover_letter_markers:
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.10,
            document_type="cover_letter",
            detected_sections=detected_sections,
            missing_critical_sections=missing_critical,
            rejection_reason="The uploaded file is a cover letter.",
            actionable_guidance="Please upload your CV or resume instead to benchmark your skills.",
            positive_signals_count=positive_signals,
            negative_signals_count=max(max_neg_matches, 2)
        )

    # Explicit Job Description check
    if dominant_neg_type == "job_description" and max_neg_matches >= 2:
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.10,
            document_type="job_description",
            detected_sections=detected_sections,
            missing_critical_sections=missing_critical,
            rejection_reason="The uploaded file is a job description.",
            actionable_guidance="Please upload your personal CV or resume instead of a job posting.",
            positive_signals_count=positive_signals,
            negative_signals_count=max_neg_matches
        )

    # Strong negative override (e.g. >= 2 invoice/legal/code keywords or >= 3 academic keywords)
    threshold = 2 if dominant_neg_type in ["invoice", "legal_contract", "source_code", "cover_letter", "job_description"] else 3
    if max_neg_matches >= threshold:
        config = NEGATIVE_DOCUMENT_TAXONOMY[dominant_neg_type]
        confidence = min(0.85 + (max_neg_matches * 0.03), 0.99)
        return JEVValidationResult(
            is_resume=False,
            confidence_score=round(1.0 - confidence, 3),
            document_type=dominant_neg_type,
            detected_sections=detected_sections,
            missing_critical_sections=missing_critical,
            rejection_reason=f"The uploaded file is a {config['label']}.",
            actionable_guidance=config["guidance"],
            positive_signals_count=positive_signals,
            negative_signals_count=max_neg_matches
        )

    # Calculate overall resume confidence score
    # Max positive score ~ 8-10 points
    base_confidence = min(positive_signals / 8.0, 1.0)
    
    # Penalize if missing critical pillars
    if len(missing_critical) == 3:
        base_confidence *= 0.25
    elif len(missing_critical) == 2 and not (has_email or has_phone):
        base_confidence *= 0.50

    # Penalize for residual negative markers
    if max_neg_matches > 0:
        base_confidence = max(base_confidence - (max_neg_matches * 0.10), 0.1)

    confidence_score = round(base_confidence, 2)
    is_resume = confidence_score >= 0.35 and len(missing_critical) < 3

    if not is_resume:
        return JEVValidationResult(
            is_resume=False,
            confidence_score=confidence_score,
            document_type="unrelated_document",
            detected_sections=detected_sections,
            missing_critical_sections=missing_critical,
            rejection_reason="Document lacks standard resume sections (missing: " + ", ".join(missing_critical) + ").",
            actionable_guidance="Please provide a resume containing your technical skills, work or project experience, and educational background.",
            positive_signals_count=positive_signals,
            negative_signals_count=max_neg_matches
        )

    return JEVValidationResult(
        is_resume=True,
        confidence_score=confidence_score,
        document_type="resume",
        detected_sections=detected_sections,
        missing_critical_sections=missing_critical,
        rejection_reason=None,
        actionable_guidance=None,
        positive_signals_count=positive_signals,
        negative_signals_count=max_neg_matches
    )
