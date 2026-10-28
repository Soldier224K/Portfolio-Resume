# TWELVE — Complete Product Documentation

**Tagline:** No fear. No favour. Only knowledge.  
**Product:** AI-Powered Viva & Interview Assessment System for Higher Education  
**Status:** POC Pending

---

## 1. The Core Problem
The oral examination (viva) in Indian colleges is broken at three levels:
1. **The Biased Professor:** Assigns marks based on favouritism, attendance, or personal preference. The sincere student is uniquely disadvantaged because there is no transcript or evidence.
2. **The Dishonest Student:** Uses scripted, memorised answers for generic questions to pass without genuine understanding.
3. **The Unstandardized Institution:** Runs oral exams with no consistent rubric, no audit trail, and no data for improvement.

**The Root Cause:** No one built a system to replace human subjectivity in oral examinations with something better. TWELVE is that system.

## 2. The Solution — What TWELVE Does
TWELVE replaces the biased human examiner with a structured, AI-driven kiosk system that:
* **Authenticates** the student.
* **Reads** their submitted project/report *before* asking a single question.
* **Generates** personalized, case-based questions uniquely tied to their work.
* **Drills down** with cross-questioning to test genuine understanding.
* **Evaluates** responses against the college's rubric using a multi-model AI panel.
* **Produces** a final score alongside a complete, auditable transcript.

## 3. Session Flow — Minute by Minute
1. **Kiosk Activation:** OS locked down; TWELVE takes over the screen.
2. **Student Identification:** Roll Number + Name entry (camera monitors eye-contact for anti-cheat, not biometric scoring).
3. **Submission Retrieval:** TWELVE reads the specific problem statement (PS) and student code/report.
4. **Pre-Session Analysis:** The AI builds a layered question tree (Surface -> Drill-down -> Variants).
5. **PS Verification:** Opening question verifies basic comprehension of the problem.
6. **Project Deep Dive:** Dynamic questioning using the student's own words. *(e.g., "You mentioned O(1) lookup. What happens on hash collision?")*
7. **Cross-Questioning:** The core test. The same concept is reframed in novel scenarios to break scripted memorization.
8. **Core Subject Knowledge:** Randomized, calibrated questions from a curriculum bank.
9. **Feedback:** Developmental feedback on strong/weak areas (not graded).
10. **Score Generation:** Panel computes marks; transcript securely logged.

## 4. Technical Architecture
### The AI Panel — Multi-Model Design
A single model creates an echo chamber. TWELVE uses three independent models to evaluate responses:
*   **Model A (Curriculum Accuracy - 40%):** Trained on academic textbooks and syllabi. Detects factual errors.
*   **Model B (Application Depth - 40%):** Trained on industry case studies and technical interviews. Evaluates concept application.
*   **Model C (Coherence & Consistency - 20%):** Trained on debate records and Q&A transcripts. Detects memorized scripts breaking under cross-questioning.
*   **The Aggregator:** Computes a weighted rational average. If disagreement exceeds a threshold, it flags the answer for human review.

### Kiosk Mode
*   Runs on Windows LTSC with Assigned Access + Electron.
*   OS-level lockdown: No task manager, no USB ports, no screen recording.
*   Local network only (no internet access for the student).

## 5. The Appeal Process
**The AI is the examiner. The professor is the appellate authority. The transcript is the evidence.**
If a student disputes their mark, the professor reviews the immutable transcript containing every question, answer, and AI scoring rationale. The professor can override the score only by documenting a clear, articulable error by the AI.

## 6. Competitive Advantage
Competitors (HireVue, Mercer Mettl, Talview, ExamSoft) focus on corporate hiring, written MCQs, or admissions screening. **TWELVE is the only product built specifically for the academic oral viva in Indian higher education.**

## 7. Phased Rollout
1. **POC (Proof of Concept):** Prove the core questioning engine works via a simple file upload interface.
2. **Phase 1 (Pilot):** Run one real batch at the host college using kiosk mode and the multi-model panel.
3. **Phase 2 (First External Sale):** Approach nearby engineering colleges using the pilot transcript data as the pitch.
4. **Phase 3 (Scale):** LMS integrations, biometric verification (post-DPDP Act compliance), and self-service onboarding.
