# API — Azure Static Web Apps managed functions

This folder is the `api_location` of the Azure Static Web Apps deployment
(`.github/workflows/azure-static-web-apps-proud-pond-06dc10c1e.yml`). Azure
builds it automatically on deploy and serves it under `/api/` on the same
host as the site — no separate deployment step.

One function ships today:

| Route | File | Purpose |
| --- | --- | --- |
| `POST /api/chat` | `src/functions/chat.js` | Proxies the site's AI chat widget to the Anthropic Messages API. The key lives in an Azure application setting (`ANTHROPIC_API_KEY`), never in the repo or the browser. |

Full documentation — activation switches, environment variables, hardening,
and how this relates to the GitHub Pages deployment — lives in
[`docs/automation.md`](../docs/automation.md).

## Local run (optional)

Requires Node 18+ and Azure Functions Core Tools v4:

```bash
cd api
npm install
cp local.settings.json.sample local.settings.json   # then set ANTHROPIC_API_KEY
func start
```

The function listens on `http://localhost:7071/api/chat`. Note the theme also
ships its own Node dev proxy for local chat testing; see
`templates/deploy/chat-proxy/` in the zer0-mistakes theme repo.
