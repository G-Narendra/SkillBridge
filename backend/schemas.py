"""
Strict Pydantic v2 Domain Schemas & API Contracts for SkillBridge AI (v2.0).
Defines immutable data models for 4-tier taxonomy, transparent benchmarks,
pedagogical gap diagnostics, and downloadable project blueprints.
"""

from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field

class CompetencyItem(BaseModel):
    name: str
    level: str = "Beginner"
    verified: bool = True

class ExtractedCompetencies(BaseModel):
    languages: List[CompetencyItem] = Field(default_factory=list)
    frameworks: List[CompetencyItem] = Field(default_factory=list)
    databases: List[CompetencyItem] = Field(default_factory=list)
    tools_infrastructure: List[CompetencyItem] = Field(default_factory=list)

class BenchmarkStandard(BaseModel):
    standard_name: str
    sample_size: str
    comparison_source: str
    percentile_threshold: int = 80
    required_distribution: Dict[str, List[str]] = Field(default_factory=dict)

class CompetencyGapItem(BaseModel):
    skill: str
    tier: Literal["languages", "frameworks", "databases", "tools"]
    tier_label: str
    current_proficiency: int = 0
    required_benchmark: int = 80
    deficit_delta: float
    priority: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    pedagogical_reasoning: str
    actionable_recommendation: str

class CategoryMetrics(BaseModel):
    tier_label: str
    matched: List[str] = Field(default_factory=list)
    missing: List[str] = Field(default_factory=list)
    percentage: int
    total_required: int
    weight: int

class ProjectBlueprint(BaseModel):
    id: str
    title: str
    objective: str
    difficulty: str
    hours: int
    tech_stack: List[str] = Field(default_factory=list)
    target_skills_covered: List[str] = Field(default_factory=list)
    roadmap: List[str] = Field(default_factory=list)
    starter_files: Dict[str, str] = Field(default_factory=dict)
    manual_cli_commands: str
    is_skeleton: bool = True
    is_kaggle_track: bool = False

class DownloadZipRequest(BaseModel):
    blueprint: Dict[str, Any]

class ResumeParseResponse(BaseModel):
    target_role: str
    experience_years: float
    match_percentage: int
    competency_deficit_delta: float
    benchmark_standard: BenchmarkStandard
    category_breakdown: Dict[str, CategoryMetrics]
    competency_gaps: List[CompetencyGapItem]
    matched_skills: List[str]
    missing_skills: List[str]
    projects: List[ProjectBlueprint]
    contacts: Dict[str, Any] = Field(default_factory=dict)
