# MzaziRada 📱🏫

> **High-Speed USSD & SMS Gateway for School Data Management**  
> Empowering schools to bridge the digital divide by connecting Google Sheets to basic mobile phones (2G/feature phones) via sub-10ms USSD sessions and automated SMS notifications.

---

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Africa's Talking](https://img.shields.io/badge/Telecom-Africa's%20Talking-orange.svg)](https://africastalking.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-12%20passed-brightgreen.svg)](tests/)

---

## 🎯 Purpose & The Problem

In emerging markets across Sub-Saharan Africa:
1. **The Smartphone & Data Barrier**: Millions of parents do not own smartphones, lack reliable home Wi-Fi, or cannot afford mobile data bundles to access web portals. However, nearly 100% have access to basic GSM/2G feature phones (*kabambe*).
2. **Administrative Complexity**: Most primary and secondary schools manage records using spreadsheets (like Google Sheets) rather than complex, expensive enterprise ERP systems.
3. **Communication Latency**: Parents often travel long distances or wait until end-of-term report cards to learn about fee balances, exam results, or truancy.

**MzaziRada** (*"Mzazi"* = Parent, *"Rada"* = Informed / On the alert) solves this by:
- Turning a standard **Google Spreadsheet** into an automated school CMS via Google Apps Script.
- Syncing student fee balances, attendance, and exam marks to a high-performance **FastAPI** backend in real time.
- Providing an instant, zero-data-cost **USSD menu (`*384*XXXX#`)** with sub-10ms response times so parents can check records on any phone.
- Dispatched automated **SMS reminders** whenever fee ledgers are updated.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    A["📊 Google Sheets\n(Students & FeeLedger)"] -->|Custom Menu / Trigger| B["📜 Google Apps Script\n(Code.gs)"]
    B -->|Webhook POST + Secret| C["⚡ FastAPI Gateway\n(MzaziRada Backend)"]
    C -->|Sub-10ms Read/Write| D[("🧠 Fast In-Memory Cache\nPhone ➔ Student Record")]
    C -->|Trigger SMS Alert| E["📲 Africa's Talking SMS"]
    F["📞 Parent Phone\n(*384*73355#)"] <-->|Dial USSD Session| G["📡 Africa's Talking USSD"]
    G <-->|Form POST / Plaintext CON-END| C
```

Detailed architecture diagrams and state machine specifications are documented in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## ✨ Key Features

- **Sub-10ms USSD Engine**: Uses an in-memory state machine to serve telecom gateway requests well within the strict carrier timeouts.
- **Zero-Internet Accessibility**: Works on any GSM phone—no smartphone, mobile app, or data bundle required for parents.
- **Familiar School Interface**: School administrators continue using standard Google Sheets; no new software training required.
- **Secure Webhook Verification**: Shared secret tokens protect endpoints against unauthorized updates.
- **Automated SMS Alerts**: Dispatches personalized fee reminders directly to parent phone numbers.
- **Clean Architecture & Full Test Coverage**: Fully decoupled API routes, Pydantic schemas, and Pytest coverage for all user journeys.

---

## 📁 Repository Structure

```
mzazirada/
├── .env.example                 # Environment configuration template
├── .gitignore                   # Comprehensive git exclusions (secrets, venv, cache)
├── LICENSE                      # MIT Open Source License
├── README.md                    # Main documentation
├── ARCHITECTURE.md              # Deep dive into system design & state machine
├── CONTRIBUTING.md              # Guidelines for open source contributors
├── pytest.ini                   # Pytest path and runner configuration
├── requirements.txt             # Production Python dependencies
├── requirements-dev.txt         # Development & testing dependencies
│
├── apps_script/
│   ├── Code.gs                  # Google Apps Script for Google Sheets integration
│   ├── appsscript.json          # Apps Script manifest
│   └── README.md                # Google Sheets & Apps Script setup guide
│
├── backend/
│   ├── .env.example             # Backend local environment template
│   ├── requirements.txt         # Backend dependency list
│   └── app/
│       ├── main.py              # FastAPI app instance and router registration
│       ├── config.py            # Pydantic v2 application settings
│       ├── api/
│       │   ├── ussd.py          # Africa's Talking USSD callback handler (Form POST)
│       │   └── webhook.py       # Google Apps Script student update webhook
│       ├── core/
│       │   ├── cache.py         # Fast in-memory student record store
│       │   └── state_machine.py # USSD CON/END state machine processor
│       ├── schemas/
│       │   └── payloads.py      # Pydantic models for incoming webhooks
│       └── services/
│           └── africastalking_service.py # Africa's Talking SMS dispatcher
│
├── sample_data/
│   ├── students.csv             # Mock student demographics, phone numbers & grades
│   ├── fee_ledger.csv           # Mock student fee payments & balances
│   ├── webhook_payload_sample.json # Sample payload from Google Apps Script
│   ├── ussd_callback_sample.json   # Sample payload from Africa's Talking USSD
│   └── README.md                # Guide to importing mock data
│
└── tests/
    ├── __init__.py
    ├── test_state_machine.py    # Unit tests for USSD menu navigation
    └── test_api_endpoints.py    # Integration tests for USSD and Webhook endpoints
```

---

## 🔒 Security & Privacy Practices

This repository is pre-configured with strict security best practices:
- **Zero Credentials in Code**: No API keys, carrier credentials, or webhook secrets are committed. All secrets are loaded through environment variables.
- **Git Protection**: `.gitignore` prevents inadvertent commits of `.env`, cache files, and private logs.
- **Sanitized Mock Data**: All phone numbers (`+254712345678`), names, and student records in `sample_data/` are strictly fictional.
- **Webhook Authentication**: Incoming updates from Google Apps Script require matching the `WEBHOOK_SECRET` header token.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** installed
- An **[Africa's Talking](https://africastalking.com/)** account (Free Sandbox mode is sufficient)
- A **Google account** (for Google Sheets testing)

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/your-username/mzazirada.git
cd mzazirada

# Create and activate a virtual environment
python -m venv venv

# On Linux/macOS:
source venv/bin/activate
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements-dev.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your Africa's Talking sandbox or live credentials:
```ini
AT_USERNAME=sandbox
AT_API_KEY=your_africastalking_api_key_here
AT_SHORTCODE=*384*73355#
WEBHOOK_SECRET=your_secure_random_webhook_secret_here
```

### 4. Run the Backend Server

Start the development server with Uvicorn:
```bash
uvicorn app.main:app --reload --app-dir backend
```

The API will be accessible at:
- **API Root**: `http://localhost:8000/`
- **Interactive OpenAPI Docs**: `http://localhost:8000/docs`

---

## 🧪 Running Tests

Run the automated test suite using `pytest`:

```bash
pytest -v
```

All 12 unit and integration tests will execute against mocked cache and carrier services:
```
tests/test_api_endpoints.py::test_health_check PASSED
tests/test_api_endpoints.py::test_ussd_endpoint_initial_dial PASSED
tests/test_api_endpoints.py::test_ussd_endpoint_menu_selection PASSED
tests/test_api_endpoints.py::test_webhook_update_success PASSED
tests/test_api_endpoints.py::test_webhook_unauthorized_secret PASSED
tests/test_api_endpoints.py::test_webhook_missing_required_fields PASSED
tests/test_state_machine.py::test_ussd_initial_dial_shows_main_menu PASSED
tests/test_state_machine.py::test_ussd_select_fee_balance PASSED
tests/test_state_machine.py::test_ussd_select_attendance PASSED
tests/test_state_machine.py::test_ussd_select_recent_grades PASSED
tests/test_state_machine.py::test_ussd_invalid_option PASSED
tests/test_state_machine.py::test_ussd_unregistered_phone_number PASSED

======================= 12 passed in 1.25s =======================
```

---

## 🌐 Connecting to Africa's Talking Simulator

To test the USSD flow interactively without telecom fees:

1. **Expose Localhost via Tunnel**:
   ```bash
   ngrok http 8000
   ```
   Copy your forwarding HTTPS URL (e.g., `https://xyz.ngrok-free.app`).

2. **Configure Africa's Talking Sandbox**:
   - Log into the [Africa's Talking Sandbox Dashboard](https://account.africastalking.com/).
   - Navigate to **USSD > Service Codes > Create Channel**.
   - Set Channel Shortcode (e.g., `*384*73355#`).
   - Set Callback URL to:  
     `https://xyz.ngrok-free.app/api/v1/ussd`
   - Save the channel.

3. **Launch the Web Simulator**:
   - In Africa's Talking, open the **USSD Simulator**.
   - Enter your registered test phone number (`+254712345678`).
   - Dial `*384*73355#`.
   - The interactive MzaziRada menu will appear on the simulated screen!

---

## 📊 Google Sheets & Apps Script Integration

1. Follow the instructions in [sample_data/README.md](sample_data/README.md) to populate your sheet with `students.csv` and `fee_ledger.csv`.
2. Follow the steps in [apps_script/README.md](apps_script/README.md) to add `Code.gs` to **Extensions > Apps Script**.
3. Use the **MzaziRada SMS > Setup Script Properties** menu in your spreadsheet to link your backend URL and `WEBHOOK_SECRET`.
4. Click **MzaziRada SMS > Send Fee Reminders to Parents** to trigger updates and SMS alerts automatically!

---

## 🗺️ Roadmap

- [ ] Multi-tenant support (Multiple schools separated by tenant ID).
- [ ] Multilingual USSD menu switching (English & Kiswahili).
- [ ] Persistent SQLite / PostgreSQL storage with Redis caching.
- [ ] Automated M-Pesa Daraja STK Push integration for instant fee settlement directly from the USSD session.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Feel free to use and adapt this project for educational and community impact.
