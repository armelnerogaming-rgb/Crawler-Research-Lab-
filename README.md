# Crawler Research Lab

Standalone Python FastAPI + React PWA website crawler and research agent.

## Architecture
React PWA → FastAPI job endpoints → per-job async crawler → link graph and text extraction → cited research (OpenAI optional).

## Run locally

Terminal 1:
```sh
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Terminal 2:
```sh
cd frontend
npm install
npm run dev
```
Visit http://localhost:5173. Set `OPENAI_API_KEY` in backend environment to enable synthesized research; no key uses cited excerpts. Set `OPENAI_MODEL` to adjust model and `ALLOWED_ORIGINS` for production frontend URL. `npm run build` produces installable PWA assets (HTTPS required outside localhost).

## Safety and limitations
- Public HTTP/HTTPS sites only, standard ports; attempts to block localhost, private IPs, link-local IPs, credential-bearing URLs.
- Only same-host links, maximum 50 pages per crawl, at least 1 second between requests, robots.txt must be retrievable and permit crawling. Robots crawl-delay honored. No login, auth bypass, CAPTCHA circumvention or stealth tactics.
- Prototype only: in-memory jobs disappear on restart; server is single-worker; no user authentication, API quota, durable queue, database, real-time WebSockets, automatic deep research across sites, or browser JS rendering.
- Production deployments **must** add egress firewall/network deny rules for private IP ranges (DNS rebinding risk), strict outbound proxy/connection IP pinning, auth + per-user job limits, persistent queues, storage policies, audit logs, retention, size streaming caps, and origin allowlisting where appropriate.
- Use on websites for which you have permission, follow terms and applicable law. Do not crawl personal/sensitive information without authorization.
