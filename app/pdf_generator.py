import os
import io
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

def generate_pdf_resume(resume_data: Dict[str, Any], output_path: str = None) -> io.BytesIO:
    """
    Generate a clean, ATS-compliant, professional PDF resume.
    Adheres strictly to typography and structure expected by corporate ATS systems.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        output_path if output_path else buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom ATS typography styles
    style_name = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=0, # Left-aligned for modern ATS standard
        spaceAfter=3
    )

    style_target_title = ParagraphStyle(
        'ResumeTargetTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563EB'), # Indigo/Blue
        spaceAfter=4
    )

    style_contact = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    style_section_heading = ParagraphStyle(
        'ResumeSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=7,
        spaceAfter=2,
        textTransform='uppercase'
    )

    style_item_title = ParagraphStyle(
        'ResumeItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )

    style_item_sub = ParagraphStyle(
        'ResumeItemSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    style_body = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=2
    )

    style_bullet = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=1.5
    )

    story = []

    profile = resume_data.get("profile", {})
    target_title = resume_data.get("target_title", profile.get("title", ""))
    
    # 1. Header: Name & Target Title
    story.append(Paragraph(profile.get("name", "Raj Bharat Rasal").upper(), style_name))
    if target_title:
        story.append(Paragraph(target_title, style_target_title))

    # Contact line
    contact_parts = []
    if profile.get("location"):
        contact_parts.append(profile["location"])
    if profile.get("phone"):
        contact_parts.append(profile["phone"])
    if profile.get("email"):
        contact_parts.append(profile["email"])
    if profile.get("linkedin"):
        clean_li = profile["linkedin"].replace("https://", "").replace("http://", "")
        contact_parts.append(clean_li)
    if profile.get("github"):
        clean_gh = profile["github"].replace("https://", "").replace("http://", "")
        contact_parts.append(clean_gh)

    contact_line = "  |  ".join(contact_parts)
    story.append(Paragraph(contact_line, style_contact))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=0))

    # 2. Professional Summary
    summary = resume_data.get("custom_summary") or profile.get("summary")
    if summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        story.append(Paragraph(summary, style_body))
        story.append(Spacer(1, 3))

    # 3. Technical Skills
    skills = resume_data.get("skills", [])
    if skills:
        story.append(Paragraph("TECHNICAL & ARCHITECTURAL SKILLS", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        
        # Group skills by category
        categories = {}
        for s in skills:
            cat = s.get("category", "General")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(s["name"])

        for cat, skill_names in categories.items():
            cat_text = f"<b>{cat}:</b> {', '.join(skill_names)}"
            story.append(Paragraph(cat_text, style_body))
        story.append(Spacer(1, 3))

    # 4. Featured Projects
    projects = resume_data.get("projects", [])
    if projects:
        story.append(Paragraph("FEATURED SYSTEMS & PROJECTS", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        
        for p in projects:
            title_text = f"<b>{p.get('title')}</b> — {p.get('subtitle_role', '')}"
            date_text = f"{p.get('start_date', '')} - {p.get('end_date', 'Present')}" if p.get('start_date') else ""
            
            # Use 2-column table for header to align dates right
            t_data = [[
                Paragraph(title_text, style_item_title),
                Paragraph(date_text, ParagraphStyle('RightDate', parent=style_item_sub, alignment=2))
            ]]
            t = Table(t_data, colWidths=[420, 120])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(t)

            if p.get("tech_stack"):
                story.append(Paragraph(f"<i>Tech Stack: {p.get('tech_stack')}</i>", style_item_sub))

            # Bullets
            desc = p.get("description", "")
            bullets = [b.strip() for b in desc.split("\n") if b.strip()]
            for b in bullets:
                clean_b = b.lstrip("•-* ").strip()
                story.append(Paragraph(f"• {clean_b}", style_bullet))

            if p.get("architecture_highlights"):
                story.append(Paragraph(f"• <b>Key Architecture:</b> {p.get('architecture_highlights')}", style_bullet))

            story.append(Spacer(1, 2))

    # 5. Experience
    experiences = resume_data.get("experiences", [])
    if experiences:
        story.append(Paragraph("EXPERIENCE & LEADERSHIP", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        
        for exp in experiences:
            exp_title = f"<b>{exp.get('company')}</b> — {exp.get('role')}"
            exp_date = f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}"
            
            t_data = [[
                Paragraph(exp_title, style_item_title),
                Paragraph(exp_date, ParagraphStyle('RightDateExp', parent=style_item_sub, alignment=2))
            ]]
            t = Table(t_data, colWidths=[420, 120])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(t)

            bullets = [b.strip() for b in exp.get("description", "").split("\n") if b.strip()]
            for b in bullets:
                clean_b = b.lstrip("•-* ").strip()
                story.append(Paragraph(f"• {clean_b}", style_bullet))

            story.append(Spacer(1, 2))

    # 6. Publications / Whitepapers
    publications = resume_data.get("publications", [])
    if publications:
        story.append(Paragraph("SYSTEM DESIGN SPECIFICATIONS & WHITEPAPERS", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        
        for pub in publications:
            pub_title = f"<b>{pub.get('title')}</b> ({pub.get('venue_type')}, {pub.get('publication_date', '')})"
            story.append(Paragraph(pub_title, style_item_title))
            if pub.get("abstract"):
                story.append(Paragraph(f"• {pub.get('abstract')}", style_bullet))
            story.append(Spacer(1, 2))

    # 7. Education
    education = resume_data.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        
        for edu in education:
            edu_title = f"<b>{edu.get('institution')}</b> — {edu.get('degree')}"
            edu_date = f"{edu.get('start_year', '')} - {edu.get('end_year', '')}"
            
            t_data = [[
                Paragraph(edu_title, style_item_title),
                Paragraph(edu_date, ParagraphStyle('RightDateEdu', parent=style_item_sub, alignment=2))
            ]]
            t = Table(t_data, colWidths=[420, 120])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(t)

            details = []
            if edu.get("field_of_study"):
                details.append(f"Field: {edu.get('field_of_study')}")
            if edu.get("score"):
                details.append(f"Score: {edu.get('score')}")
            if details:
                story.append(Paragraph(" | ".join(details), style_item_sub))
            if edu.get("highlights"):
                story.append(Paragraph(f"• {edu.get('highlights')}", style_bullet))

            story.append(Spacer(1, 2))

    # 8. Achievements & Awards
    achievements = resume_data.get("achievements", [])
    if achievements:
        story.append(Paragraph("ACHIEVEMENTS & SECURITY RESEARCH", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        for a in achievements:
            ach_text = f"• <b>{a.get('title')}:</b> {a.get('description')}"
            story.append(Paragraph(ach_text, style_bullet))
        story.append(Spacer(1, 2))

    # 9. Certifications
    certifications = resume_data.get("certifications", [])
    if certifications:
        story.append(Paragraph("CERTIFICATIONS & ACCREDITATIONS", style_section_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=1))
        for c in certifications:
            cert_text = f"• <b>{c.get('name')}</b> — {c.get('issuing_org')} ({c.get('issue_date')})"
            story.append(Paragraph(cert_text, style_bullet))

    doc.build(story)
    buffer.seek(0)
    return buffer

