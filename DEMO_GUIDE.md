# Application Demonstration Video & Walkthrough Guide

This document provides a concise, structured script and step-by-step walkthrough for recording the application demonstration video for the **AI-Powered Portfolio Management & Dynamic Resume Generator**.

---

## Video Outline & Timecodes (Total Duration: ~3-5 Minutes)

| Timecode | Segment | Core Action Shown |
|---|---|---|
| **0:00 - 0:45** | **1. Architecture & Portfolio Showcase** | Walk through the Daksh Gajjar / Marcus Lorenzet-inspired dark interface. Show Raj Bharat Rasal's verified background, system whitepapers (HAMIA & TWELVE), and project cards (SATURDAY/SUNDAY, F.R.I.D.A.Y, EduOS). |
| **0:45 - 1:30** | **2. Structured Database & CRUD** | Open the Database Manager tab. Navigate the 9 categories (`Profile`, `Education`, `Skills`, `Experience`, `Projects`, `Certifications`, `Achievements`, `Publications`, `Languages`). Add/edit a live entry to demonstrate relational integrity. |
| **1:30 - 2:15** | **3. Gemini AI Smart Parser** | Switch to the AI Parser tab. Paste unstructured text or raw resume notes. Click "Extract Structured Fields with Gemini". Show how the AI structures raw text into typed JSON schema and imports it into the DB. |
| **2:15 - 2:50** | **4. Google Sheets Synchronization** | Open the Google Sheets Hub. Click "Download Multi-Tab XLSX" to show the multi-sheet workbook. Demonstrate the Google Apps Script Webhook integration that pushes real-time database updates to a live Google Sheet. |
| **2:50 - 4:15** | **5. Dynamic JD Matcher & Customizer** | Select Sample JD 1 (*Backend & Distributed Systems Architect*). Click "Analyze with Gemini AI". Point out the Match Score (88%), Matched vs Missing Skills, Domain Keywords, and Strategic Recommendations. Show how selecting different JDs (e.g. *AI Multi-Agent Systems Engineer*) dynamically alters the match matrix and tailored summary without inventing facts. |
| **4:15 - 5:00** | **6. Live ATS Preview, PDF & DOCX Download** | Preview the rendered ATS document. Show how toggling project and skill checkboxes instantly updates the resume. Click **Download PDF** and **Download Word (.docx)**. Open the generated files to demonstrate ATS compliance. |

---

## Detailed Step-by-Step Narration Script

### Scene 1: Introduction & Live Portfolio (0:00 - 0:45)
> *"Welcome! Today I am presenting an AI-Powered Portfolio Management and Dynamic Resume Generation System built for Backend Systems Architect and Distributed AI Engineer Raj Bharat Rasal.*
> 
> *Our frontend aesthetic is inspired by award-winning portfolios like Daksh Gajjar and Marcus Lorenzet. On the home showcase, you see Raj's verified profile, contact details, competitive metrics, and systems projects like the SATURDAY/SUNDAY distributed tensor-sharding network and F.R.I.D.A.Y multi-agent backend.*
> 
> *Notice that we also feature his architectural whitepapers—HAMIA and TWELVE—grounded in zero-trust data flow and verifiable compute."*

### Scene 2: Structured Relational Database (0:45 - 1:30)
> *"Next, let's explore the Database Manager. All professional information is stored in a clean SQLite database with strict relationships. We can manage 9 separate categories:*
> - *Profile, Education, and Categorized Skills*
> - *Production Systems, Work Experience, and Accreditations*
> - *Publications, Security Research, and Languages*
> 
> *Every entry has full CRUD support. When we create or modify an entry, the changes persist immediately and cascade to both Google Sheets and the resume engine."*

### Scene 3: Gemini API Parsing & Ground-Truth Verification (1:30 - 2:15)
> *"In the AI Text Parser module, users can paste unstructured notes, bio paragraphs, or raw resumes. The system integrates the Gemini API to extract entities and map them to our schema.*
> 
> *Crucially, our system enforces a strict ground-truth verification rule: the AI is strictly bounded to the candidate's authentic data and will never invent degrees, companies, or fictitious metrics."*

### Scene 4: Google Sheets Integration (2:15 - 2:50)
> *"For data accessibility, our Google Sheets Hub provides two mechanisms:*
> 1. *A 1-click multi-tab XLSX download formatted with freeze panes, slate header styling, and separate sheets for all 9 categories.*
> 2. *A live 2-way Webhook via our included Google Apps Script (`Code.gs`). With one click, your database is pushed directly into your Google Sheet in the cloud."*

### Scene 5: Dynamic Job Description Matcher (2:50 - 4:15)
> *"Now let's demonstrate the core value proposition: dynamic resume customization based on a Job Description.*
> 
> *Let's select our first sample role: **Backend & Distributed Systems Architect**.*
> *When we click 'Analyze with Gemini AI', the model evaluates the JD against Raj's portfolio. It calculates an 88% match score, extracts domain keywords like Tensor Sharding and Zero-Trust, identifies matching skills in green and missing keywords in pink, and writes an ATS-optimized professional summary.*
> 
> *Now watch what happens when we switch to our second role: **AI Systems & Multi-Agent Infrastructure Engineer**.*
> *The system re-analyzes the JD, highlights F.R.I.D.A.Y and EduOS, re-prioritizes multi-agent orchestration skills, and generates a completely different tailored summary—all from the exact same underlying portfolio database!"*

### Scene 6: Live ATS Preview and Export (4:15 - 5:00)
> *"Finally, we navigate to the Live Resume Preview. Users can toggle checkboxes to select or deselect specific projects, skills, and experiences, watching the preview update live.*
> 
> *The resume layout follows strict corporate ATS standards: clean hierarchy, bold headings, no table nesting bugs, and right-aligned dates.*
> 
> *With a single click, we can export the resume as a high-resolution PDF or an editable ATS Word document (.docx).*
> 
> *Both customized resumes—one for Distributed Systems and one for Multi-Agent AI—are pre-generated and available in the repo for review. Thank you!"*

---

## Video Recording Tips & Tools
- Recommended screen recorder: **QuickTime Player** (`Cmd + Shift + 5` on Mac) or **OBS Studio**.
- Mic: Clear audio with no background noise.
- Browser: Fullscreen view at 1280x800 or 1920x1080.

