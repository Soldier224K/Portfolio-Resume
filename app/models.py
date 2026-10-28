from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

# Profile Schemas
class ProfileBase(BaseModel):
    name: str
    title: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio_url: Optional[str] = None
    summary: Optional[str] = None

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    updated_at: Optional[Any] = None

    model_config = ConfigDict(from_attributes=True)

# Education Schemas
class EducationBase(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_year: str
    end_year: str
    score: Optional[str] = None
    highlights: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class EducationResponse(EducationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Skill Schemas
class SkillBase(BaseModel):
    name: str
    category: str
    proficiency: str = "Advanced"
    is_highlighted: bool = False

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Experience Schemas
class ExperienceBase(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    start_date: str
    end_date: str
    is_current: bool = False
    description: str
    technologies: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceResponse(ExperienceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Project Schemas
class ProjectBase(BaseModel):
    title: str
    subtitle_role: str
    repo_link: Optional[str] = None
    demo_link: Optional[str] = None
    tech_stack: str
    description: str
    architecture_highlights: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_featured: bool = True

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Certification Schemas
class CertificationBase(BaseModel):
    name: str
    issuing_org: str
    issue_date: str
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None

class CertificationCreate(CertificationBase):
    pass

class CertificationResponse(CertificationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Achievement Schemas
class AchievementBase(BaseModel):
    title: str
    issuer: str
    date: Optional[str] = None
    description: str
    category: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class AchievementResponse(AchievementBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Publication Schemas
class PublicationBase(BaseModel):
    title: str
    venue_type: str
    publisher: str
    publication_date: Optional[str] = None
    url: Optional[str] = None
    abstract: str

class PublicationCreate(PublicationBase):
    pass

class PublicationResponse(PublicationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Language Schemas
class LanguageBase(BaseModel):
    language: str
    proficiency: str

class LanguageCreate(LanguageBase):
    pass

class LanguageResponse(LanguageBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Full Portfolio Export / Retrieval Schema
class PortfolioFullResponse(BaseModel):
    profile: Optional[ProfileResponse] = None
    education: List[EducationResponse] = []
    skills: List[SkillResponse] = []
    experiences: List[ExperienceResponse] = []
    projects: List[ProjectResponse] = []
    certifications: List[CertificationResponse] = []
    achievements: List[AchievementResponse] = []
    publications: List[PublicationResponse] = []
    languages: List[LanguageResponse] = []

    model_config = ConfigDict(from_attributes=True)

# JD Analysis Schemas
class JDAnalysisRequest(BaseModel):
    job_description: str
    target_title: Optional[str] = None

class JDAnalysisResponse(BaseModel):
    role_title: str
    company_name: Optional[str] = None
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    domain_keywords: List[str]
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    suggested_project_ids: List[int]
    suggested_skill_ids: List[int]
    suggested_experience_ids: List[int]
    suggested_summary: str

# Resume Customization & Generation Schemas
class ResumeGenerateRequest(BaseModel):
    target_title: str
    job_description: Optional[str] = None
    custom_summary: Optional[str] = None
    selected_project_ids: List[int]
    selected_skill_ids: List[int]
    selected_experience_ids: List[int]
    selected_certification_ids: List[int] = []
    selected_achievement_ids: List[int] = []
    selected_publication_ids: List[int] = []

class TailoredSummaryRequest(BaseModel):
    job_description: str
    target_title: str

class UnstructuredParseRequest(BaseModel):
    raw_text: str

class GoogleSheetSyncRequest(BaseModel):
    webhook_url: Optional[str] = None
    sheet_id: Optional[str] = None

class ApiKeyConfigRequest(BaseModel):
    gemini_api_key: Optional[str] = None
    sheets_webhook_url: Optional[str] = None
