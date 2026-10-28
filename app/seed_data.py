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
            "Second-year B.Tech CSE student focused on backend systems architecture, distributed computing, "
            "and multi-agent AI pipelines. Founder of SecureVerse with a mission to build secure, human-aligned AI systems. "
            "Passionate about AI Safety, Digital Forensics, Decentralized Infrastructure, and Verifiable Zero-Trust Computation."
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
        ("Rust", "Languages", "Intermediate", True),
        ("Java", "Languages", "Advanced", True),
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
        ("Soroban Smart Contracts (Stellar)", "Distributed Systems & Architecture", "Advanced", True),

        # AI & Machine Learning
        ("Multi-Agent AI Pipelines", "AI & Machine Learning", "Expert", True),
        ("AI Safety & Alignment", "AI & Machine Learning", "Advanced", True),
        ("LLM Intent Classification & Routing", "AI & Machine Learning", "Expert", True),
        ("Prompt Engineering & Chains", "AI & Machine Learning", "Advanced", True),
        ("Progressive RAG & Memory Layers", "AI & Machine Learning", "Advanced", True),
        ("Adversarial Critic Systems", "AI & Machine Learning", "Advanced", True),
        ("Ethical AI Systems", "AI & Machine Learning", "Advanced", False),
        ("Predictive Computational Modeling", "AI & Machine Learning", "Intermediate", False),

        # Backend & Cloud Infrastructure
        ("FastAPI", "Backend & Cloud", "Expert", True),
        ("RESTful API Design", "Backend & Cloud", "Expert", True),
        ("Asynchronous Programming (asyncio)", "Backend & Cloud", "Expert", True),
        ("AWS Lambda & Serverless Pipelines", "Backend & Cloud", "Advanced", True),
        ("MongoDB & Aggregation Framework", "Backend & Cloud", "Advanced", True),
        ("APScheduler & Task Queues", "Backend & Cloud", "Advanced", False),
        ("Tailscale VPN & Mesh Networking", "Backend & Cloud", "Advanced", False),
        ("Redis Streams & Message Passing", "Backend & Cloud", "Advanced", False),

        # Security & Systems Research
        ("Vulnerability Research & Bug Bounty", "Security & Systems", "Advanced", True),
        ("Digital Forensics & Reverse Engineering", "Security & Systems", "Advanced", True),
        ("Zero-Trust Data Flow Verification", "Security & Systems", "Advanced", True),
        ("Futuristic Systems Design", "Distributed Systems & Architecture", "Advanced", True),
        ("Non-STL Algorithm Engineering", "Security & Systems", "Advanced", True),
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
    db.add_all([
        Experience(
            company="SecureVerse",
            role="Founder & Lead Architect",
            location="Navi Mumbai, India",
            start_date="Oct 2025",
            end_date="Present",
            is_current=True,
            description=(
                "Founded SecureVerse to engineer decentralized zero-trust identity verification architectures, AI safety tooling, and privacy-preserving computing systems.\n"
                "Formulated end-to-end cryptographic trust chains, automated audit mechanisms, and threat mitigation models recognized in national engineering challenges.\n"
                "Directed technology roadmap, leading proof-of-concept development and cross-functional prototype verification."
            ),
            technologies="Zero-Trust Architecture, Cryptography, AI Safety, System Design, Python, Distributed Ledger"
        ),
        Experience(
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
        )
    ])

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
            title="BioShield AI — Computational Biosafety & Health Resilience Engine",
            subtitle_role="Lead Researcher & Architect",
            repo_link="https://github.com/Soldier224K/bioshield-ai",
            demo_link="https://rajrasal.dev/projects/bioshield",
            tech_stack="Python, PyTorch, Predictive Modeling, Simulation Engines, FastAPI, Docker",
            description=(
                "Engineered predictive computational modeling pipelines for simulating pathogen transmission dynamics and evaluating countermeasure strategies in real time.\n"
                "Designed distributed simulation workers to process high-throughput biological interaction datasets with deterministic validation hooks.\n"
                "Authored biosafety compliance blueprints and zero-leakage data sandboxing mechanisms for sensitive health research data."
            ),
            architecture_highlights=(
                "Event-driven asynchronous worker pool; deterministic simulation checkpointing; isolated compute sandboxes with strict egress filtering."
            ),
            start_date="Jan 2026",
            end_date="Present",
            is_featured=True
        ),
        Project(
            title="SecureVerse — Decentralized Zero-Trust Architecture",
            subtitle_role="Founder & Systems Architect",
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
        ),
        Project(
            title="Cognitive Diplomat — Multi-Agent Negotiation Predictor & RAG",
            subtitle_role="Lead AI Systems Architect",
            repo_link="https://github.com/Soldier224K/TypeScript-prediction-API-with-parallel-agents-and-RAG",
            demo_link="https://loom.com/share/b5c92f183d2a456191b24e931168923a",
            tech_stack="TypeScript, Express, Ollama LLM, Progressive RAG, In-Memory LRU Cache, Vector-Keyword Hybrid Retrieval",
            description=(
                "Engineered a high-performance negotiation next-turn prediction engine orchestrating a 3-persona parallel agent fan-out via Promise.all.\n"
                "Implemented a progressive RAG layer over tactical negotiation playbooks with keyword-hybrid retrieval and LRU-bounded memory.\n"
                "Enforced deterministic synthesis using temperature=0 and fixed seed assertions with strict confidence score clamping."
            ),
            architecture_highlights=(
                "Parallel agent fan-out; deterministic LLM synthesis; 500-entry LRU per-request memory cache; full requirement traceability matrix."
            ),
            start_date="Sep 2026",
            end_date="Oct 2026",
            is_featured=True
        ),
        Project(
            title="Topcoder AI Profile Video Pipeline — Async Cloud-Native Engine",
            subtitle_role="Cloud & AI Pipeline Architect",
            repo_link="https://github.com/Soldier224K/Topcoder-Profile-Intro-Video-Generator-AI-Pipeline-Async-Scalable-",
            demo_link="https://topcoder-video-pipeline.onrender.com",
            tech_stack="Python, AWS Lambda, MoviePy/FFmpeg, Streamlit, Asynchronous Orchestration, Docker, Render",
            description=(
                "Architected an event-driven serverless video processing pipeline that automatically converts raw member intro footage into professional branded Topcoder videos.\n"
                "Built an AWS Lambda queue consumer for scalable background transcription, caption overlay, and audio normalization.\n"
                "Delivered an interactive Streamlit operational dashboard for cost, performance, and compute budget analysis."
            ),
            architecture_highlights=(
                "Decoupled queue-driven serverless architecture; dynamic FFmpeg rendering pipeline; budget and resource observability dashboard."
            ),
            start_date="Aug 2026",
            end_date="Sep 2026",
            is_featured=True
        ),
        Project(
            title="DealVault & Pactum — Stellar Soroban Smart Contract Escrow",
            subtitle_role="Smart Contract & Backend Engineer",
            repo_link="https://github.com/Soldier224K/dealvault-platform-escrow",
            demo_link="https://github.com/Soldier224K/Pactum",
            tech_stack="Rust, Soroban Smart Contracts, Stellar Testnet, TypeScript, Express, Web3",
            description=(
                "Co-developed an enterprise-grade escrow infrastructure and recurring commitment registry on the Stellar blockchain.\n"
                "Authored Soroban smart contracts enforcing programmatic fund locking, milestone verification, and automated payouts.\n"
                "Constructed a tamper-proof on-chain compliance history tracking fulfillment status for service-level commitments."
            ),
            architecture_highlights=(
                "Non-custodial smart contract vaults; state-machine commitment tracker; cryptographic transaction signing via Stellar SDK."
            ),
            start_date="Jul 2026",
            end_date="Aug 2026",
            is_featured=True
        ),
        Project(
            title="DSA SpaceOPs — Satellite Mission Operations & Navigation Engine",
            subtitle_role="Systems & Algorithm Engineer",
            repo_link="https://github.com/Soldier224K/DSA-SpaceOPs",
            demo_link="https://github.com/Soldier224K/DSA-SpaceOPs",
            tech_stack="C++, Non-STL Custom Data Structures, AVL Trees, Priority Queues, Graph Algorithms, Dijkstra",
            description=(
                "Engineered a mission control and cislunar spacecraft communications router implementing 7 custom data structures completely from scratch without STL containers.\n"
                "Implemented an AVL self-balancing mission registry, Dijkstra minimum-latency routing for cislunar mesh networks, and priority queue activity arbiters.\n"
                "Designed an abort-sequence navigational rollback stack with zero memory leaks and deterministic sub-millisecond execution."
            ),
            architecture_highlights=(
                "Zero-STL core architecture; custom self-balancing AVL trees; Dijkstra shortest-path network topology; O(1) abort stack rollback."
            ),
            start_date="May 2026",
            end_date="Jun 2026",
            is_featured=False
        ),
        Project(
            title="Exam Question Paper Generator — ITM Skills University",
            subtitle_role="Desktop Software Architect",
            repo_link="https://github.com/Soldier224K/ExamQuestionPaperGenerator_JAVA",
            demo_link="https://github.com/Soldier224K/ExamQuestionPaperGenerator_JAVA/blob/main/ExamQuestionPaperGeneratorDocumentation.pdf",
            tech_stack="Java, Swing MVC, Custom Graphics2D, File I/O Streams, Deterministic Paper Synthesis",
            description=(
                "Engineered a database-less desktop Java application for faculty at ITM Skills University and School of Future Tech.\n"
                "Built an algorithmic question selector that generates balanced examination papers adhering to difficulty, topic weights, and mark constraints.\n"
                "Authored complete institutional software documentation and mathematical generation proofs."
            ),
            architecture_highlights=(
                "Zero-database portability using native file streams; pure MVC architecture; custom Graphics2D print formatting."
            ),
            start_date="Apr 2026",
            end_date="May 2026",
            is_featured=False
        ),
        Project(
            title="WorkHub — Coworking Space Management Platform",
            subtitle_role="Backend & Database Architect",
            repo_link="https://github.com/Soldier224K/WorkHub",
            demo_link="https://github.com/Soldier224K/WorkHub",
            tech_stack="Node.js, Express, MongoDB, Aggregation Pipeline, JWT RBAC, QR Code Verification",
            description=(
                "Engineered a coworking space reservation backend featuring zero-double-booking atomic concurrency.\n"
                "Implemented real-time availability scrubbing and MongoDB aggregation pipelines for space utilization analytics.\n"
                "Built dynamic floorplan coordinate mapping and QR-based automated desk unlock verification."
            ),
            architecture_highlights=(
                "Atomic reservation locking; 2D floorplan coordinate management; multi-role JWT RBAC security."
            ),
            start_date="Mar 2026",
            end_date="Apr 2026",
            is_featured=False
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

