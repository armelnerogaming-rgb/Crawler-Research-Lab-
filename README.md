# Crawler Research Lab

Standalone visual web crawler and AI research PWA.

## Quickstart

Backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`

Frontend: `cd frontend && npm install && npm run dev`

Set `VITE_API_URL=http://localhost:8000` for local API access.

Crawler is bounded to same-site pages, respects `robots.txt`, uses a per-request delay, and limits page count. Do not use on sites without permission. Optional `OPENAI_API_KEY` enables AI synthesis; otherwise sourced excerpts are returned.
