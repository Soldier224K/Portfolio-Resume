from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.database import (
    Profile, Education, Skill, Experience, Project,
    Certification, Achievement, Publication, Language
)
from app.gemini_service import generate_tailored_summary
from app.pdf_generator import generate_pdf_resume
from app.docx_generator import generate_docx_resume

def build_customized_resume_data(
    db: Session,
    target_title: str,
    job_description: Optional[str] = None,
    custom_summary: Optional[str] = None,
    selected_project_ids: Optional[List[int]] = None,
    selected_skill_ids: Optional[List[int]] = None,
    selected_experience_ids: Optional[List[int]] = None,
    selected_certification_ids: Optional[List[int]] = None,
    selected_achievement_ids: Optional[List[int]] = None,
    selected_publication_ids: Optional[List[int]] = None,
    gemini_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Build a verified, customized resume payload from the portfolio database.
    Strictly verifies all items exist in the database.
    """
    profile_obj = db.query(Profile).first()
    profile = profile_obj.to_dict() if profile_obj else {}

    # Education (include all formal education)
    educations = [e.to_dict() for e in db.query(Education).all()]

    # Skills filtering
    all_skills = db.query(Skill).all()
    if selected_skill_ids is not None:
        sel_set = set(selected_skill_ids)
        filtered_skills = [s.to_dict() for s in all_skills if s.id in sel_set]
    else:
        filtered_skills = [s.to_dict() for s in all_skills if s.is_highlighted]

    # Projects filtering
    all_projects = db.query(Project).all()
    if selected_project_ids is not None:
        sel_p_set = set(selected_project_ids)
        filtered_projects = [p.to_dict() for p in all_projects if p.id in sel_p_set]
    else:
        filtered_projects = [p.to_dict() for p in all_projects if p.is_featured]

    # Experience filtering
    all_exp = db.query(Experience).all()
    if selected_experience_ids is not None:
        sel_e_set = set(selected_experience_ids)
        filtered_exp = [e.to_dict() for e in all_exp if e.id in sel_e_set]
    else:
        filtered_exp = [e.to_dict() for e in all_exp]

    # Certifications filtering
    all_certs = db.query(Certification).all()
    if selected_certification_ids is not None:
        sel_c_set = set(selected_certification_ids)
        filtered_certs = [c.to_dict() for c in all_certs if c.id in sel_c_set]
    else:
        filtered_certs = [c.to_dict() for c in all_certs]

    # Achievements filtering
    all_ach = db.query(Achievement).all()
    if selected_achievement_ids is not None:
        sel_a_set = set(selected_achievement_ids)
        filtered_ach = [a.to_dict() for a in all_ach if a.id in sel_a_set]
    else:
        filtered_ach = [a.to_dict() for a in all_ach]

    # Publications filtering
    all_pubs = db.query(Publication).all()
    if selected_publication_ids is not None:
        sel_pub_set = set(selected_publication_ids)
        filtered_pubs = [pub.to_dict() for pub in all_pubs if pub.id in sel_pub_set]
    else:
        filtered_pubs = [pub.to_dict() for pub in all_pubs]

    # Languages
    languages = [l.to_dict() for l in db.query(Language).all()]

    # Summary resolution:
    # If custom_summary is provided by user, use it.
    # If not, but JD is provided, tailor with Gemini/verifier.
    # Otherwise use profile's default summary.
    final_summary = custom_summary
    if not final_summary and job_description:
        portfolio_ground_truth = {
            "profile": profile,
            "education": educations,
            "skills": filtered_skills,
            "projects": filtered_projects,
            "experiences": filtered_exp,
            "publications": filtered_pubs
        }
        final_summary = generate_tailored_summary(
            job_description=job_description,
            target_title=target_title,
            portfolio_data=portfolio_ground_truth,
            custom_key=gemini_key
        )
    elif not final_summary:
        final_summary = profile.get("summary", "")

    return {
        "target_title": target_title,
        "custom_summary": final_summary,
        "profile": profile,
        "education": educations,
        "skills": filtered_skills,
        "projects": filtered_projects,
        "experiences": filtered_exp,
        "certifications": filtered_certs,
        "achievements": filtered_ach,
        "publications": filtered_pubs,
        "languages": languages
    }

