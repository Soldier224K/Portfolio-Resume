import os
import time
import subprocess
import signal
import cv2
from playwright.sync_api import sync_playwright

def record_demonstration():
    os.makedirs("demo_video", exist_ok=True)
    video_dir = os.path.abspath("demo_video/raw_recordings")
    os.makedirs(video_dir, exist_ok=True)

    print("Step 1: Starting local FastAPI server...")
    proc = subprocess.Popen(
        ["python3", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8015"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2.5)

    try:
        print("Step 2: Launching Playwright browser with HD video recorder (1280x720)...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                record_video_dir=video_dir,
                record_video_size={"width": 1280, "height": 720},
                viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()

            # SCENE 1: Live Portfolio Showcase
            print("Recording Scene 1: Live Portfolio Showcase...")
            page.goto("http://127.0.0.1:8015")
            page.wait_for_selector("#showcaseName")
            time.sleep(2.0)
            page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
            time.sleep(2.0)
            page.evaluate("window.scrollBy({ top: 500, behavior: 'smooth' })")
            time.sleep(2.0)
            page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
            time.sleep(1.5)

            # SCENE 2: Database Manager & SQLite Inspector
            print("Recording Scene 2: Relational Database & SQLite Inspector...")
            page.click("button[data-tab='database']")
            time.sleep(1.5)
            # Open SQLite Inspector
            page.click("#toggleDbInspectorBtn")
            time.sleep(2.5)
            # Cycle through DB sub-tabs
            for sub in ["skills", "projects", "education", "experiences", "publications"]:
                page.click(f"button[data-subtab='{sub}']")
                time.sleep(1.2)

            # SCENE 3: Google Sheets Hub & Interactive Spreadsheet Viewer
            print("Recording Scene 3: Google Sheets Synchronization & Live Spreadsheet Grid...")
            page.click("button[data-tab='sheets']")
            time.sleep(1.8)
            page.evaluate("window.scrollBy({ top: 350, behavior: 'smooth' })")
            time.sleep(1.5)
            # Switch between Google Sheets tabs specifically in #tab-sheets
            for s_name in ["Skills", "Projects", "Experience", "Publications", "Profile"]:
                page.click(f"#tab-sheets button[onclick*='switchSpreadsheetSheet']:has-text('{s_name}')")
                time.sleep(1.2)
            page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
            time.sleep(1.0)

            # SCENE 4: Gemini AI Unstructured Information Parser
            print("Recording Scene 4: Gemini AI Smart Parser...")
            page.click("button[data-tab='ai-parser']")
            time.sleep(1.2)
            sample_unstructured = (
                "Raj Bharat Rasal\n"
                "Email: rajrasal0806@gmail.com | Phone: +91 8766028985\n"
                "Summary: Systems architect specializing in distributed computing, zero-trust protocols, and multi-agent AI pipelines.\n"
                "Skills: Python, C++, Distributed Computing, Tensor Sharding, Zero-Trust, FastAPI\n"
                "Projects: Saturday/Sunday distributed tensor sharding compute network; Friday multi-agent backend."
            )
            page.fill("#unstructuredTextInput", sample_unstructured)
            time.sleep(1.0)
            page.click("#parseTextBtn")
            time.sleep(2.5)

            # SCENE 5: JD Analyzer & ATS Customizer (Job 1: Distributed Systems)
            print("Recording Scene 5: JD Matcher for Distributed Systems Architect...")
            page.click("button[data-tab='jd-analyzer']")
            time.sleep(1.2)
            page.select_option("#sampleJdSelect", "jd-1")
            time.sleep(1.0)
            page.click("#analyzeJdBtn")
            time.sleep(2.5)
            page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
            time.sleep(2.0)

            # SCENE 6: Live ATS Resume Preview & Download
            print("Recording Scene 6: Live ATS Resume Preview & Export...")
            page.click("button[data-tab='resume-preview']")
            time.sleep(2.5)
            page.evaluate("window.scrollBy({ top: 350, behavior: 'smooth' })")
            time.sleep(1.5)
            page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
            time.sleep(1.0)

            # SCENE 7: Dynamic Customization for Job 2 (AI Multi-Agent Systems Engineer)
            print("Recording Scene 7: Dynamically Customizing for AI Multi-Agent Role...")
            page.click("button[data-tab='jd-analyzer']")
            time.sleep(1.0)
            page.select_option("#sampleJdSelect", "jd-2")
            time.sleep(1.0)
            page.click("#analyzeJdBtn")
            time.sleep(2.5)
            page.click("button[data-tab='resume-preview']")
            time.sleep(2.5)

            print("Closing browser session and finalizing video...")
            context.close()
            browser.close()

        # Step 3: Find the recorded webm file and convert/save as standard demonstration video
        raw_files = [f for f in os.listdir(video_dir) if f.endswith(".webm")]
        if not raw_files:
            print("Error: No raw webm video found in", video_dir)
            return

        latest_raw = os.path.join(video_dir, raw_files[-1])
        output_webm = "demo_video/portfolio_system_demonstration.webm"
        output_mp4 = "demo_video/portfolio_system_demonstration.mp4"

        # Copy webm to target
        import shutil
        shutil.copyfile(latest_raw, output_webm)
        print(f"Saved demonstration video (WebM format): {output_webm}")

        # Convert to MP4 using OpenCV
        print("Converting video to MP4 format with OpenCV...")
        cap = cv2.VideoCapture(output_webm)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1280
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_mp4, fourcc, fps, (width, height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()
        print(f"Saved demonstration video (MP4 format): {output_mp4} ({frame_count} frames)")

    finally:
        proc.send_signal(signal.SIGINT)
        proc.wait()

if __name__ == "__main__":
    record_demonstration()
