import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.environ.get("PORTFOLIO_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "portfolio.db"))
DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    linkedin = Column(String(200), nullable=True)
    github = Column(String(200), nullable=True)
    portfolio_url = Column(String(200), nullable=True)
    summary = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "linkedin": self.linkedin,
            "github": self.github,
            "portfolio_url": self.portfolio_url,
            "summary": self.summary,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(150), nullable=False)
    degree = Column(String(100), nullable=False)
    field_of_study = Column(String(100), nullable=False)
    start_year = Column(String(20), nullable=False)
    end_year = Column(String(20), nullable=False)
    score = Column(String(50), nullable=True)
    highlights = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "institution": self.institution,
            "degree": self.degree,
            "field_of_study": self.field_of_study,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "score": self.score,
            "highlights": self.highlights,
        }

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)  # Languages, Architecture & Distributed Systems, AI/ML, Backend & Cloud, Security, Soft Skills
    proficiency = Column(String(50), nullable=False, default="Advanced")  # Expert, Advanced, Intermediate
    is_highlighted = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "proficiency": self.proficiency,
            "is_highlighted": self.is_highlighted,
        }

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(150), nullable=False)
    role = Column(String(150), nullable=False)
    location = Column(String(100), nullable=True)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=False)  # Line-separated bullet points
    technologies = Column(String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_current": self.is_current,
            "description": self.description,
            "technologies": self.technologies,
        }

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    subtitle_role = Column(String(150), nullable=False)
    repo_link = Column(String(200), nullable=True)
    demo_link = Column(String(200), nullable=True)
    tech_stack = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    architecture_highlights = Column(Text, nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    is_featured = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle_role": self.subtitle_role,
            "repo_link": self.repo_link,
            "demo_link": self.demo_link,
            "tech_stack": self.tech_stack,
            "description": self.description,
            "architecture_highlights": self.architecture_highlights,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_featured": self.is_featured,
        }

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    issuing_org = Column(String(150), nullable=False)
    issue_date = Column(String(50), nullable=False)
    credential_id = Column(String(100), nullable=True)
    credential_url = Column(String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "issuing_org": self.issuing_org,
            "issue_date": self.issue_date,
            "credential_id": self.credential_id,
            "credential_url": self.credential_url,
        }

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    issuer = Column(String(150), nullable=False)
    date = Column(String(50), nullable=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)  # Competition, Security Research, Academic

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "issuer": self.issuer,
            "date": self.date,
            "description": self.description,
            "category": self.category,
        }

class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    venue_type = Column(String(100), nullable=False)  # Whitepaper, Specification, Research
    publisher = Column(String(150), nullable=False)
    publication_date = Column(String(50), nullable=True)
    url = Column(String(255), nullable=True)
    abstract = Column(Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "venue_type": self.venue_type,
            "publisher": self.publisher,
            "publication_date": self.publication_date,
            "url": self.url,
            "abstract": self.abstract,
        }

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(100), nullable=False)
    proficiency = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "language": self.language,
            "proficiency": self.proficiency,
        }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

