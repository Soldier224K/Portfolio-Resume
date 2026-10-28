import os
import io
from fastapi import FastAPI, Depends, HTTPException, Query, Response
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import (
    init_db, get_db, SessionLocal,
    Profile, Education, Skill, Experience, Project,
    Certification, Achievement, Publication, Language
)
from app.seed_data import seed_portfolio_data
from app.models import (
    ProfileBase, ProfileUpdate, ProfileResponse,
    EducationCreate, EducationResponse,
    SkillCreate, SkillResponse,
    ExperienceCreate, ExperienceResponse,
    ProjectCreate, ProjectResponse,
    CertificationCreate, CertificationResponse,
    AchievementCreate, AchievementResponse,
    PublicationCreate, PublicationResponse,
    LanguageCreate, LanguageResponse,
    PortfolioFullResponse,
    JDAnalysisRequest, JDAnalysisResponse,
    ResumeGenerateRequest, TailoredSummaryRequest,
    UnstructuredParseRequest, GoogleSheetSyncRequest, ApiKeyConfigRequest
)
from app.gemini_service import (
    set_gemini_api_key, parse_unstructured_portfolio,
    analyze_job_description, generate_tailored_summary, CURRENT_GEMINI_KEY
)
from app.sheets_service import (
    export_portfolio_to_bytes, export_portfolio_to_file,
    sync_to_google_sheets_webhook, EXPORT_XLSX_PATH
)
from app.resume_generator import build_customized_resume_data
from app.pdf_generator import generate_pdf_resume
from app.docx_generator import generate_docx_resume

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_portfolio_data(db)
        # Export initial xlsx
        full_data = get_full_portfolio_dict(db)
        export_portfolio_to_file(full_data)
    finally:
        db.close()
    yield

app = FastAPI(
    title="AI-Powered Portfolio Management & Dynamic Resume Generator",
    description="Centralized portfolio database with Gemini API intelligence, Google Sheets synchronization, and ATS-compliant resume generation.",
    version="1.0.0",
    lifespan=lifespan
)

# In-memory configuration store for runtime testing
APP_CONFIG = {
    "gemini_api_key": os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", ""),
    "sheets_webhook_url": ""
}

# Helper to fetch full portfolio dictionary
def get_full_portfolio_dict(db: Session):
    prof = db.query(Profile).first()
    return {
        "profile": prof.to_dict() if prof else {},
        "education": [e.to_dict() for e in db.query(Education).all()],
        "skills": [s.to_dict() for s in db.query(Skill).all()],
        "experiences": [ex.to_dict() for ex in db.query(Experience).all()],
        "projects": [p.to_dict() for p in db.query(Project).all()],
        "certifications": [c.to_dict() for c in db.query(Certification).all()],
        "achievements": [a.to_dict() for a in db.query(Achievement).all()],
        "publications": [pub.to_dict() for pub in db.query(Publication).all()],
        "languages": [l.to_dict() for l in db.query(Language).all()]
    }

# ==========================================
# FULL PORTFOLIO & RESET ENDPOINTS
# ==========================================

@app.get("/api/portfolio", response_model=PortfolioFullResponse)
def get_portfolio(db: Session = Depends(get_db)):
    prof = db.query(Profile).first()
    return PortfolioFullResponse(
        profile=ProfileResponse.model_validate(prof) if prof else None,
        education=[EducationResponse.model_validate(e) for e in db.query(Education).all()],
        skills=[SkillResponse.model_validate(s) for s in db.query(Skill).all()],
        experiences=[ExperienceResponse.model_validate(ex) for ex in db.query(Experience).all()],
        projects=[ProjectResponse.model_validate(p) for p in db.query(Project).all()],
        certifications=[CertificationResponse.model_validate(c) for c in db.query(Certification).all()],
        achievements=[AchievementResponse.model_validate(a) for a in db.query(Achievement).all()],
        publications=[PublicationResponse.model_validate(pub) for pub in db.query(Publication).all()],
        languages=[LanguageResponse.model_validate(l) for l in db.query(Language).all()]
    )

