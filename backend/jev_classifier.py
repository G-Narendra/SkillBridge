"""
JEV Document Classifier & Ingestion Gate (Just-in-Time Evaluator & Validator).
Evaluates incoming document text against structural, semantic, and stylistic resume indicators.
Rejects non-resume uploads (AI prompts, loop engineering directives, adversarial prompt injections,
course syllabi, software documentation/READMEs, invoices, academic research papers, source code,
legal agreements, and cover letters) prior to downstream parsing and competency benchmarking.
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
# Multiline anchored regex requiring section headers to appear on their own header line or block
RESUME_SECTION_PATTERNS = {
    "experience": [
        r'(?im)(?:^|\n)\s*(?:#+\s*|[*•\-–—]\s*)?(?:work\s+experience|professional\s+experience|employment\s+history|career\s+history|work\s+history|experience)\s*(?::|—|–|-|\n|$)',
        r'(?im)(?:^|\n)\s*(?:#+\s*|[*•\-–—]\s*)?(?:internships?|practical\s+training)\s*(?::|—|–|-|\n|$)'
    ],
    "education": [
        r'(?im)(?:^|\n)\s*(?:#+\s*|[*•\-–—]\s*)?(?:education|academic\s+background|academic\s+qualifications|educational\s+qualifications|education\s+(&|and)\s+qualifications)\s*(?::|—|–|-|\n|$)',
        r'(?i)\b(?:bachelor|master|b\.?tech|b\.?s\.?|m\.?s\.?|ph\.?d|diploma)\s+(?:of|in)\b'
    ],
    "skills": [
        r'(?im)(?:^|\n)\s*(?:#+\s*|[*•\-–—]\s*)?(?:technical\s+skills|core\s+competencies|skills\s+(&|and)\s+abilities|technical\s+stack|programming\s+languages|technical\s+proficiencies|skills|technologies|tools\s+(&|and)\s+technologies)\s*(?::|—|–|-|\n|$)'
    ],
    "projects": [
        r'(?im)(?:^|\n)\s*(?:#+\s*|[*•\-–—]\s*)?(?:projects|technical\s+projects|personal\s+projects|academic\s+projects|capstone\s+projects?|selected\s+projects|key\s+projects)\s*(?::|—|–|-|\n|$)'
    ],
    "certifications": [
        r'(?im)(?:^|\n)\s*(?:#+\s*|[*•\-–—]\s*)?(?:certifications?|licenses?\s+(&|and)\s+certifications?|credentials?|professional\s+certifications?)\s*(?::|—|–|-|\n|$)'
    ],
    "summary_objective": [
        r'(?im)(?:^|\n)\s*(?:#+\s*|[*•\-–—]\s*)?(?:professional\s+summary|career\s+objective|profile\s+summary|about\s+me|summary|executive\s+summary|objective)\s*(?::|—|–|-|\n|$)'
    ]
}

# Chronological Employment / Education Date Span Patterns
DATE_SPAN_PATTERN = r'(?i)\b(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:20[0-2][0-9]|199[0-9])\s*(?:-|–|—|to)\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:present|current|20[0-2][0-9]|199[0-9])\b'
EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_PATTERN = r'(?:\+\d{1,3}[\s-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,5}'

# Distinctive Non-Resume Negative Classification Markers
NEGATIVE_DOCUMENT_TAXONOMY = {
    "ai_prompt_or_loop": {
        "keywords": [
            r'\bloop\s+engineering\b', r'\bautonomous\s+loop\b', r'\bcouncil\s+protocol\b',
            r'\bmulti-role\s+council\b', r'\bstage\s+[1-4]:', r'\banti-student\s+code\s+standard\b',
            r'\bfaang\s+staff\s+technical\s+depth\b', r'\bponytail\s+(?:decision|ladder)\b',
            r'\bsystem\s+prompt\b', r'\byou\s+are\s+an\s+ai\b', r'\byou\s+are\s+a\s+(?:helpful\s+)?assistant\b',
            r'\byou\s+must\s+(?:not\s+)?act\s+as\b', r'\binstructions\s+for\s+(?:ai|agent)\b',
            r'\bprompt\s+engineering\b', r'\bchain\s+of\s+thought\b', r'\btool_call\b',
            r'\bdefault_api:\b', r'<USER_REQUEST>', r'\brole\s+orchestration\b',
            r'\borchestrate\.py\b', r'\btask_id\b', r'\bsubagent\b', r'\bsandbox\s+mode\b',
            r'\bbanned\s+student\s+anti-patterns\b', r'\bthe\s+agent\s+must\b'
        ],
        "label": "AI system prompt or engineering directive document",
        "guidance": "Please upload your personal CV or resume instead to benchmark your skills."
    },
    "prompt_injection": {
        "keywords": [
            r'\bignore\s+(?:all\s+)?(?:previous|prior)\s+instructions\b',
            r'\bdisregard\s+(?:all\s+)?(?:previous|prior)\s+instructions\b',
            r'\bsystem\s+override\b', r'\boverride\s+(?:all\s+)?(?:safety|system)\s+checks?\b',
            r'\byou\s+are\s+now\s+in\s+developer\s+mode\b', r'\bdan\s+mode\b', r'\bjailbreak\b',
            r'\brate\s+(?:this\s+)?candidate\s+100%\b', r'\bgive\s+(?:me|candidate)\s+100%\b',
            r'\bbypass\s+(?:security|verification|checks?)\b', r'\bgrant\s+full\s+clearance\b',
            r'<\|im_start\|>', r'<\|im_end\|>', r'---\s*BEGIN\s+SYSTEM\s+PROMPT'
        ],
        "label": "document containing system overrides or adversarial prompt directives",
        "guidance": "Please upload an authentic personal CV or resume."
    },
    "course_syllabus": {
        "keywords": [
            r'\bcourse\s+syllabus\b', r'\bsyllabus\b', r'\bcourse\s+outline\b',
            r'\bgrading\s+policy\b', r'\bgrading\s+criteria\b', r'\bgrading\s+breakdown\b',
            r'\boffice\s+hours\s*:', r'\binstructor\s*:', r'\bteaching\s+assistant\b',
            r'\blecture\s+\d+:', r'\bhomework\s+\d+:', r'\bassignment\s+\d+:',
            r'\bmidterm\s+exam\b', r'\bfinal\s+exam\b', r'\bcourse\s+schedule\b',
            r'\blearning\s+outcomes\b', r'\brequired\s+textbook\b',
            r'\bacademic\s+integrity\s+policy\b', r'\bprerequisites\s*:', r'\bclass\s+schedule\b'
        ],
        "label": "course syllabus or academic curriculum document",
        "guidance": "Please upload your personal CV or resume instead to benchmark your skills."
    },
    "software_documentation": {
        "keywords": [
            r'\btable\s+of\s+contents\b', r'\bgetting\s+started\b', r'\binstallation\s+guide\b',
            r'\bhow\s+to\s+install\b', r'\bquick\s+start\b', r'\bpip\s+install\b',
            r'\bnpm\s+(?:install|run\s+build)\b', r'\bdocker\s+run\b', r'\busage\s+example\b',
            r'\bcontributing\s+guidelines\b', r'\bbug\s+reports\b', r'\bpull\s+requests\s+welcome\b',
            r'\blicense\s*:\s*(?:mit|apache|gpl)\b', r'\bsystem\s+architecture\s+document\b',
            r'\bpr\s+planning\b', r'\bstack\s+pr\s+workflow\b'
        ],
        "label": "software documentation or project repository README",
        "guidance": "Please upload your personal CV or resume instead to benchmark your skills."
    },
    "meeting_notes": {
        "keywords": [
            r'\bmeeting\s+notes\b', r'\bmeeting\s+minutes\b', r'\battendees\s*:',
            r'\bagenda\s*:', r'\baction\s+items\s*:', r'\bcall\s+recording\b',
            r'\bdiscussion\s+topics\s*:', r'\btranscript\s*:'
        ],
        "label": "meeting notes or discussion transcript",
        "guidance": "Please upload your personal CV or resume instead to benchmark your skills."
    },
    "invoice": {
        "keywords": [
            r'\binvoice\b', r'\binvoice\s+(?:number|no|#)\b', r'\bbill(?:ed)?\s+to\b', r'\bship\s+to\b',
            r'\bamount\s+due\b', r'\btotal\s+due\b', r'\bsubtotal\b', r'\btax\s+invoice\b',
            r'\bdue\s+date\b', r'\bpayment\s+(?:terms|due)\b', r'\bremit\s+to\b', r'\bwire\s+transfer\b',
            r'\bunit\s+price\b', r'\bqty\b'
        ],
        "label": "invoice or billing statement",
        "guidance": "Please upload a personal CV or resume."
    },
    "academic_paper": {
        "keywords": [
            r'\babstract\b', r'\bintroduction\b', r'\brelated\s+work\b', r'\bmethodology\b',
            r'\bexperimental\s+results\b', r'\bconclusion\s+and\s+future\s+work\b', r'\breferences\b',
            r'\bproceedings\s+of\b', r'\bietf\b', r'\bieee\b', r'\bacm\b', r'\barxiv:\b', r'\bdoi:\b', r'\bet\s+al\.'
        ],
        "label": "academic research paper or journal article",
        "guidance": "Please upload a personal CV or student resume."
    },
    "legal_contract": {
        "keywords": [
            r'\bwhereas\b', r'\bparty\s+of\s+the\s+first\s+part\b', r'\bindemnification\b',
            r'\bgoverning\s+law\b', r'\bconfidential\s+information\s+shall\s+mean\b',
            r'\bnon-disclosure\s+agreement\b', r'\bin\s+witness\s+whereof\b', r'\bhereby\s+agrees?\b'
        ],
        "label": "legal contract or non-disclosure agreement",
        "guidance": "Please upload your curriculum vitae or resume."
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
        "guidance": "Please upload your CV or resume containing your work experience and technical skills to proceed."
    },
    "job_description": {
        "keywords": [
            r'\bjob\s+description\b', r'\brole\s+overview\b', r'\bwhat\s+you(?:\'ll|\s+will)\s+do\b',
            r'\bwhat\s+we(?:\'re|\s+are)\s+looking\s+for\b', r'\bresponsibilities\s+(?:and|&)\s+requirements\b',
            r'\bkey\s+responsibilities\b', r'\babout\s+the\s+(?:company|role|team)\b',
            r'\bequal\s+opportunity\s+employer\b', r'\bcompensation\s+(?:and|&)\s+benefits\b'
        ],
        "label": "job description",
        "guidance": "Please upload your personal CV or resume instead of a job posting."
    },
    "source_code": {
        "keywords": [
            r'#include\s+<', r'public\s+static\s+void\s+main', r'def\s+[a-zA-Z_]\w*\s*\(',
            r'function\s+[a-zA-Z_]\w*\s*\(', r'import\s+react\s+from', r'from\s+[a-zA-Z_]\w*\s+import',
            r'console\.log\(', r'System\.out\.println\(', r'package\s+[a-zA-Z_]'
        ],
        "label": "raw source code file or configuration script",
        "guidance": "Please provide a standard resume document."
    }
}

# Imperative directives vs past-tense achievement action verbs
IMPERATIVE_DIRECTIVE_PATTERN = r'(?i)\b(?:you\s+must(?:\s+not)?|you\s+should(?:\s+not)?|always\s+ensure|never\s+(?:use|write|allow)|strictly\s+(?:forbidden|prohibited|required)|do\s+not\s+(?:use|write|skip)|the\s+agent\s+must|instructions\s*:|step\s+\d+:|rule\s+\d+:|rubric\s*:|grading\s*:|prerequisites\s*:)\b'
PAST_ACTION_VERB_PATTERN = r'(?i)\b(?:developed|engineered|implemented|designed|built|architected|created|spearheaded|optimized|refactored|deployed|maintained|scaled|automated|reduced|increased|achieved|configured|integrated|analyzed|collaborated|graduated|earned|awarded)\b'

def classify_document(text: str) -> JEVValidationResult:
    """
    Evaluates whether raw document text represents a genuine resume/CV.
    Computes confidence score and returns structured validation status.
    Protects against AI system prompts, loop engineering directives, prompt injections,
    syllabi, README files, invoices, contracts, and cover letters.
    """
    clean_text = text.strip()
    if len(clean_text) < 60:
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.05,
            document_type="unrelated_document",
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason="The uploaded document contains insufficient text (< 60 characters).",
            actionable_guidance="Please upload a complete resume with at least your work history or projects, education, and technical skills.",
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

    # 2. Check for explicit prompt injections / jailbreaks immediately
    if negative_scores.get("prompt_injection", 0) >= 1:
        cfg = NEGATIVE_DOCUMENT_TAXONOMY["prompt_injection"]
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.05,
            document_type="prompt_injection",
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason=f"The uploaded file is a {cfg['label']}.",
            actionable_guidance=cfg["guidance"],
            positive_signals_count=0,
            negative_signals_count=negative_scores["prompt_injection"]
        )

    # 3. Check for AI prompt / loop engineering directives
    if dominant_neg_type == "ai_prompt_or_loop" and max_neg_matches >= 2:
        cfg = NEGATIVE_DOCUMENT_TAXONOMY["ai_prompt_or_loop"]
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.10,
            document_type="ai_prompt_or_loop",
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason=f"The uploaded file appears to be an {cfg['label']}.",
            actionable_guidance=cfg["guidance"],
            positive_signals_count=0,
            negative_signals_count=max_neg_matches
        )

    # 4. Check for course syllabus
    if dominant_neg_type == "course_syllabus" and max_neg_matches >= 2:
        cfg = NEGATIVE_DOCUMENT_TAXONOMY["course_syllabus"]
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.10,
            document_type="course_syllabus",
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason=f"The uploaded file appears to be a {cfg['label']}.",
            actionable_guidance=cfg["guidance"],
            positive_signals_count=0,
            negative_signals_count=max_neg_matches
        )

    # 5. Check for software documentation / README
    if dominant_neg_type == "software_documentation" and max_neg_matches >= 2:
        cfg = NEGATIVE_DOCUMENT_TAXONOMY["software_documentation"]
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.10,
            document_type="software_documentation",
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason=f"The uploaded file appears to be {cfg['label']}.",
            actionable_guidance=cfg["guidance"],
            positive_signals_count=0,
            negative_signals_count=max_neg_matches
        )

    # 6. Check for meeting notes
    if dominant_neg_type == "meeting_notes" and max_neg_matches >= 2:
        cfg = NEGATIVE_DOCUMENT_TAXONOMY["meeting_notes"]
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.10,
            document_type="meeting_notes",
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason=f"The uploaded file appears to be {cfg['label']}.",
            actionable_guidance=cfg["guidance"],
            positive_signals_count=0,
            negative_signals_count=max_neg_matches
        )

    # 7. Check for cover letters
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
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason="The uploaded file is a cover letter.",
            actionable_guidance="Please upload your CV or resume instead to benchmark your skills.",
            positive_signals_count=0,
            negative_signals_count=max(max_neg_matches, 2)
        )

    # 8. Check for job descriptions
    if dominant_neg_type == "job_description" and max_neg_matches >= 2:
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.10,
            document_type="job_description",
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason="The uploaded file is a job description.",
            actionable_guidance="Please upload your personal CV or resume instead of a job posting.",
            positive_signals_count=0,
            negative_signals_count=max_neg_matches
        )

    # 9. Other negative overrides (invoice, legal, code, academic paper)
    threshold = 2 if dominant_neg_type in ["invoice", "legal_contract", "source_code"] else 3
    if max_neg_matches >= threshold:
        cfg = NEGATIVE_DOCUMENT_TAXONOMY[dominant_neg_type]
        confidence = min(0.85 + (max_neg_matches * 0.03), 0.99)
        return JEVValidationResult(
            is_resume=False,
            confidence_score=round(1.0 - confidence, 3),
            document_type=dominant_neg_type,
            detected_sections=[],
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason=f"The uploaded file is a {cfg['label']}.",
            actionable_guidance=cfg["guidance"],
            positive_signals_count=0,
            negative_signals_count=max_neg_matches
        )

    # 10. Evaluate Section Headings
    detected_sections: List[str] = []
    for section_name, patterns in RESUME_SECTION_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, clean_text):
                detected_sections.append(section_name)
                break

    # 11. Personhood and Contact Signatures
    has_date_spans = bool(re.search(DATE_SPAN_PATTERN, clean_text))
    has_email = bool(re.search(EMAIL_PATTERN, clean_text))
    has_phone = bool(re.search(PHONE_PATTERN, clean_text))

    # 12. Imperative vs Past Action verb analysis
    imperatives = len(re.findall(IMPERATIVE_DIRECTIVE_PATTERN, clean_text))
    past_actions = len(re.findall(PAST_ACTION_VERB_PATTERN, clean_text))

    # If document has high imperative directives and very few personal past actions, it's instruction/prompt text
    if imperatives >= 3 and imperatives > past_actions:
        return JEVValidationResult(
            is_resume=False,
            confidence_score=0.15,
            document_type="instruction_document",
            detected_sections=detected_sections,
            missing_critical_sections=["work experience or projects", "education or certifications", "technical skills"],
            rejection_reason="The uploaded file appears to be a list of instructions or directives rather than a personal resume.",
            actionable_guidance="Please upload your personal CV or resume instead to benchmark your skills.",
            positive_signals_count=len(detected_sections),
            negative_signals_count=imperatives
        )

    positive_signals = len(detected_sections)
    if has_date_spans:
        positive_signals += 2
    if has_email:
        positive_signals += 1
    if has_phone:
        positive_signals += 1
    if past_actions >= 2:
        positive_signals += 1

    # Check for Essential Pillars (Student Projects & Certifications count as valid pillars)
    has_experience = ("experience" in detected_sections) or ("projects" in detected_sections)
    has_education = ("education" in detected_sections) or ("certifications" in detected_sections)
    has_skills = ("skills" in detected_sections)

    missing_critical = []
    if not has_experience:
        missing_critical.append("work experience or projects")
    if not has_education:
        missing_critical.append("education or certifications")
    if not has_skills:
        missing_critical.append("technical skills")

    # Base confidence calculation
    base_confidence = min(positive_signals / 7.0, 1.0)
    if len(missing_critical) >= 2 and not (has_email or has_phone):
        base_confidence *= 0.40
    elif len(missing_critical) >= 2:
        base_confidence *= 0.60

    if max_neg_matches > 0:
        base_confidence = max(base_confidence - (max_neg_matches * 0.12), 0.05)

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
