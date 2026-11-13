# MedSpin 🩺

**MedSpin** is a simple, interactive medical learning application that helps you revise diseases through a randomized spinner. Spin to discover a new disease, explore its clinical aspects, and keep track of your learning progress.

🌐 **Live Demo:** [MedSpin](https://med-spin-hqoh8c8zv-zain-ul-abideens-projects-4c66e3a7.vercel.app/)

## Features

- 🎡 **Random Disease Spinner:** Discover a random disease from the available dataset.
- 🚫 **No Repetitions:** Previously explored diseases are excluded from subsequent spins.
- 📚 **Exploration History:** View all previously explored diseases.
- 📊 **Progress Tracking:** Track explored diseases, remaining diseases, and completion percentage.
- 🔄 **Persistent Progress:** Exploration history is stored in PostgreSQL and retained across sessions.
- ♻️ **Reset Progress:** Reset the exploration history and start again.
- ⚡ **Interactive Interface:** Simple, responsive single-page application.

## Tech Stack

| Layer            | Technology |
| ---------------- | ---------- |
| Frontend         | Vue 3      |
| Language         | TypeScript |
| Build Tool       | Vite       |
| Styling          | CSS        |
| Backend          | FastAPI    |
| Backend Language | Python     |
| ORM              | SQLAlchemy |
| Database         | PostgreSQL |
| Database Hosting | Supabase   |
| Backend Hosting  | Render     |
| Frontend Hosting | Vercel     |

## Architecture

```text
                  ┌──────────────────────┐
                  │      Vue 3          │
                  │     Frontend        │
                  │      Vercel          │
                  └──────────┬───────────┘
                             │
                         HTTP API
                             │
                  ┌──────────▼───────────┐
                  │      FastAPI        │
                  │      Backend        │
                  │       Render        │
                  └──────────┬───────────┘
                             │
                         SQLAlchemy
                             │
                  ┌──────────▼───────────┐
                  │     PostgreSQL      │
                  │      Supabase       │
                  └─────────────────────┘
```

## Project Structure

```text
medspin/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── seed.py
│   │   └── test_db.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── style.css
│   │   ├── assets/
│   │   │   └── main.css
│   │   └── data/
│   │       └── diseases.json
│   ├── index.html
│   ├── package.json
│   └── .env
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js and npm
- PostgreSQL database

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/medspin.git
cd medspin
```

### 2. Backend Setup

```bash
cd backend

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```dotenv
DATABASE_URL=your_postgresql_connection_string
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

`http://localhost:8000`

Interactive API documentation:

`http://localhost:8000/docs`

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install
```

Create a `.env` file inside `frontend/`:

```dotenv
VITE_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Frontend runs at:

`http://localhost:5173`

## API Endpoints

| Method | Endpoint                 | Description                  |
| ------ | ------------------------ | ---------------------------- |
| GET    | `/health`                | Check backend health         |
| GET    | `/diseases`              | Retrieve available diseases  |
| GET    | `/explored`              | Retrieve exploration history |
| POST   | `/explored/{disease_id}` | Mark a disease as explored   |
| DELETE | `/explored`              | Reset exploration history    |

## Deployment

MedSpin is deployed using:

- **Frontend:** Vercel
- **Backend:** Render
- **Database:** Supabase PostgreSQL

Environment variables are configured separately for local development and production deployment.

## Learning Objectives

MedSpin was developed as a practical full-stack project to explore:

- Vue.js and reactive frontend development
- REST API development using FastAPI
- PostgreSQL database integration
- SQLAlchemy ORM
- Frontend-backend communication
- Environment variable management
- Cloud deployment and production configuration
- Persistent application state

## Future Improvements

Potential enhancements include:

- Disease information pages
- Epidemiology and pathophysiology summaries
- Pharmacology and treatment information
- Disease categories and difficulty levels
- Search and filtering
- Improved spinner animations
- Personal learning statistics

---

**MedSpin** · A spin toward better medical knowledge.
