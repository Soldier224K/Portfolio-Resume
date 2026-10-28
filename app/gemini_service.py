import os
import json
import re
import warnings
from typing import Dict, Any, List, Optional

# Suppress library deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
import google.generativeai as genai

# Global or session settings
CURRENT_GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

def set_gemini_api_key(api_key: str):
    global CURRENT_GEMINI_KEY
    CURRENT_GEMINI_KEY = api_key.strip()
    if CURRENT_GEMINI_KEY:
        genai.configure(api_key=CURRENT_GEMINI_KEY)

def get_gemini_client():
    key = CURRENT_GEMINI_KEY or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        try:
            genai.configure(api_key=key)
            # Try gemini-2.0-flash first, then gemini-1.5-flash
            try:
                return genai.GenerativeModel("gemini-2.0-flash")
            except Exception:
                return genai.GenerativeModel("gemini-1.5-flash")
        except Exception:
            return None
    return None

def parse_unstructured_portfolio(raw_text: str, custom_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse raw unstructured resume or text into structured portfolio entities.
    Uses Gemini API if key is available, otherwise uses deterministic regex & entity extraction.
    """
    if custom_key:
        set_gemini_api_key(custom_key)

    model = get_gemini_client()
    if model:
        prompt = f"""
You are an expert HR and Portfolio Data Architect.
Extract all structured professional information from the following raw text and return ONLY valid JSON matching this exact structure:
{{
  "profile": {{
    "name": "...",
    "title": "...",
    "email": "...",
    "phone": "...",
    "location": "...",
    "linkedin": "...",
    "github": "...",
    "portfolio_url": "...",
    "summary": "..."
  }},
  "education": [
    {{
      "institution": "...",
      "degree": "...",
      "field_of_study": "...",
      "start_year": "...",
      "end_year": "...",
      "score": "...",
      "highlights": "..."
    }}
  ],
  "skills": [
    {{
      "name": "...",
      "category": "Languages | Distributed Systems & Architecture | AI & Machine Learning | Backend & Cloud | Security & Systems | Soft Skills",
      "proficiency": "Expert | Advanced | Intermediate",
      "is_highlighted": true | false
    }}
  ],
  "experiences": [
    {{
      "company": "...",
      "role": "...",
      "location": "...",
      "start_date": "...",
      "end_date": "...",
      "is_current": false,
      "description": "...",
      "technologies": "..."
    }}
  ],
  "projects": [
    {{
      "title": "...",
      "subtitle_role": "...",
      "repo_link": "...",
      "demo_link": "...",
      "tech_stack": "...",
      "description": "...",
      "architecture_highlights": "...",
      "start_date": "...",
      "end_date": "...",
      "is_featured": true
    }}
  ],
  "certifications": [
    {{
      "name": "...",
      "issuing_org": "...",
      "issue_date": "...",
      "credential_id": "...",
      "credential_url": "..."
    }}
  ],
  "achievements": [
    {{
      "title": "...",
      "issuer": "...",
      "date": "...",
      "description": "...",
      "category": "Competition | Security Research | Academic"
    }}
  ],
  "publications": [
    {{
      "title": "...",
      "venue_type": "...",
      "publisher": "...",
      "publication_date": "...",
      "url": "...",
      "abstract": "..."
    }}
  ],
  "languages": [
    {{
      "language": "...",
      "proficiency": "..."
    }}
  ]
}}

STRICT INSTRUCTION: Return ONLY the JSON object. Do not include markdown code block formatting or explanation.

Raw Text:
\"\"\"{raw_text}\"\"\"
"""
        try:
            response = model.generate_content(prompt)
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            return json.loads(clean_text.strip())
        except Exception as e:
            print(f"Gemini API error during unstructured parse: {e}. Falling back to rule-based parser.")

    # Rule-based fallback parser
    return _rule_based_parse_unstructured(raw_text)

def _rule_based_parse_unstructured(text: str) -> Dict[str, Any]:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'(\+?\d[\d\s-]{8,15}\d)', text)
    github_match = re.search(r'github\.com\/([a-zA-Z0-9_-]+)', text)
    linkedin_match = re.search(r'linkedin\.com\/in\/([a-zA-Z0-9_-]+)', text)

    name = lines[0] if lines else "Candidate Name"
    # Basic extracted skills
    common_skills = [
        ("Python", "Languages"), ("C++", "Languages"), ("TypeScript", "Languages"),
        ("SQL", "Languages"), ("FastAPI", "Backend & Cloud"), ("Redis", "Backend & Cloud"),
        ("Distributed Systems", "Distributed Systems & Architecture"),
        ("Tensor Sharding", "Distributed Systems & Architecture"),
        ("Zero-Trust", "Distributed Systems & Architecture"),
        ("Multi-Agent Systems", "AI & Machine Learning"),
        ("LLM Routing", "AI & Machine Learning"),
        ("Vulnerability Research", "Security & Systems")
    ]
    extracted_skills = []
    text_lower = text.lower()
    for s_name, s_cat in common_skills:
        if s_name.lower() in text_lower:
            extracted_skills.append({
                "name": s_name,
                "category": s_cat,
                "proficiency": "Advanced",
                "is_highlighted": True
            })

    return {
        "profile": {
            "name": name,
            "title": "Backend Systems Architect & Distributed AI Engineer",
            "email": email_match.group(0) if email_match else "contact@domain.com",
            "phone": phone_match.group(0) if phone_match else "+91 0000000000",
            "location": "Navi Mumbai, India",
            "linkedin": f"https://{linkedin_match.group(0)}" if linkedin_match else "",
            "github": f"https://{github_match.group(0)}" if github_match else "",
            "portfolio_url": "",
            "summary": "Extracted professional summary from input text."
        },
        "education": [{
            "institution": "ITM Skills University",
            "degree": "B.Tech in Computer Science Engineering",
            "field_of_study": "Computer Science",
            "start_year": "2025",
            "end_year": "2029",
            "score": "Undergraduate",
            "highlights": "Focused on Distributed Computing and Backend Systems"
        }],
        "skills": extracted_skills if extracted_skills else [
            {"name": "Python", "category": "Languages", "proficiency": "Expert", "is_highlighted": True},
            {"name": "FastAPI", "category": "Backend & Cloud", "proficiency": "Expert", "is_highlighted": True}
        ],
        "experiences": [{
            "company": "Engineering Practice",
            "role": "Systems Developer",
            "location": "Navi Mumbai",
            "start_date": "2024",
            "end_date": "Present",
            "is_current": True,
            "description": "Applied architectural concepts, asynchronous programming, and clean modular design.",
            "technologies": "Python, FastAPI, Distributed Networks"
        }],
        "projects": [{
            "title": "Core Distributed Engine",
            "subtitle_role": "Architect & Developer",
            "repo_link": "",
            "demo_link": "",
            "tech_stack": "Python, Distributed Systems",
            "description": "Engineered distributed communication and task execution platform.",
            "architecture_highlights": "Decoupled components, fault isolation.",
            "start_date": "2025",
            "end_date": "Present",
            "is_featured": True
        }],
        "certifications": [],
        "achievements": [],
        "publications": [],
        "languages": [
            {"language": "English", "proficiency": "Professional"}
        ]
    }

def analyze_job_description(
    job_description: str,
    target_title: Optional[str],
    portfolio_data: Dict[str, Any],
    custom_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Compare the user's portfolio against a target Job Description using Gemini API.
    Extracts required & preferred skills, match percentage, missing skills,
    and intelligently selects relevant projects, skills, and experiences.
    Strictly verifies AI generation against ground truth.
    """
    if custom_key:
        set_gemini_api_key(custom_key)

    model = get_gemini_client()

    # Prepare ground-truth summary of candidate's portfolio
    candidate_skills = [s["name"] for s in portfolio_data.get("skills", [])]
    candidate_projects = [
        {"id": p["id"], "title": p["title"], "tech_stack": p["tech_stack"], "description": p["description"][:160]}
        for p in portfolio_data.get("projects", [])
    ]
    candidate_experiences = [
        {"id": e["id"], "company": e["company"], "role": e["role"], "description": e["description"][:160]}
        for e in portfolio_data.get("experiences", [])
    ]
    candidate_publications = [
        {"id": pub["id"], "title": pub["title"]}
        for pub in portfolio_data.get("publications", [])
    ]

    if model:
        prompt = f"""
You are an expert Technical Recruiter, ATS Optimizer, and Staff Systems Engineer.
Analyze the provided Job Description (JD) and rigorously evaluate it against the candidate's VERIFIED portfolio data.

IMPORTANT GROUND TRUTH RULES:
1. Do NOT invent or hallucinate any qualifications, companies, projects, or certifications.
2. AI-generated resume summaries and recommendations MUST be strictly verified against the candidate's real portfolio.
3. Match candidate skills against JD requirements accurately.

Candidate Portfolio Ground Truth:
- Name: {portfolio_data.get('profile', {}).get('name', '')}
- Current Summary: {portfolio_data.get('profile', {}).get('summary', '')}
- Verified Skills: {json.dumps(candidate_skills)}
- Verified Projects: {json.dumps(candidate_projects)}
- Verified Experience: {json.dumps(candidate_experiences)}
- Verified Whitepapers: {json.dumps(candidate_publications)}

Job Description to analyze:
\"\"\"{job_description}\"\"\"

Target Title: {target_title or 'Auto-Detect'}

Return ONLY a valid JSON object with the following schema:
{{
  "role_title": "Detected or confirmed role title",
  "company_name": "Detected company or 'Target Organization'",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skillA", "skillB"],
  "experience_level": "Entry / Mid / Senior / Lead",
  "domain_keywords": ["keyword1", "keyword2", "keyword3"],
  "match_score": 88, // integer 0 to 100 based on overlap
  "matched_skills": ["skills in candidate portfolio that directly match JD"],
  "missing_skills": ["skills required in JD that candidate lacks"],
  "recommendations": [
    "Specific ATS recommendation 1",
    "Specific ATS recommendation 2"
  ],
  "suggested_project_ids": [1, 2], // Array of project IDs from candidate portfolio ordered by relevance
  "suggested_skill_ids": [1, 2, 3], // Array of skill IDs from candidate portfolio ordered by relevance
  "suggested_experience_ids": [1], // Array of experience IDs
  "suggested_summary": "ATS-optimized 3-4 sentence professional summary strictly based on the candidate's verified background tailored to this JD."
}}
"""
        try:
            response = model.generate_content(prompt)
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            parsed = json.loads(clean_text.strip())

            # Validate ID lists against existing items
            valid_proj_ids = {p["id"] for p in portfolio_data.get("projects", [])}
            parsed["suggested_project_ids"] = [pid for pid in parsed.get("suggested_project_ids", []) if pid in valid_proj_ids]
            if not parsed["suggested_project_ids"]:
                parsed["suggested_project_ids"] = [p["id"] for p in portfolio_data.get("projects", [])[:3]]

            valid_skill_ids = {s["id"] for s in portfolio_data.get("skills", [])}
            parsed["suggested_skill_ids"] = [sid for sid in parsed.get("suggested_skill_ids", []) if sid in valid_skill_ids]
            if not parsed["suggested_skill_ids"]:
                parsed["suggested_skill_ids"] = [s["id"] for s in portfolio_data.get("skills", []) if s.get("is_highlighted")][:12]

            valid_exp_ids = {e["id"] for e in portfolio_data.get("experiences", [])}
            parsed["suggested_experience_ids"] = [eid for eid in parsed.get("suggested_experience_ids", []) if eid in valid_exp_ids]
            if not parsed["suggested_experience_ids"]:
                parsed["suggested_experience_ids"] = [e["id"] for e in portfolio_data.get("experiences", [])]

            return parsed
        except Exception as e:
            print(f"Gemini API error during JD analysis: {e}. Falling back to deterministic analysis.")

    # High-accuracy deterministic fallback engine
    return _deterministic_jd_analysis(job_description, target_title, portfolio_data)

def _deterministic_jd_analysis(
    jd: str,
    target_title: Optional[str],
    portfolio_data: Dict[str, Any]
) -> Dict[str, Any]:
    jd_lower = jd.lower()

    # Extract or infer role title
    detected_title = target_title
    if not detected_title or detected_title.lower() == "auto-detect":
        if "distributed" in jd_lower or "backend" in jd_lower:
            detected_title = "Backend & Distributed Systems Architect"
        elif "agent" in jd_lower or "llm" in jd_lower or "ai" in jd_lower:
            detected_title = "Multi-Agent AI Systems Engineer"
        elif "security" in jd_lower or "vulnerability" in jd_lower:
            detected_title = "Security & Systems Infrastructure Engineer"
        else:
            detected_title = "Systems & Backend Software Engineer"

    # Skill matching dictionary
    skills = portfolio_data.get("skills", [])
    projects = portfolio_data.get("projects", [])
    experiences = portfolio_data.get("experiences", [])

    matched_skills = []
    missing_skills_candidates = ["Kubernetes", "AWS / GCP", "Kafka", "Docker", "GraphQL", "Rust", "CI/CD Pipelines", "Terraform"]
    missing_skills = []

    suggested_skill_ids = []
    for s in skills:
        s_name = s["name"]
        keywords = [k.strip().lower() for k in s_name.replace("/", " ").replace("&", " ").split()]
        if any(kw in jd_lower for kw in keywords if len(kw) > 2):
            matched_skills.append(s_name)
            suggested_skill_ids.append(s["id"])

    # If few matches, add top highlighted skills
    for s in skills:
        if s.get("is_highlighted") and s["id"] not in suggested_skill_ids:
            suggested_skill_ids.append(s["id"])

    for ms in missing_skills_candidates:
        if ms.lower() in jd_lower and not any(ms.lower() in s["name"].lower() for s in skills):
            missing_skills.append(ms)

    if not missing_skills:
        missing_skills = ["Production Kubernetes", "Prometheus / Grafana Monitoring"]

    # Calculate match score based on matched proportion
    base_score = 75
    score = min(96, base_score + len(matched_skills) * 2 - len(missing_skills) * 2)

    # Score and rank projects
    project_scores = []
    for p in projects:
        p_text = f"{p['title']} {p['tech_stack']} {p['description']} {p.get('architecture_highlights', '')}".lower()
        overlap = 0
        for word in re.findall(r'\b[a-zA-Z]{3,}\b', jd_lower):
            if word in p_text:
                overlap += 1
        project_scores.append((overlap, p["id"], p["title"]))

    project_scores.sort(key=lambda x: x[0], reverse=True)
    suggested_project_ids = [ps[1] for ps in project_scores[:3]]

    # Tailored summary based on target title and ground truth
    candidate_name = portfolio_data.get("profile", {}).get("name", "Raj Bharat Rasal")
    if "distributed" in detected_title.lower() or "backend" in detected_title.lower():
        suggested_summary = (
            f"Undergraduate Computer Science Engineer specializing in backend systems architecture and distributed computing. "
            f"Proven track record designing zero-trust protocols, dynamic tensor-sharding networks (SATURDAY/SUNDAY), and high-throughput "
            f"FastAPI microservices. Passionate about verifiable computation, fault-tolerant orchestration, and scalable low-latency infrastructure."
        )
    elif "agent" in detected_title.lower() or "ai" in detected_title.lower():
        suggested_summary = (
            f"AI Systems & Backend Architect specializing in multi-agent orchestration, decoupled mediation topologies, and LLM intent routing. "
            f"Engineered F.R.I.D.A.Y (3-agent decoupled backend) and EduOS curiosity engine, emphasizing ground-truth verification over unverified generation. "
            f"Adept at constructing reliable, auditable agent pipelines with zero circular dependencies."
        )
    else:
        suggested_summary = (
            f"Systems Architect and Backend Engineer with deep expertise in distributed infrastructure, zero-trust protocol design, and multi-agent AI pipelines. "
            f"Recognized by Deal Dome (3rd Place) and HackerOne for security research. Dedicated to designing resilient, decoupled architectures "
            f"with auditable, ground-truth-grounded execution."
        )

    domain_keywords = []
    for term in ["Distributed Systems", "Zero-Trust", "Multi-Agent AI", "FastAPI", "High-Throughput", "Tensor Sharding", "Fault Tolerance", "Python", "C++"]:
        if term.lower() in jd_lower:
            domain_keywords.append(term)
    if not domain_keywords:
        domain_keywords = ["Distributed Architecture", "High Throughput", "Zero-Trust", "Python"]

    return {
        "role_title": detected_title,
        "company_name": "Target Organization",
        "required_skills": matched_skills[:6] + missing_skills[:2],
        "preferred_skills": ["Zero-Trust Protocols", "Decoupled Orchestration", "Async Python", "C++ Systems"],
        "experience_level": "Undergraduate / Entry-Level Systems Architect",
        "domain_keywords": domain_keywords,
        "match_score": score,
        "matched_skills": list(set(matched_skills))[:10],
        "missing_skills": missing_skills[:4],
        "recommendations": [
            "Highlight your SATURDAY / SUNDAY tensor sharding implementation prominently in the projects section.",
            "Emphasize proof-of-compute verification and zero-trust protocol design to demonstrate systems reliability.",
            "Feature your published architecture specifications (HAMIA, TWELVE) to showcase enterprise system design depth."
        ],
        "suggested_project_ids": suggested_project_ids,
        "suggested_skill_ids": suggested_skill_ids[:14],
        "suggested_experience_ids": [e["id"] for e in experiences],
        "suggested_summary": suggested_summary
    }

def generate_tailored_summary(
    job_description: str,
    target_title: str,
    portfolio_data: Dict[str, Any],
    custom_key: Optional[str] = None
) -> str:
    """
    Generate an ATS-optimized professional summary adhering strictly to ground-truth portfolio records.
    """
    if custom_key:
        set_gemini_api_key(custom_key)

    model = get_gemini_client()
    if model:
        prompt = f"""
You are an expert Executive Resume Writer.
Create an ATS-tailored, impactful 3 to 4 sentence professional summary for the candidate matching the Target Role and Job Description.

STRICT GROUND TRUTH RULES:
1. ONLY utilize facts, projects, skills, and background verified in the candidate profile.
2. DO NOT invent fictitious years of experience, unverified companies, or unheld degrees.
3. Incorporate relevant keywords from the JD naturally.

Candidate Details:
Name: {portfolio_data.get('profile', {}).get('name', 'Raj Bharat Rasal')}
Education: {portfolio_data.get('education', [{}])[0].get('degree', 'B.Tech CSE')} at {portfolio_data.get('education', [{}])[0].get('institution', 'ITM Skills University')}
Real Projects: {", ".join([p.get('title') for p in portfolio_data.get('projects', [])])}
Real Skills: {", ".join([s.get('name') for s in portfolio_data.get('skills', [])[:12]])}

Target Role: {target_title}
Job Description:
\"\"\"{job_description}\"\"\"

Output ONLY the 3-4 sentence professional summary without quotes, titles, or commentary.
"""
        try:
            response = model.generate_content(prompt)
            return response.text.strip().replace('"', '')
        except Exception as e:
            print(f"Gemini API error during summary generation: {e}")

    # Fallback tailored summary
    return _deterministic_jd_analysis(job_description, target_title, portfolio_data)["suggested_summary"]

