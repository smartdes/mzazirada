# Google Apps Script Setup Guide for MzaziRada

This folder contains the automation script that turns a standard Google Spreadsheet into an administrative CMS for school fee tracking and student records.

---

## Architecture Flow

```
[Google Sheets] 
   └── [Apps Script: Code.gs]
           └── HTTP POST (JSON Payload + Webhook Secret)
                   └── [FastAPI Gateway: /api/v1/webhook/update-student]
                           ├── Updates in-memory USSD cache (<10ms lookup)
                           └── Dispatches SMS via Africa's Talking API
```

---

## Setup Steps

### 1. Prepare Google Sheet
1. Create a new Google Spreadsheet titled **MzaziRada School Records**.
2. Add two sheets named:
   - **`Students`**
   - **`FeeLedger`**
3. Import the header rows and sample data from `sample_data/students.csv` and `sample_data/fee_ledger.csv`.

### 2. Install the Script
1. In your Google Sheet, navigate to **Extensions > Apps Script**.
2. Replace any existing contents of `Code.gs` with the code in `apps_script/Code.gs`.
3. Save the project with `Ctrl + S`.
4. Return to your Google Sheet and reload the browser page.
5. A new menu named **`MzaziRada SMS`** will appear in the top toolbar.

### 3. Configure Secrets via Script Properties
Never hardcode secrets directly into shared spreadsheets! Use the built-in configuration helper:
1. Click **MzaziRada SMS > ⚙️ Setup Script Properties** in the sheet menu.
2. Enter your backend webhook URL (e.g., `https://your-domain.com/api/v1/webhook/update-student` or your Ngrok forwarding URL).
3. Enter your secret token matching `WEBHOOK_SECRET` in your backend `.env`.

Alternatively, set them under **Project Settings (gear icon) > Script Properties**:
- `MZAZIRADA_API_URL`
- `WEBHOOK_SECRET`
- `INSTITUTION_NAME`
- `USSD_SHORTCODE`

### 4. Testing the Connection
Click **MzaziRada SMS > ⚡ Test API Connection**. You should see a success confirmation indicating that your Google Apps Script communicates with the FastAPI backend.

### 5. Sending Fee Reminders
Click **MzaziRada SMS > 📢 Send Fee Reminders to Parents**. The script scans rows with a positive balance in `FeeLedger`, matches the parent's phone number from `Students`, updates the USSD cache, and triggers an SMS alert via Africa's Talking.
