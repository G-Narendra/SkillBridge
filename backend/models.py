from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String, primary_key=True)
    target_role = Column(String, nullable=False)
    extracted_skills = Column(JSON, nullable=False)
    match_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TargetJobProfile(Base):
    __tablename__ = "target_job_profiles"

    role_id = Column(String, primary_key=True)
    role_name = Column(String, nullable=False, unique=True)
    required_skills = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class GeneratedProjectRecord(Base):
    __tablename__ = "generated_projects"

    project_id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(JSON, nullable=False)
    roadmap = Column(JSON, nullable=False)
    starter_files = Column(JSON, nullable=True)
    repository_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
