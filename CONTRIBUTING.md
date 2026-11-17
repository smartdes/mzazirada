# Contributing to MzaziRada

Thank you for your interest in contributing to MzaziRada! We welcome contributions to make school communication more accessible to parents across Africa.

---

## Development Workflow

### 1. Fork & Clone
```bash
git clone https://github.com/your-username/mzazirada.git
cd mzazirada
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate
# Or Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies including dev tools
pip install -r requirements-dev.txt

# Create .env from template
cp .env.example .env
```

### 3. Run the Test Suite
Ensure all existing tests pass before making any changes:
```bash
pytest -v
```

### 4. Code Standards
- Keep USSD responses concise (under 160 characters per screen where possible to prevent pagination truncation).
- Never commit private keys, real phone numbers, or student data. Always use fictional E.164 numbers (e.g. `+254712345678`).
- Maintain type hints with Pydantic schemas.

### 5. Submitting Changes
1. Create a descriptive branch: `git checkout -b feature/multilingual-support`
2. Commit your changes with clear messages.
3. Push to your fork and submit a Pull Request against the main branch.
