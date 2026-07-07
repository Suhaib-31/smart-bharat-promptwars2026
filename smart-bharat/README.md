# 🇮🇳 Smart Bharat — AI-Powered Civic Companion

> Built for **PromptWars 2026**

Smart Bharat is a GenAI-powered web platform that helps Indian citizens access
government services, report public issues, and receive personalized assistance
through an intelligent AI companion — powered by **Google Gemini**.

![Tech Stack](https://img.shields.io/badge/Flask-Python-blue) ![Tailwind](https://img.shields.io/badge/TailwindCSS-UI-38bdf8) ![Gemini](https://img.shields.io/badge/Google-Gemini%20API-orange) ![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 **Landing Page** | Premium Material-Design inspired UI with glassmorphism, gradients, and animations |
| 🤖 **AI Civic Assistant** | Gemini-powered chatbot answering questions on schemes, taxes, Aadhaar, PAN, passports, health, education, agriculture & welfare |
| 🔍 **Government Service Finder** | Select a category → AI recommends the relevant service, eligibility, documents, process & estimated time |
| 📄 **Document Guide** | Step-by-step guides for Passport, Driving License, Birth Certificate, Income Certificate, Domicile, Pension, Scholarship |
| 📝 **Complaint Assistant** | Enter complaint type, location & description → AI drafts a professional complaint letter |
| 📍 **Complaint Tracker** | Auto-generated tracking IDs with simulated status progression (Received → In Progress → Assigned → Resolved), backed by SQLite |
| 🌐 **Multilingual Support** | English & Hindi, powered by Gemini translation |
| 🌗 **Dark / Light Mode** | Persistent theme toggle |
| 🎙️ **Voice Input** | Speak your questions using the Web Speech API |
| 🔊 **Speech Output** | Listen to AI responses via speech synthesis |
| 📋 **Copy Response** | One-click copy for AI responses and generated complaints |
| ✍️ **Markdown Rendering** | Rich formatted AI responses |
| 💬 **Recent Chat History** | Chat history stored per session (SQLite) + locally in browser |

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask (application factory + blueprints)
- **Frontend:** HTML5, Tailwind CSS (CDN), Vanilla JavaScript
- **AI:** Google Gemini API (`google-generativeai` SDK)
- **Database:** SQLite
- **Templating:** Jinja2
- **Icons:** Lucide Icons
- **Markdown Rendering:** marked.js

---

## 📁 Project Structure

```
smart-bharat/
├── app.py                     # Main Flask application entrypoint (app factory)
├── config.py                  # Environment-based configuration
├── requirements.txt            # Python dependencies
├── Procfile                    # Process file for Render/Railway
├── runtime.txt                 # Python version pin
├── render.yaml                  # Render deployment blueprint
├── .env.example                 # Example environment variables
├── .gitignore
├── README.md
│
├── routes/                     # Flask blueprints (controllers)
│   ├── main_routes.py            # Home, About, Contact
│   ├── chat_routes.py            # AI Civic Assistant chat + API
│   ├── services_routes.py        # Service Finder + Document Guide
│   └── complaint_routes.py       # Complaint Assistant + Tracker
│
├── services/                   # Business logic / external integrations
│   ├── gemini_service.py         # All Gemini API calls (chat, recommend, complaint, translate)
│   └── data_service.py           # Static reference data (categories, document guides)
│
├── models/                     # Database access layer
│   ├── complaint_model.py
│   ├── contact_model.py
│   └── chat_model.py
│
├── database/
│   ├── db.py                     # SQLite connection + init helper
│   └── schema.sql                # Table definitions
│
├── utils/
│   └── helpers.py                # Tracking ID generation, status simulation
│
├── templates/                  # Jinja2 templates
│   ├── base.html                  # Shared layout (navbar, footer, theme)
│   ├── index.html                 # Landing page
│   ├── chat.html                  # AI Assistant
│   ├── services.html              # Service Finder
│   ├── documents.html             # Document Guide
│   ├── complaint.html             # Complaint Assistant
│   ├── tracker.html               # Complaint Tracker
│   ├── about.html
│   ├── contact.html
│   ├── 404.html
│   └── 500.html
│
└── static/
    ├── css/style.css              # Glassmorphism, gradients, animations
    └── js/
        ├── theme.js                 # Dark/Light mode toggle
        ├── main.js                  # Shared UI behavior
        └── chat.js                  # Chat logic, voice input/output, markdown
```

---

## 🚀 Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/smart-bharat.git
cd smart-bharat
```

### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy the example file and fill in your values:
```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
SECRET_KEY=some_random_secret_string
FLASK_ENV=development
PORT=5000
DATABASE_PATH=database/smart_bharat.db
```

### 5. How to get a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key and paste it into your `.env` file as `GEMINI_API_KEY`

> ⚠️ **Never commit your `.env` file or expose your API key in client-side code.**
> This project keeps the key strictly server-side — all Gemini calls happen through
> Flask API routes (`/api/chat`, `/api/services/recommend`, `/api/complaint/generate`).

### 6. Run the application
```bash
python app.py
```

The app will be available at **http://localhost:5000**

The SQLite database (`database/smart_bharat.db`) is created automatically on first run.

---

## 🌍 Deployment Guide

### Deploying to Render

1. Push your code to a GitHub repository.
2. Go to [Render Dashboard](https://dashboard.render.com/) → **New +** → **Web Service**.
3. Connect your GitHub repo.
4. Render will detect `render.yaml` automatically (Blueprint deploy), or configure manually:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variables in the Render dashboard:
   - `GEMINI_API_KEY` → your Gemini API key
   - `GEMINI_MODEL` → `gemini-1.5-flash`
   - `SECRET_KEY` → any random string (or let Render auto-generate)
   - `FLASK_ENV` → `production`
6. Click **Create Web Service**. Render will build and deploy automatically.

### Deploying to Railway

1. Push your code to GitHub.
2. Go to [Railway](https://railway.app/) → **New Project** → **Deploy from GitHub repo**.
3. Select your repository.
4. Railway auto-detects Python. Set the **Start Command** to:
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```
5. Go to the **Variables** tab and add:
   - `GEMINI_API_KEY`
   - `GEMINI_MODEL=gemini-1.5-flash`
   - `SECRET_KEY`
   - `FLASK_ENV=production`
6. Deploy. Railway provides a public URL automatically.

### Deploying to any Python host (Heroku-style / VPS)

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key
export SECRET_KEY=your_secret
gunicorn app:app --bind 0.0.0.0:8000
```

> **Note on SQLite in production:** SQLite works well for demos and small-scale
> deployments, but most free hosting tiers (Render/Railway free plans) use
> **ephemeral filesystems** — meaning the database resets on redeploy. For a
> persistent production database, mount a persistent disk (Render Disks) or
> migrate to a managed Postgres database.

---

## 🔒 Security Notes

- The Gemini API key is **only** read from environment variables (`os.environ`) via `config.py` and is **never** sent to the browser or included in any template/JS file.
- All AI calls happen server-side through Flask API routes.
- `.env` is included in `.gitignore` and must never be committed.
- Use `SECRET_KEY` with a strong random value in production (Flask session signing).

---

## 🩺 Troubleshooting

**Error: `404 NOT_FOUND ... models/gemini-1.5-flash is not found`**
Google has fully retired the Gemini 1.5 model family — all requests to `gemini-1.5-*` now
return a 404. This project defaults to `gemini-2.5-flash`, which is the current stable
model. If you still see this error:
1. Open your `.env` file and make sure `GEMINI_MODEL=gemini-2.5-flash` (not `gemini-1.5-flash`).
2. Restart the Flask app after editing `.env` (`Ctrl+C` then `python app.py` again) — env vars are only read on startup.
3. If Google has released a newer model by the time you read this, check the current list at
   https://ai.google.dev/gemini-api/docs/models and update `GEMINI_MODEL` accordingly
   (e.g. `gemini-flash-latest` is an alias that always points to the newest Flash model).

**Error: `GEMINI_API_KEY is not set`**
Your `.env` file is missing or wasn't loaded. Confirm `.env` exists in the project root
(not just `.env.example`) and contains a real key, then restart the app.

**Render/Railway deploy works but AI features fail**
Double-check that `GEMINI_API_KEY` and `GEMINI_MODEL` are added under that platform's
**Environment Variables** settings (not just your local `.env` — that file is never
uploaded since it's in `.gitignore`).

---

## 🧪 Quick Feature Test Checklist

- [ ] Visit `/` — landing page loads with hero, features, and CTA
- [ ] Toggle dark/light mode — persists on reload
- [ ] Visit `/chat` — send a message, get AI response, try voice input & listen button
- [ ] Visit `/services` — select a category, get AI recommendation
- [ ] Visit `/documents` — select a document type, view guide
- [ ] Visit `/complaint` — fill form, generate complaint, get tracking ID
- [ ] Visit `/tracker?id=<tracking_id>` — view live status
- [ ] Visit `/contact` — submit the form, see success flash message
- [ ] Switch language dropdown to Hindi in Chat/Services/Complaint

---

## 📜 License

This project was built as a hackathon submission for **PromptWars 2026**.
Free to use, modify, and extend for educational and non-commercial purposes.

---

## 🙌 Acknowledgements

- [Google Gemini API](https://ai.google.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)
- [Flask](https://flask.palletsprojects.com/)
