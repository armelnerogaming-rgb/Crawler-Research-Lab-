# Render deployment (first supervised release)

This application is an early prototype, not a multi-user production crawler.
The Render Blueprint is in `render.yaml`. Create a **new Blueprint** at
https://dashboard.render.com/select-repo?type=blueprint and select this repository.

## Required settings
- `CRAWLER_API_TOKEN`: generated securely by Render; do not commit or expose in public frontend build variables.
- `CRAWL_ALLOWED_HOSTS`: required exact host allowlist, e.g. `example.org,www.example.org`.
- `ALLOWED_ORIGINS`: exact deployed Lovable origin, e.g. `https://your-app.lovable.app`.
- `OPENAI_API_KEY`: optional; add in Render dashboard only.
- Keep **one** Uvicorn worker. Jobs are in memory and will disappear across restarts.

## Before broad public use
Do not allow arbitrary crawling until you have IP-pinned outbound connections or
an egress firewall rejecting loopback/private/link-local/metadata addresses even
after DNS rebinding. The existing DNS checks alone do **not** guarantee SSRF prevention.
Add accounts, per-user quotas, durable queue, streaming response-size limits and
rate throttling. This Blueprint requires an exact host allowlist to reduce exposure,
but is **not a substitute for network egress protection**.

The current Lovable frontend needs a secure token-entry flow before it can call
authenticated `/api/crawl`, `/api/crawl/{id}`, and `/api/research` endpoints.
Do not put `CRAWLER_API_TOKEN` into any `VITE_*` variable or bundled JS.

## Verify
Check `/api/health`, then from an authorized client use `Authorization: Bearer <token>`
for crawl/research calls. Confirm robots.txt policy is respected and blocked URLs
never initiate crawling. Expect free-service cold starts and job loss on restart.
