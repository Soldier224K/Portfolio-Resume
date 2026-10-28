# Google Sheets Live Integration Guide

This portfolio management system integrates seamlessly with **Google Sheets** through two powerful mechanisms:

1. **One-Click Native XLSX Download**:
   - Downloads a multi-tab workbook with separate sheets for `Profile`, `Education`, `Skills`, `Experience`, `Projects`, `Certifications`, `Achievements`, `Publications`, and `Languages`.
   - Formatted with freeze rows, styled slate headers, alternating row colors, and auto-fitted columns.
   - Simply drag-and-drop or import into Google Sheets (`File > Import > Upload`).

2. **Live 2-Way Webhook Synchronization (Google Apps Script)**:
   - Synchronizes your database directly to a live Google Sheet in real time without requiring complex Google Cloud OAuth setup.
   - Follow the 60-second setup below.

---

### Troubleshooting: "Error 401: invalid_client"
If Google gives you `Error 401: invalid_client` during authorization:
1. **Cause**: You are logged into **more than one Google Account** in your browser (e.g. personal + university/work). Google Apps Script's OAuth redirects to the wrong account profile (`/u/0` vs `/u/1`), causing Google's identity server to reject the client.
2. **Solution (Takes 30 seconds)**:
   - Open a **New Incognito Window** (`Cmd + Shift + N` on Mac).
   - Log into **ONLY** your intended account (`rajrasal0806@gmail.com`).
   - Open your Google Sheet -> **Extensions > Apps Script**.
   - Deploy as Web App -> Authorize. It will succeed immediately!

---

### Alternative: Instant Zero-Auth Import
If you do not want to use Apps Script at all:
1. Open [sheets.new](https://sheets.new).
2. Click **File > Import > Upload**.
3. Select or drag [`sample_data/exported_portfolio.xlsx`](../sample_data/exported_portfolio.xlsx).
4. Select *Replace spreadsheet* and click **Import data**.
5. All 9 sheets (`Profile`, `Education`, `Skills`, `Experience`, `Projects`, `Certifications`, `Achievements`, `Publications`, `Languages`) will be populated and formatted immediately without requiring any authorization!

1. **Create or Open a Google Sheet**:
   - Open [Google Sheets](https://sheets.new) and create a new blank spreadsheet.
   - Name it `Raj Rasal - Centralized Portfolio Database`.

2. **Open Apps Script**:
   - In the Google Sheet menu, click **Extensions** > **Apps Script**.

3. **Paste the Script**:
   - Delete any default code in `Code.gs`.
   - Copy the entire contents of [`Code.gs`](./Code.gs) and paste it into the editor.
   - Click the **Save** icon (disk).

4. **Deploy as Web App**:
   - Click the blue **Deploy** button at the top right > **New deployment**.
   - Under *Select type*, click the gear icon and select **Web app**.
   - Set **Description**: `Portfolio Sync Bridge`.
   - Set **Execute as**: `Me (your email)`.
   - Set **Who has access**: `Anyone`.
   - Click **Deploy**.
   - If prompted, click **Authorize Access**, select your Google account, click *Advanced*, and click *Go to Untitled project (unsafe)*.
   - Copy the generated **Web App URL** (e.g. `https://script.google.com/macros/s/.../exec`).

5. **Connect to Application**:
   - In the Portfolio Web Application, open the **Google Sheets Sync Hub** tab (or Settings).
   - Paste the Web App URL into the **Google Apps Script Webhook URL** input.
   - Click **"Sync Database to Google Sheets"**.
   - Switch back to your Google Sheet: All 9 sheets (`Profile`, `Education`, `Skills`, `Experience`, `Projects`, etc.) are created and populated with formatted data instantly!