@app.post("/api/portfolio/reset")
def reset_portfolio(db: Session = Depends(get_db)):
    seed_portfolio_data(db, force=True)
    full_data = get_full_portfolio_dict(db)
    export_portfolio_to_file(full_data)
    return {"message": "Portfolio database reset to default verified records successfully"}

# ==========================================
# CRUD: PROFILE
# ==========================================

@app.get("/api/profile", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    prof = db.query(Profile).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found")
    return prof

@app.put("/api/profile", response_model=ProfileResponse)
def update_profile(data: ProfileUpdate, db: Session = Depends(get_db)):
    prof = db.query(Profile).first()
    if not prof:
        prof = Profile(**data.model_dump())
        db.add(prof)
    else:
        for k, v in data.model_dump().items():
            setattr(prof, k, v)
    db.commit()
    db.refresh(prof)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return prof

# ==========================================
# CRUD: EDUCATION
# ==========================================

@app.get("/api/education")
def list_education(db: Session = Depends(get_db)):
    return [e.to_dict() for e in db.query(Education).all()]

@app.post("/api/education", response_model=EducationResponse)
def create_education(data: EducationCreate, db: Session = Depends(get_db)):
    item = Education(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/education/{item_id}", response_model=EducationResponse)
def update_education(item_id: int, data: EducationCreate, db: Session = Depends(get_db)):
    item = db.query(Education).filter(Education.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Education item not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/education/{item_id}")
def delete_education(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Education).filter(Education.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Education item not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# CRUD: SKILLS
# ==========================================

@app.get("/api/skills")
def list_skills(db: Session = Depends(get_db)):
    return [s.to_dict() for s in db.query(Skill).all()]

@app.post("/api/skills", response_model=SkillResponse)
def create_skill(data: SkillCreate, db: Session = Depends(get_db)):
    item = Skill(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/skills/{item_id}", response_model=SkillResponse)
def update_skill(item_id: int, data: SkillCreate, db: Session = Depends(get_db)):
    item = db.query(Skill).filter(Skill.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Skill item not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/skills/{item_id}")
def delete_skill(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Skill).filter(Skill.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Skill item not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# CRUD: EXPERIENCE
# ==========================================

@app.get("/api/experience")
@app.get("/api/experiences")
def list_experience(db: Session = Depends(get_db)):
    return [e.to_dict() for e in db.query(Experience).all()]

@app.post("/api/experience", response_model=ExperienceResponse)
@app.post("/api/experiences", response_model=ExperienceResponse)
def create_experience(data: ExperienceCreate, db: Session = Depends(get_db)):
    item = Experience(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/experience/{item_id}", response_model=ExperienceResponse)
@app.put("/api/experiences/{item_id}", response_model=ExperienceResponse)
def update_experience(item_id: int, data: ExperienceCreate, db: Session = Depends(get_db)):
    item = db.query(Experience).filter(Experience.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Experience item not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/experience/{item_id}")
@app.delete("/api/experiences/{item_id}")
def delete_experience(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Experience).filter(Experience.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Experience item not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# CRUD: PROJECTS
# ==========================================

@app.get("/api/projects")
def list_projects(db: Session = Depends(get_db)):
    return [p.to_dict() for p in db.query(Project).all()]

@app.post("/api/projects", response_model=ProjectResponse)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    item = Project(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/projects/{item_id}", response_model=ProjectResponse)
def update_project(item_id: int, data: ProjectCreate, db: Session = Depends(get_db)):
    item = db.query(Project).filter(Project.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Project not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/projects/{item_id}")
def delete_project(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Project).filter(Project.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# CRUD: CERTIFICATIONS
# ==========================================

@app.get("/api/certifications")
def list_certifications(db: Session = Depends(get_db)):
    return [c.to_dict() for c in db.query(Certification).all()]

@app.post("/api/certifications", response_model=CertificationResponse)
def create_certification(data: CertificationCreate, db: Session = Depends(get_db)):
    item = Certification(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/certifications/{item_id}", response_model=CertificationResponse)
def update_certification(item_id: int, data: CertificationCreate, db: Session = Depends(get_db)):
    item = db.query(Certification).filter(Certification.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certification not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/certifications/{item_id}")
def delete_certification(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Certification).filter(Certification.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# CRUD: ACHIEVEMENTS
# ==========================================

@app.get("/api/achievements")
def list_achievements(db: Session = Depends(get_db)):
    return [a.to_dict() for a in db.query(Achievement).all()]

@app.post("/api/achievements", response_model=AchievementResponse)
def create_achievement(data: AchievementCreate, db: Session = Depends(get_db)):
    item = Achievement(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/achievements/{item_id}", response_model=AchievementResponse)
def update_achievement(item_id: int, data: AchievementCreate, db: Session = Depends(get_db)):
    item = db.query(Achievement).filter(Achievement.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Achievement not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/achievements/{item_id}")
def delete_achievement(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Achievement).filter(Achievement.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Achievement not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# CRUD: PUBLICATIONS
# ==========================================

@app.get("/api/publications")
def list_publications(db: Session = Depends(get_db)):
    return [pub.to_dict() for pub in db.query(Publication).all()]

@app.post("/api/publications", response_model=PublicationResponse)
def create_publication(data: PublicationCreate, db: Session = Depends(get_db)):
    item = Publication(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/publications/{item_id}", response_model=PublicationResponse)
def update_publication(item_id: int, data: PublicationCreate, db: Session = Depends(get_db)):
    item = db.query(Publication).filter(Publication.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Publication not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/publications/{item_id}")
def delete_publication(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Publication).filter(Publication.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Publication not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# CRUD: LANGUAGES
# ==========================================

@app.get("/api/languages")
def list_languages(db: Session = Depends(get_db)):
    return [l.to_dict() for l in db.query(Language).all()]

@app.post("/api/languages", response_model=LanguageResponse)
def create_language(data: LanguageCreate, db: Session = Depends(get_db)):
    item = Language(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.put("/api/languages/{item_id}", response_model=LanguageResponse)
def update_language(item_id: int, data: LanguageCreate, db: Session = Depends(get_db)):
    item = db.query(Language).filter(Language.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Language not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return item

@app.delete("/api/languages/{item_id}")
def delete_language(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Language).filter(Language.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Language not found")
    db.delete(item)
    db.commit()
    export_portfolio_to_file(get_full_portfolio_dict(db))
    return {"message": "Deleted successfully"}

# ==========================================
# GEMINI AI INTELLIGENCE ENDPOINTS
# ==========================================

@app.post("/api/ai/parse-unstructured")
def parse_unstructured(payload: UnstructuredParseRequest):
    key = APP_CONFIG.get("gemini_api_key")
    parsed = parse_unstructured_portfolio(payload.raw_text, custom_key=key)
    return parsed

@app.post("/api/ai/import-unstructured")
def import_unstructured(payload: UnstructuredParseRequest, db: Session = Depends(get_db)):
    key = APP_CONFIG.get("gemini_api_key")
    parsed = parse_unstructured_portfolio(payload.raw_text, custom_key=key)

    # Insert into database
    if parsed.get("profile"):
        prof_data = parsed["profile"]
        prof = db.query(Profile).first()
        if not prof:
            prof = Profile(**prof_data)
            db.add(prof)
        else:
            for k, v in prof_data.items():
                if v:
                    setattr(prof, k, v)

    for e in parsed.get("education", []):
        db.add(Education(**e))

    for s in parsed.get("skills", []):
        db.add(Skill(**s))

    for ex in parsed.get("experiences", []):
        db.add(Experience(**ex))

    for p in parsed.get("projects", []):
        db.add(Project(**p))

    for c in parsed.get("certifications", []):
        db.add(Certification(**c))

    for a in parsed.get("achievements", []):
        db.add(Achievement(**a))

    for pub in parsed.get("publications", []):
        db.add(Publication(**pub))

    for lang in parsed.get("languages", []):
        db.add(Language(**lang))

    db.commit()
    full_data = get_full_portfolio_dict(db)
    export_portfolio_to_file(full_data)
    return {"status": "success", "message": "Parsed data successfully imported to database!"}

@app.post("/api/ai/analyze-jd", response_model=JDAnalysisResponse)
def analyze_jd(payload: JDAnalysisRequest, db: Session = Depends(get_db)):
    full_data = get_full_portfolio_dict(db)
    key = APP_CONFIG.get("gemini_api_key")
    result = analyze_job_description(
        job_description=payload.job_description,
        target_title=payload.target_title,
        portfolio_data=full_data,
        custom_key=key
    )
    return result

@app.post("/api/ai/tailor-summary")
def tailor_summary(payload: TailoredSummaryRequest, db: Session = Depends(get_db)):
    full_data = get_full_portfolio_dict(db)
    key = APP_CONFIG.get("gemini_api_key")
    summary = generate_tailored_summary(
        job_description=payload.job_description,
        target_title=payload.target_title,
        portfolio_data=full_data,
        custom_key=key
    )
    return {"summary": summary}

# ==========================================
# RESUME GENERATION & EXPORT ENDPOINTS
# ==========================================

@app.post("/api/resume/preview")
def preview_resume(payload: ResumeGenerateRequest, db: Session = Depends(get_db)):
    key = APP_CONFIG.get("gemini_api_key")
    resume_data = build_customized_resume_data(
        db=db,
        target_title=payload.target_title,
        job_description=payload.job_description,
        custom_summary=payload.custom_summary,
        selected_project_ids=payload.selected_project_ids,
        selected_skill_ids=payload.selected_skill_ids,
        selected_experience_ids=payload.selected_experience_ids,
        selected_certification_ids=payload.selected_certification_ids,
        selected_achievement_ids=payload.selected_achievement_ids,
        selected_publication_ids=payload.selected_publication_ids,
        gemini_key=key
    )
    return resume_data

@app.post("/api/resume/export-pdf")
def export_pdf(payload: ResumeGenerateRequest, db: Session = Depends(get_db)):
    key = APP_CONFIG.get("gemini_api_key")
    resume_data = build_customized_resume_data(
        db=db,
        target_title=payload.target_title,
        job_description=payload.job_description,
        custom_summary=payload.custom_summary,
        selected_project_ids=payload.selected_project_ids,
        selected_skill_ids=payload.selected_skill_ids,
        selected_experience_ids=payload.selected_experience_ids,
        selected_certification_ids=payload.selected_certification_ids,
        selected_achievement_ids=payload.selected_achievement_ids,
        selected_publication_ids=payload.selected_publication_ids,
        gemini_key=key
    )
    pdf_buffer = generate_pdf_resume(resume_data)
    filename = f"Resume_{payload.target_title.replace(' ', '_')}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/resume/export-docx")
def export_docx(payload: ResumeGenerateRequest, db: Session = Depends(get_db)):
    key = APP_CONFIG.get("gemini_api_key")
    resume_data = build_customized_resume_data(
        db=db,
        target_title=payload.target_title,
        job_description=payload.job_description,
        custom_summary=payload.custom_summary,
        selected_project_ids=payload.selected_project_ids,
        selected_skill_ids=payload.selected_skill_ids,
        selected_experience_ids=payload.selected_experience_ids,
        selected_certification_ids=payload.selected_certification_ids,
        selected_achievement_ids=payload.selected_achievement_ids,
        selected_publication_ids=payload.selected_publication_ids,
        gemini_key=key
    )
    docx_buffer = generate_docx_resume(resume_data)
    filename = f"Resume_{payload.target_title.replace(' ', '_')}.docx"
    return StreamingResponse(
        docx_buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ==========================================
# GOOGLE SHEETS INTEGRATION ENDPOINTS
# ==========================================

@app.get("/api/sheets/export-xlsx")
def download_sheets_xlsx(db: Session = Depends(get_db)):
    full_data = get_full_portfolio_dict(db)
    buffer = export_portfolio_to_bytes(full_data)
    filename = f"Raj_Rasal_Portfolio_GoogleSheets_{full_data.get('profile', {}).get('name', 'Database').replace(' ', '_')}.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/sheets/sync-webhook")
async def sync_sheets_webhook(payload: GoogleSheetSyncRequest, db: Session = Depends(get_db)):
    webhook_url = payload.webhook_url or APP_CONFIG.get("sheets_webhook_url")
    if not webhook_url:
        raise HTTPException(status_code=400, detail="Google Apps Script Webhook URL is required.")
    
    full_data = get_full_portfolio_dict(db)
    result = await sync_to_google_sheets_webhook(webhook_url, full_data)
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result

# ==========================================
# CONFIGURATION & SAMPLE JDS
# ==========================================

@app.post("/api/config/keys")
def set_api_keys(payload: ApiKeyConfigRequest):
    if payload.gemini_api_key is not None:
        APP_CONFIG["gemini_api_key"] = payload.gemini_api_key.strip()
        set_gemini_api_key(payload.gemini_api_key.strip())
    if payload.sheets_webhook_url is not None:
        APP_CONFIG["sheets_webhook_url"] = payload.sheets_webhook_url.strip()
    return {
        "status": "success",
        "gemini_api_key_set": bool(APP_CONFIG["gemini_api_key"]),
        "sheets_webhook_set": bool(APP_CONFIG["sheets_webhook_url"])
    }

@app.get("/api/config/status")
def get_config_status():
    return {
        "gemini_configured": bool(APP_CONFIG.get("gemini_api_key")),
        "sheets_webhook_configured": bool(APP_CONFIG.get("sheets_webhook_url"))
    }

@app.get("/api/sample-jds")
def get_sample_jds():
    return [
        {
            "id": "jd-1",
            "title": "Backend & Distributed Systems Architect",
            "company": "Decentralized Compute Labs",
            "description": (
                "We are seeking an exceptional Backend & Distributed Systems Architect to build high-throughput, "
                "fault-tolerant compute networks. In this role, you will design distributed tensor-sharding pipelines, "
                "orchestrate zero-trust communication protocols, and write low-latency async services in Python, C++, and FastAPI. "
                "Requirements:\n"
                "- Strong understanding of distributed systems architecture, state synchronization, and matrix sharding.\n"
                "- Proficiency in Python (asyncio), C++, socket programming, and RESTful API engineering.\n"
                "- Experience with zero-trust security models, proof-of-compute verification, and mesh networking (Tailscale/WireGuard).\n"
                "- Ability to author rigorous architecture whitepapers and technical specifications.\n"
                "- Track record in competitive hackathons or security vulnerability research is an asset."
            )
        },
        {
            "id": "jd-2",
            "title": "AI Systems & Multi-Agent Infrastructure Engineer",
            "company": "Nexus Agentic Platforms",
            "description": (
                "Join our core AI platform team building next-generation multi-agent execution pipelines and decoupled LLM backends. "
                "You will formulate mediator agent topologies, implement confidence-based intent classification, and build auditable knowledge engines. "
                "Requirements:\n"
                "- Deep technical expertise in multi-agent architecture (mediator patterns, separation of concerns, deadlock prevention).\n"
                "- Practical mastery of Python, FastAPI, background task queues, and LLM prompt chaining.\n"
                "- Experience designing confidence thresholds, intent routing, and conversational fallback disambiguation.\n"
                "- Passion for verifiable ground truth in AI systems and preventing ensemble bias amplification.\n"
                "- Excellent pedagogical communication and cross-functional engineering leadership."
            )
        },
        {
            "id": "jd-3",
            "title": "Security & Systems Infrastructure Engineer",
            "company": "SecureSphere Enterprises",
            "description": (
                "Looking for a Security & Systems Engineer to harden enterprise microservices and zero-trust protocol pipelines. "
                "You will audit system designs, perform vulnerability research, formulate sandboxed execution boundaries, and eliminate access bypasses. "
                "Requirements:\n"
                "- Hands-on background in vulnerability research, threat modeling, and responsible security disclosures (HackerOne).\n"
                "- Knowledge of zero-trust architecture, cryptographic identity assertions, and Firecracker microVM sandboxing.\n"
                "- High proficiency in Python, Linux systems, network security protocols, and secure code review.\n"
                "- Demonstrated ability to produce end-to-end security architecture specifications and audit trails."
            )
        }
    ]

# Mount static directory for frontend single page app
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Portfolio Application API running. index.html not yet created."}
