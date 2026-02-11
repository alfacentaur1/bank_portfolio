# Bank Application Portfolio Analyzer

## Technical Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Django 5.1+ (Python 3.11) |
| **Frontend** | Tailwind CSS, HTMX, Alpine.js |
| **DB** | sqlite3 |
| **AI / LLM** | OpenAI API (GPT-4o) |
| **Visuals** | Mermaid.js, Chart.js |

---

### 1. Prerequisites
Ensure you have **Python 3.11** or higher installed.

### 2. Environment Configuration
Create a `.env` file in the root directory and add your OpenAI API key:
```text
OPENAI_API_KEY=your_sk_key_here

# Install required packages
pip install django openai python-dotenv

# Run migrations to set up the database schema
python manage.py migrate

# Generate the portfolio using AI (this takes 30-60 seconds)
python manage.py seed_data

# Run server
python manage.py runserver

Visit the application at http://127.0.0.1:8000/ (typically)

### 3. Demo instructions
# Analysis 
Dashboard > Run AI audit
Dashboard > AI reports

# Q&A
Dashboard > Ask AI Assistant

# Mermaid
Dashboard > Inventory > Detail > GENERATE ARCHITECTURE 

# CRUD
Dashboard > Integrations

### 4. Improvements
Monitoring: Log changes and audit trails.

Tests: Automated tests for AI logic.

Authentication: Secure login via Django system.

User Roles: Groups for architects and managers.


