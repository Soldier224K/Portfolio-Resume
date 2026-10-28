import time
import subprocess
import os
import signal
from playwright.sync_api import sync_playwright

def run():
    os.makedirs("screenshots", exist_ok=True)
    
    # Start FastAPI server in background
    proc = subprocess.Popen(
        ["python3", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8008"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2.5) # Wait for server boot

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})

            # 1. Live Portfolio Showcase
            print("Capturing 01_live_portfolio_showcase.png...")
            page.goto("http://127.0.0.1:8008")
            page.wait_for_selector("#showcaseName")
            time.sleep(1.0)
            page.screenshot(path="screenshots/01_live_portfolio_showcase.png")

            # 2. Database Manager Tab
            print("Capturing 02_database_manager.png...")
            page.click("button[data-tab='database']")
            time.sleep(0.8)
            page.screenshot(path="screenshots/02_database_manager.png")

            # 3. AI Smart Parser Tab
            print("Capturing 03_ai_unstructured_parser.png...")
            page.click("button[data-tab='ai-parser']")
            page.fill("#unstructuredTextInput", "Raj Bharat Rasal\nEmail: rajrasal0806@gmail.com\nSkills: Python, C++, Distributed Systems, Tensor Sharding, Zero-Trust Protocols\nProjects: Saturday/Sunday Distributed Compute Network, Friday Multi-Agent Communication Backend")
            page.click("#parseTextBtn")
            time.sleep(1.2)
            page.screenshot(path="screenshots/03_ai_unstructured_parser.png")

            # 4. Google Sheets Sync Hub Tab
            print("Capturing 04_google_sheets_sync_hub.png...")
            page.click("button[data-tab='sheets']")
            time.sleep(0.8)
            page.screenshot(path="screenshots/04_google_sheets_sync_hub.png")

            # 5. JD Analyzer & Tailor Tab
            print("Capturing 05_jd_analysis_matcher.png...")
            page.click("button[data-tab='jd-analyzer']")
            time.sleep(0.5)
            # Select sample JD 1
            page.select_option("#sampleJdSelect", "jd-1")
            page.click("#analyzeJdBtn")
            time.sleep(1.2)
            page.screenshot(path="screenshots/05_jd_analysis_matcher.png")

            # 6. Live Resume Preview & Export Tab
            print("Capturing 06_resume_preview_and_download.png...")
            page.click("button[data-tab='resume-preview']")
            time.sleep(1.0)
            page.screenshot(path="screenshots/06_resume_preview_and_download.png")

            browser.close()
            print("All 6 screenshots captured successfully!")

    finally:
        proc.send_signal(signal.SIGINT)
        proc.wait()

if __name__ == "__main__":
    run()

