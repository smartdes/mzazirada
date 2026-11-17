/**
 * ============================================================================
 * MzaziRada — Google Apps Script for School Management System
 * ============================================================================
 * Syncs student records and fee balances from Google Sheets to the MzaziRada
 * USSD/SMS backend gateway.
 */

// Retrieve configuration from Script Properties (or fall back to defaults)
const props = PropertiesService.getScriptProperties();

const CONFIG = {
  MZAZIRADA_API_URL:
    props.getProperty("MZAZIRADA_API_URL") ||
    "https://your-domain-or-ngrok.app/api/v1/webhook/update-student",
  WEBHOOK_SECRET:
    props.getProperty("WEBHOOK_SECRET") || "your_webhook_secret_here",
  INSTITUTION_NAME:
    props.getProperty("INSTITUTION_NAME") || "MzaziRada Academy",
  USSD_SHORTCODE: props.getProperty("USSD_SHORTCODE") || "*384*73355#",
};

/**
 * Creates custom MzaziRada menu when the spreadsheet is opened.
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("MzaziRada SMS")
    .addItem("📢 Send Fee Reminders to Parents", "sendFeeReminders")
    .addSeparator()
    .addItem("⚡ Test API Connection", "testConnection")
    .addItem("⚙️ Setup Script Properties", "setupScriptProperties")
    .addToUi();
}

/**
 * Helper to configure API URL and Webhook Secret via user prompt.
 */
function setupScriptProperties() {
  const ui = SpreadsheetApp.getUi();
  const urlPrompt = ui.prompt(
    "MzaziRada Setup",
    "Enter the Backend Webhook URL (e.g., https://xyz.ngrok-free.app/api/v1/webhook/update-student):",
    ui.ButtonSet.OK_CANCEL
  );

  if (urlPrompt.getSelectedButton() !== ui.Button.OK) return;
  const url = urlPrompt.getResponseText().trim();

  const secretPrompt = ui.prompt(
    "MzaziRada Setup",
    "Enter the Webhook Secret Token:",
    ui.ButtonSet.OK_CANCEL
  );

  if (secretPrompt.getSelectedButton() !== ui.Button.OK) return;
  const secret = secretPrompt.getResponseText().trim();

  props.setProperty("MZAZIRADA_API_URL", url);
  props.setProperty("WEBHOOK_SECRET", secret);

  ui.alert("Success! Configuration saved to Script Properties.");
}

/**
 * 1. SEND FEE REMINDERS
 * Iterates through FeeLedger and triggers student updates to MzaziRada backend.
 */
function sendFeeReminders() {
  const ui = SpreadsheetApp.getUi();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const feeSheet = ss.getSheetByName("FeeLedger");
  const studentSheet = ss.getSheetByName("Students");

  if (!feeSheet || !studentSheet) {
    ui.alert("Error: 'FeeLedger' or 'Students' tab not found.");
    return;
  }

  const studentsMap = getStudentsMap(studentSheet);
  const feeData = feeSheet.getDataRange().getValues();
  const headers = feeData[0];
  const admIdx = headers.indexOf("adm_no");
  const balIdx = headers.indexOf("balance");
  let queuedCount = 0;

  for (let i = 1; i < feeData.length; i++) {
    const row = feeData[i];
    const adm = String(row[admIdx] || "").trim();
    if (!adm) continue;

    const balance = parseFloat(row[balIdx]) || 0;
    if (balance > 0 && studentsMap[adm]) {
      const student = studentsMap[adm];
      const payload = {
        secret: CONFIG.WEBHOOK_SECRET,
        phone_number: student.phone,
        student_id: adm,
        name: student.name,
        fees_due: `KES ${balance.toLocaleString()}`,
        attendance: student.attendance || "95%",
        latest_grade: student.latest_grade || "Math: A, Sci: B",
        send_sms: true,
        sms_custom_message: `Dear Parent, fee reminder for ${student.name} (${adm}). Outstanding balance: KES ${balance.toLocaleString()}. Dial ${CONFIG.USSD_SHORTCODE} anytime to check status.`,
      };

      postToMzaziRada(payload);
      queuedCount++;
    }
  }
  ui.alert(`Done! Queued fee reminder updates for ${queuedCount} parent(s).`);
}

/**
 * Helper: Makes HTTP POST request to MzaziRada backend webhook.
 */
function postToMzaziRada(payload) {
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  };

  try {
    const response = UrlFetchApp.fetch(CONFIG.MZAZIRADA_API_URL, options);
    return response.getResponseCode();
  } catch (err) {
    Logger.log("Failed to post webhook: " + err.message);
    return null;
  }
}

/**
 * Helper: Builds a map of adm_no -> { name, phone, attendance, latest_grade }
 */
function getStudentsMap(studentSheet) {
  const data = studentSheet.getDataRange().getValues();
  const headers = data[0];
  const admIdx = headers.indexOf("adm_no");
  const nameIdx = headers.indexOf("student_name");
  const phoneIdx = headers.indexOf("parent_phone");
  const attIdx = headers.indexOf("attendance");
  const gradeIdx = headers.indexOf("latest_grade");
  const map = {};

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const adm = String(row[admIdx] || "").trim();
    if (adm) {
      map[adm] = {
        name: String(row[nameIdx] || "").trim(),
        phone: String(row[phoneIdx] || "").trim(),
        attendance: attIdx !== -1 ? String(row[attIdx] || "") : "95%",
        latest_grade: gradeIdx !== -1 ? String(row[gradeIdx] || "") : "N/A",
      };
    }
  }
  return map;
}

/**
 * Test API connection from Google Sheet.
 */
function testConnection() {
  const ui = SpreadsheetApp.getUi();
  const status = postToMzaziRada({
    secret: CONFIG.WEBHOOK_SECRET,
    phone_number: "+254712345678",
    student_id: "ADM-1001",
    name: "Jane Doe",
    fees_due: "KES 15,000",
    attendance: "95%",
    latest_grade: "Mathematics: A",
    send_sms: false,
  });

  if (status === 200) {
    ui.alert("Success! Google Apps Script connected to MzaziRada backend.");
  } else {
    ui.alert(
      `Connection status: ${status || "Failed"}. Check MZAZIRADA_API_URL.`
    );
  }
}
