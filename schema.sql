-- ====================================================================
-- AI-Powered Portfolio Management System Database Schema
-- Target: SQLite / PostgreSQL compatible schema
-- ====================================================================

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    location VARCHAR(100),
    linkedin VARCHAR(200),
    github VARCHAR(200),
    portfolio_url VARCHAR(200),
    summary TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS educations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution VARCHAR(150) NOT NULL,
    degree VARCHAR(100) NOT NULL,
    field_of_study VARCHAR(100) NOT NULL,
    start_year VARCHAR(20) NOT NULL,
    end_year VARCHAR(20) NOT NULL,
    score VARCHAR(50),
    highlights TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    proficiency VARCHAR(50) DEFAULT 'Advanced',
    is_highlighted BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company VARCHAR(150) NOT NULL,
    role VARCHAR(150) NOT NULL,
    location VARCHAR(100),
    start_date VARCHAR(50) NOT NULL,
    end_date VARCHAR(50) NOT NULL,
    is_current BOOLEAN DEFAULT 0,
    description TEXT NOT NULL,
    technologies VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    subtitle_role VARCHAR(150) NOT NULL,
    repo_link VARCHAR(200),
    demo_link VARCHAR(200),
    tech_stack VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    architecture_highlights TEXT,
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    is_featured BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    issuing_org VARCHAR(150) NOT NULL,
    issue_date VARCHAR(50) NOT NULL,
    credential_id VARCHAR(100),
    credential_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    issuer VARCHAR(150) NOT NULL,
    date VARCHAR(50),
    description TEXT NOT NULL,
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    venue_type VARCHAR(100) NOT NULL,
    publisher VARCHAR(150) NOT NULL,
    publication_date VARCHAR(50),
    url VARCHAR(255),
    abstract TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language VARCHAR(100) NOT NULL,
    proficiency VARCHAR(100) NOT NULL
);

