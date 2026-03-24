# Portfolio Website

A clean, minimal portfolio with a working contact form. Built with **Flask + SQLite** backend and plain **HTML/CSS/JS** frontend. Deployed via **Render** with a **GitHub Actions CI/CD** pipeline.

---

## Project structure

```
portfolio/
├── app.py                        # Flask app + SQLite contact API
├── requirements.txt              # Python dependencies
├── Procfile                      # For Render/Heroku deployment
├── pytest.ini
├── templates/
│   └── index.html                # Single-page portfolio
├── static/
│   ├── css/style.css
│   └── js/main.js
├── tests/
│   └── test_app.py               # Pytest tests
└── .github/
    └── workflows/
        └── ci-cd.yml             # GitHub Actions CI/CD
```

---

## Run locally

### 1. Clone and set up

```bash
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Start the server

```bash
python app.py
```

Visit **http://localhost:5000** — the SQLite database (`contacts.db`) is created automatically on first run.

### 3. Run tests

```bash
pytest
```

---

## Customise the portfolio

Open `templates/index.html` and update:

| Thing | Where |
|---|---|
| Your name | `<title>`, nav `.nav-name`, hero, footer |
| Hero tagline | `.hero-sub` paragraph |
| About bio | `#about .about-right` paragraphs |
| Skills | `#skills .skill-tags` spans |
| Projects | `#projects .project-card` blocks |
| Email / city | `#contact .contact-info` |
| Social links | `<footer>` anchor tags |

---

## Push to GitHub

```bash
# One-time setup
git init
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git

# Every time you make changes
git add .
git commit -m "your message"
git push origin main
```

---

## Deploy to Render (free)

1. Go to **https://render.com** → New → Web Service
2. Connect your GitHub repo
3. Fill in:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Environment:** Python 3
4. Click **Deploy**
5. Once live, go to **Settings → Deploy hook** and copy the URL

---

## Set up CI/CD (GitHub Actions)

The pipeline (`.github/workflows/ci-cd.yml`) does two things automatically:

1. **On every push/PR** → runs `pytest` tests
2. **On push to `main`** → triggers a Render redeploy (only if tests pass)

### Add the deploy hook secret

1. GitHub repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `RENDER_DEPLOY_HOOK_URL`
4. Value: paste the Render deploy hook URL

That's it. Every `git push origin main` will now: ✅ run tests → ✅ deploy automatically.

---

## API endpoints

| Method | URL | Description |
|---|---|---|
| `GET` | `/` | Portfolio page |
| `POST` | `/api/contact` | Submit contact form (saves to SQLite) |
| `GET` | `/api/messages` | View all messages (admin use) |

### Contact form payload

```json
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello!"
}
```

### Response

```json
{ "success": true, "message": "Message received! I'll be in touch soon." }
```
