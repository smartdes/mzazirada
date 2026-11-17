# Sample Datasets for MzaziRada

This directory contains sanitized, synthetic mock datasets to test and showcase MzaziRada without using real student or parent data.

## Files

1. **`students.csv`**
   - Represents the `Students` sheet in Google Sheets.
   - Headers: `adm_no`, `student_name`, `parent_phone`, `attendance`, `latest_grade`
   - Example parent phone numbers use standard E.164 test formats (`+254712345678`, `+254722000001`, etc.).

2. **`fee_ledger.csv`**
   - Represents the `FeeLedger` sheet in Google Sheets.
   - Headers: `adm_no`, `student_name`, `term`, `total_fees`, `amount_paid`, `balance`, `status`
   - Used by `sendFeeReminders()` in Google Apps Script to compute outstanding fees.

3. **`webhook_payload_sample.json`**
   - An example of the JSON payload dispatched by Google Apps Script to `POST /api/v1/webhook/update-student`.

4. **`ussd_callback_sample.json`**
   - An example of the form data transmitted by Africa's Talking gateway when a user dials the USSD shortcode.

## How to Import into Google Sheets

1. Create a new Google Spreadsheet and title it **MzaziRada School Records**.
2. Create two tabs:
   - Name the first tab **`Students`**
   - Name the second tab **`FeeLedger`**
3. Open `students.csv` and copy/paste or import the data into the `Students` tab (starting at row 1).
4. Open `fee_ledger.csv` and copy/paste or import the data into the `FeeLedger` tab (starting at row 1).
5. Open **Extensions > Apps Script**, paste `apps_script/Code.gs`, and refresh the sheet to see the **MzaziRada SMS** custom menu.
