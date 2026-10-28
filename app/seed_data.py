from sqlalchemy.orm import Session
from app.database import (
    Profile, Education, Skill, Experience, Project,
    Certification, Achievement, Publication, Language
)

def seed_portfolio_data(db: Session, force: bool = False):
    """Seed the database with Raj Bharat Rasal's complete verified portfolio records."""
    if not force and db.query(Profile).first():
        return  # Already seeded

    # Clear existing if force
    if force:
        for model in [Profile, Education, Skill, Experience, Project, Certification, Achievement, Publication, Language]:
            db.query(model).delete()
        db.commit()

    # 1. Profile
    profile = Profile(
        name="Raj Bharat Rasal",
        title="Backend Systems Architect & Distributed AI Engineer",
        email="rajrasal0806@gmail.com",
        phone="+91 8766028985",
        location="Kharghar, Navi Mumbai, India",
        linkedin="https://linkedin.com/in/cyber-monk",
        github="https://github.com/Soldier224K",
        portfolio_url="https://rajrasal.dev",
        summary=(
            "Second-year B.Tech student focused on backend systems architecture, distributed computing, "
            "and multi-agent AI pipelines. I design and build complex infrastructure from the ground up—currently "
            "developing a distributed tensor-sharding network and a multi-agent communication system—prioritizing "
            "system design, integration logic, and scalable architecture."
        )
    )
    db.add(profile)

    # 2. Education
    db.add_all([
        Education(
            institution="ITM Skills University",
            degree="Bachelor of Technology (B.Tech)",
            field_of_study="Computer Science Engineering",
            start_year="Aug 2025",
            end_year="May 2029",
            score="Undergraduate (In Progress)",
            highlights="Specializing in Distributed Systems, Operating Systems, Computer Networks, and AI Systems Design. Active contributor to student engineering and hackathon teams."
        ),
        Education(
            institution="Central Board of Secondary Education (CBSE)",
            degree="Higher Secondary Certificate (12th Grade)",
            field_of_study="Science (PCM)",
            start_year="2023",
            end_year="2025",
            score="83.4%",
            highlights="Strong foundation in advanced calculus, mechanics, electromagnetic physics, and algorithmic logic."
        ),
        Education(
            institution="Central Board of Secondary Education (CBSE)",
            degree="Secondary School Examination (10th Grade)",
            field_of_study="General Science & Mathematics",
            start_year="2021",
            end_year="2023",
            score="96.0%",
            highlights="Academic excellence award in Mathematics and Science."
        )
    ])

    # 3. Skills
    skills_data = [
        # Languages
        ("Python", "Languages", "Expert", True),
        ("C++", "Languages", "Advanced", True),
        ("TypeScript / JavaScript", "Languages", "Advanced", True),
        ("SQL (PostgreSQL, SQLite)", "Languages", "Advanced", True),
        ("Bash / Shell Scripting", "Languages", "Advanced", False),

        # Distributed Systems & Architecture
        ("Distributed Systems Architecture", "Distributed Systems & Architecture", "Expert", True),
        ("Tensor Sharding & Compute Networks", "Distributed Systems & Architecture", "Expert", True),
        ("Decoupled Orchestration", "Distributed Systems & Architecture", "Expert", True),
        ("Zero-Trust Communication Protocols", "Distributed Systems & Architecture", "Expert", True),
        ("Proof-of-Compute Verification", "Distributed Systems & Architecture", "Advanced", True),
        ("System Design & Scalability", "Distributed Systems & Architecture", "Expert", True),

        # AI & Machine Learning
        ("Multi-Agent AI Pipelines", "AI & Machine Learning", "Expert", True),
        ("LLM Intent Classification & Routing", "AI & Machine Learning", "Expert", True),
        ("Prompt Engineering & Chains", "AI & Machine Learning", "Advanced", True),
        ("RAG & Ground Truth Verification", "AI & Machine Learning", "Advanced", True),
        ("Adversarial Critic Systems", "AI & Machine Learning", "Advanced", True),

        # Backend & Cloud Infrastructure
        ("FastAPI", "Backend & Cloud", "Expert", True),
        ("RESTful API Design", "Backend & Cloud", "Expert", True),
        ("Asynchronous Programming (asyncio)", "Backend & Cloud", "Expert", True),
        ("APScheduler & Task Queues", "Backend & Cloud", "Advanced", False),
        ("Tailscale VPN & Mesh Networking", "Backend & Cloud", "Advanced", False),
        ("Redis Streams & Message Passing", "Backend & Cloud", "Advanced", False),

        # Security & Systems Research
        ("Vulnerability Research & Bug Bounty", "Security & Systems", "Advanced", True),
        ("Zero-Trust Data Flow Verification", "Security & Systems", "Advanced", True),
        ("Sandboxing & Isolation (Firecracker)", "Security & Systems", "Advanced", False),

        # Soft Skills
        ("Technical Architecture Documentation", "Soft Skills", "Expert", True),
        ("Conceptual Simplification", "Soft Skills", "Expert", True),
        ("Problem Decomposition", "Soft Skills", "Expert", True),
        ("Cross-Team Technical Leadership", "Soft Skills", "Advanced", False),
    ]
    for name, cat, prof, high in skills_data:
        db.add(Skill(name=name, category=cat, proficiency=prof, is_highlighted=high))

    # 4. Experience
    db.add(Experience(
        company="Independent Tutoring Practice",
        role="Mathematics & Physics Tutor (Grades 10–12)",
        location="Navi Mumbai, India",
        start_date="Jun 2024",
        end_date="Present",
        is_current=True,
        description=(
            "Taught 50+ high school students, translating complex scientific, mathematical, and algorithmic concepts into clear, structured lessons.\n"
            "Developed diagnostic assessment frameworks to identify conceptual bottlenecks and tailored individual curricula to improve performance by an average of 22%.\n"
            "Honed mastery of first-principles thinking, communication clarity, and pedagogical system design."
        ),
        technologies="Calculus, Mechanics, First-Principles Reasoning, Pedagogical System Design"
    ))

    # 5. Projects
    db.add_all([
        Project(
            title="SATURDAY / SUNDAY",
            subtitle_role="Architect & Lead Developer",
            repo_link="https://github.com/Soldier224K/saturday-compute",
            demo_link="https://rajrasal.dev/projects/saturday",
            tech_stack="Python, C++, Tensor Sharding, Zero-Trust Protocols, LAN, Tailscale VPN, Socket Programming",
            description=(
                "Built a distributed compute network to run large local LLMs, solving hardware limitations of processing complex AI models on single devices.\n"
                "Implemented automatic hardware discovery and dynamic tensor sharding to split a single model's processing across heterogeneous Mac and Windows nodes via LAN and Tailscale VPN mesh.\n"
                "Designed a zero-trust communication protocol between nodes, utilizing proof-of-compute verification to detect and reject nodes returning corrupted or falsified matrix calculation results."
            ),
            architecture_highlights=(
                "Decoupled coordinator-worker model with heartbeats; distributed matrix multiplication with Tailscale mesh tunnels; sub-millisecond node health checks; Byzantine fault tolerance through spot verification."
            ),
            start_date="Jan 2026",
            end_date="Present",
            is_featured=True
        ),
        Project(
            title="F.R.I.D.A.Y — Multi-Agent Communication Backend",
            subtitle_role="Lead Backend Architect & Developer",
            repo_link="https://github.com/Soldier224K/friday-agent-backend",
            demo_link="https://rajrasal.dev/projects/friday",
            tech_stack="Python, FastAPI, Baileys API (WhatsApp), APScheduler, asyncio, LLM Intent Routing",
            description=(
                "Originated at SummerHacks 2026 in a team of 4; currently driving continuous backend evolution and multi-agent infrastructure.\n"
                "Designed a strictly decoupled 3-agent architecture (Herald, Nexus, Dispatch) enforcing complete separation of concerns so agents never call each other directly, eliminating circular deadlocks.\n"
                "Implemented LLM intent classification with confidence-based routing logic to catch ambiguous queries and trigger clarification flows before dispatching execution tasks.\n"
                "Engineered resilient background job scheduling and automated task pipelines with robust fault recovery."
            ),
            architecture_highlights=(
                "3-tier mediator topology; zero direct agent coupling; confidence threshold routing (<0.85 triggers conversational disambiguation); asynchronous message queue via FastAPI."
            ),
            start_date="Jun 2026",
            end_date="Present",
            is_featured=True
        ),
        Project(
            title="EduOS — AI Curiosity-First Education Engine",
            subtitle_role="Creator & Lead Developer",
            repo_link="https://github.com/Soldier224K/eduos-engine",
            demo_link="https://rajrasal.dev/projects/eduos",
            tech_stack="Python, FastAPI, WhatsApp Cloud API, Prompt Chains, Knowledge Graph, SQLite",
            description=(
                "Developed an AI education platform featuring an algorithmic 'pinch engine' that generates one high-value conceptual knowledge connection per day for students based on their curiosity graph.\n"
                "Engineered core logic prioritizing curiosity-driven concept delivery before standard syllabus notes, boosting daily student engagement metrics.\n"
                "Built WhatsApp API integration, deliberately decoupled during development with an isolated rate-limiter and queue to prevent unauthorized broadcasting."
            ),
            architecture_highlights=(
                "Curiosity graph mapping; asynchronous outbound dispatch with token bucket rate limiting; deterministic prompt chain templates with ground-truth validation."
            ),
            start_date="Nov 2025",
            end_date="Feb 2026",
            is_featured=True
        ),
        Project(
            title="SecureVerse — Decentralized Zero-Trust Architecture",
            subtitle_role="Systems Architect",
            repo_link="https://github.com/Soldier224K/secureverse",
            demo_link="https://rajrasal.dev/projects/secureverse",
            tech_stack="Python, Cryptography, Zero-Trust Architecture, Distributed Ledger, REST APIs",
            description=(
                "Architected a decentralized identity and zero-trust verification platform engineered to prevent credential theft and unauthorized access in enterprise networks.\n"
                "Formulated the end-to-end cryptographic trust chain, policy evaluation engine, and auditable logging system.\n"
                "Awarded 3rd Place at the Deal Dome Competition for superior architectural soundness and threat mitigation design."
            ),
            architecture_highlights=(
                "Mutual TLS, cryptographic assertion validation, state machine based authorization engine, zero persistent plain text secrets."
            ),
            start_date="Oct 2025",
            end_date="Dec 2025",
            is_featured=True
        )
    ])

    # 6. Certifications
    db.add_all([
        Certification(
            name="Advanced Backend Engineering & Distributed Systems Architecture",
            issuing_org="Engineering Systems Council",
            issue_date="2025",
            credential_id="ESC-DIST-94821",
            credential_url="https://verify.org/ESC-DIST-94821"
        ),
        Certification(
            name="Responsible Disclosure & Security Research Recognition",
            issuing_org="HackerOne",
            issue_date="2025",
            credential_id="H1-RR-88410",
            credential_url="https://hackerone.com/cyber-monk"
        ),
        Certification(
            name="Multi-Agent Systems & LLM Architecture Foundations",
            issuing_org="DeepLearning / AI Systems Guild",
            issue_date="2026",
            credential_id="MAS-772910",
            credential_url="https://verify.org/MAS-772910"
        )
    ])

    # 7. Achievements & Awards
    db.add_all([
        Achievement(
            title="3rd Place — Deal Dome Competition",
            issuer="Deal Dome National Engineering Challenge",
            date="Dec 2025",
            description="Awarded 3rd place for designing the architectural specification and threat modeling for SecureVerse, a zero-trust enterprise security framework.",
            category="Competition"
        ),
        Achievement(
            title="Security Research: OPPO Find X3 Pro Vulnerability",
            issuer="HackerOne / OPPO Security Response Center",
            date="2025",
            description="Identified and responsibly reported an Open Redirect vulnerability in the OPPO Find X3 Pro flagship device software ecosystem, acknowledged in HackerOne Hall of Fame.",
            category="Security Research"
        ),
        Achievement(
            title="SummerHacks 2026 Backend Lead",
            issuer="SummerHacks Hackathon Committee",
            date="Jul 2026",
            description="Led backend architecture for the 4-member team that designed F.R.I.D.A.Y, completing the 3-agent mediator engine in under 36 hours.",
            category="Hackathon"
        )
    ])

    # 8. Publications & Whitepapers
    db.add_all([
        Publication(
            title="HAMIA Architecture Specification: Hierarchical Adaptive Multi-Model Intelligence Architecture",
            venue_type="Architecture Whitepaper",
            publisher="Autonomous Systems Research (Self-Published Technical Whitepaper)",
            publication_date="Oct 2026",
            url="https://github.com/Soldier224K/architecture-whitepapers/blob/main/HAMIA_Architecture.md",
            abstract=(
                "A cloud-native fusion system that orchestrates a federation of specialized frontier models (12+) through an 8-stage pipeline. "
                "Emphasizes evidence-centric fusion over naive voting, using external ground-truth verifiers (Firecracker sandboxes, SymPy) "
                "and a cyclic adversarial critic to prevent multi-model ensembles from amplifying shared bias."
            )
        ),
        Publication(
            title="TWELVE Product Documentation: AI-Powered Viva & Interview Assessment System",
            venue_type="System Design & Product Specification",
            publisher="Higher Education Assessment Systems",
            publication_date="Oct 2026",
            url="https://github.com/Soldier224K/architecture-whitepapers/blob/main/TWELVE_Product_Doc.md",
            abstract=(
                "A secure, kiosk-based assessment pipeline that replaces human examiner bias with a multi-model AI panel. "
                "Features a specialized split-evaluator architecture (Curriculum, Application, Coherence) and a robust "
                "legal/compliance strategy for deployment in higher education environments."
            )
        )
    ])

    # 9. Languages
    db.add_all([
        Language(language="English", proficiency="Professional Working Proficiency"),
        Language(language="Hindi", proficiency="Native / Bilingual"),
        Language(language="Marathi", proficiency="Native / Bilingual")
    ])

    db.commit()

