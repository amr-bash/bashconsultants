/**
 * ===================================================================
 * bashconsultants.com AI Chat Proxy — Azure Static Web Apps managed function
 * ===================================================================
 *
 * File: api/src/functions/chat.js
 * Route: POST /api/chat  (SWA prefixes managed-function routes with /api)
 *
 * Server-side companion for the zer0-mistakes theme chat widget
 * (theme files: _includes/components/ai-chat.html + assets/js/ai-chat.js).
 * Ported from the theme's Cloudflare Worker reference implementation at
 * templates/deploy/chat-proxy/worker.js — chat route only. The worker's
 * GitHub issue/PR routes are NOT ported: this site runs ai_chat.github.mode
 * 'url' (pre-filled github.com forms), which needs no server-side token.
 *
 * Contract with the widget (assets/js/ai-chat.js):
 *   Request:  POST { model, max_tokens, system, messages, tools?, stream: true }
 *   Response: Anthropic Messages API SSE stream passed through unchanged,
 *             or a plain JSON message object — the widget accepts both.
 *   Errors:   { error: { message } } with an HTTP status the widget maps
 *             to a friendly message.
 *
 * Auth: API key only (process.env.ANTHROPIC_API_KEY, set as an Azure
 * Static Web App application setting — never in the repo, never echoed).
 * The worker's personal OAuth modes are intentionally not ported; a
 * workspace-scoped API key with a spend cap is the right shape for a
 * public site.
 *
 * Hardening:
 *   - POST only (OPTIONS answered for preflight)
 *   - Origin allowlist (production domains + this SWA's own hostnames)
 *   - Request body size cap
 *   - Server-side max_tokens cap and optional model pin
 *   - Simple fixed-window in-memory rate limit per client IP
 *
 * Optional application settings (all have safe defaults):
 *   CHAT_MODEL            — pin the model server-side (overrides the client)
 *   MAX_TOKENS_CAP        — cap on client-requested max_tokens (default 4096)
 *   MAX_BODY_BYTES        — request body cap in bytes (default 524288)
 *   ALLOWED_ORIGINS       — comma-separated extra allowed origins
 *   RATE_LIMIT_MAX        — requests per window per IP (default 20)
 *   RATE_LIMIT_WINDOW_MS  — window length in ms (default 60000)
 *   CHAT_BUFFER_RESPONSE  — 'true' to buffer the upstream SSE body instead
 *                           of streaming it (fallback if the managed runtime
 *                           rejects HTTP streaming; the widget handles both)
 * ===================================================================
 */

'use strict';

const { app } = require('@azure/functions');

// HTTP streaming requires Functions runtime >= 4.28 and @azure/functions >= 4.3,
// both standard on SWA managed functions with a node:18+ apiRuntime.
app.setup({ enableHttpStream: true });

const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_VERSION = '2023-06-01';
const DEFAULT_MODEL = 'claude-opus-4-8'; // mirrors ai_chat.model in _config.yml
const DEFAULT_MAX_TOKENS = 1024;
const DEFAULT_MAX_TOKENS_CAP = 4096;
const DEFAULT_MAX_BODY_BYTES = 512 * 1024; // widget can attach ~48 KB page-source tool results
const DEFAULT_RATE_LIMIT_MAX = 20;
const DEFAULT_RATE_LIMIT_WINDOW_MS = 60_000;
const MAX_TOOLS = 16;

// Production origins plus this Static Web App's own default and staging
// hostnames (staging environments look like <name>-<pr>.<region>.azurestaticapps.net).
const STATIC_ALLOWED_ORIGINS = [
  'https://bashconsultants.com',
  'https://www.bashconsultants.com',
  'https://bash-365.com',
  'https://www.bash-365.com',
];
const SWA_ORIGIN_PREFIX = 'https://proud-pond-06dc10c1e';
const SWA_ORIGIN_SUFFIX = '.azurestaticapps.net';

// --- CORS / origin gate ------------------------------------------------

function allowedOrigins() {
  const extra = (process.env.ALLOWED_ORIGINS || '')
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);
  return STATIC_ALLOWED_ORIGINS.concat(extra);
}

function originAllowed(origin) {
  // Browsers always send Origin on POST; a missing Origin means a
  // non-browser client, which has no business spending the API credential.
  if (!origin) return false;
  if (allowedOrigins().includes(origin)) return true;
  return origin.startsWith(SWA_ORIGIN_PREFIX) && origin.endsWith(SWA_ORIGIN_SUFFIX);
}

function corsHeaders(origin) {
  const headers = {
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'content-type',
    'Access-Control-Max-Age': '86400',
  };
  if (origin && originAllowed(origin)) {
    headers['Access-Control-Allow-Origin'] = origin;
    headers['Vary'] = 'Origin';
  }
  return headers;
}

function jsonError(message, status, cors) {
  return {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...cors },
    body: JSON.stringify({ error: { message } }),
  };
}

// --- Rate limit (fixed window, per instance, per IP) ---------------------

const rateBuckets = new Map(); // ip -> { windowStart, count }

function clientIp(request) {
  const forwarded = request.headers.get('x-forwarded-for') || '';
  // Key on the LAST hop, not the first. On Azure Static Web Apps / App Service
  // the trusted front end APPENDS the real client IP to whatever the caller sent,
  // so the first comma-separated entry is attacker-controlled (a client can spoof
  // it to dodge or poison the per-IP limit). The last entry is the value the
  // trusted proxy added.
  const parts = forwarded.split(',');
  let ip = parts[parts.length - 1].trim();
  if (ip.startsWith('[')) {
    // bracketed IPv6 with port: [::1]:12345
    ip = ip.slice(1, ip.indexOf(']') > 0 ? ip.indexOf(']') : undefined);
  } else if ((ip.match(/:/g) || []).length === 1) {
    // IPv4 with port: 203.0.113.7:54321
    ip = ip.split(':')[0];
  }
  return ip || 'unknown';
}

function rateLimited(ip) {
  const max = Number(process.env.RATE_LIMIT_MAX) || DEFAULT_RATE_LIMIT_MAX;
  const windowMs = Number(process.env.RATE_LIMIT_WINDOW_MS) || DEFAULT_RATE_LIMIT_WINDOW_MS;
  const now = Date.now();

  // Opportunistic sweep so the map cannot grow without bound.
  if (rateBuckets.size > 5000) {
    for (const [key, bucket] of rateBuckets) {
      if (now - bucket.windowStart > windowMs) rateBuckets.delete(key);
    }
  }

  const bucket = rateBuckets.get(ip);
  if (!bucket || now - bucket.windowStart > windowMs) {
    rateBuckets.set(ip, { windowStart: now, count: 1 });
    return false;
  }
  bucket.count += 1;
  return bucket.count > max;
}

// --- Handler -------------------------------------------------------------

async function chatHandler(request, context) {
  const origin = request.headers.get('origin') || '';
  const cors = corsHeaders(origin);

  if (request.method === 'OPTIONS') {
    return { status: 204, headers: cors };
  }
  if (request.method !== 'POST') {
    return jsonError('Method not allowed', 405, cors);
  }
  if (!originAllowed(origin)) {
    return jsonError('Origin not allowed', 403, cors);
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    // proxy_ready should stay false in _config.yml until this is set.
    return jsonError('Chat is not configured on this deployment', 503, cors);
  }

  if (rateLimited(clientIp(request))) {
    return jsonError('Too many requests — please wait a minute and try again', 429, cors);
  }

  const maxBodyBytes = Number(process.env.MAX_BODY_BYTES) || DEFAULT_MAX_BODY_BYTES;
  const declaredLength = Number(request.headers.get('content-length'));
  if (declaredLength && declaredLength > maxBodyBytes) {
    return jsonError('Request body too large', 413, cors);
  }

  let rawBody;
  try {
    rawBody = await request.text();
  } catch (err) {
    return jsonError('Invalid request body', 400, cors);
  }
  if (Buffer.byteLength(rawBody, 'utf8') > maxBodyBytes) {
    return jsonError('Request body too large', 413, cors);
  }

  let body;
  try {
    body = JSON.parse(rawBody);
  } catch (err) {
    body = null;
  }
  if (!body || !Array.isArray(body.messages) || body.messages.length === 0) {
    return jsonError('Invalid request body', 400, cors);
  }

  const cap = Number(process.env.MAX_TOKENS_CAP) || DEFAULT_MAX_TOKENS_CAP;
  const payload = {
    // Model is pinned server-side (CHAT_MODEL app setting, else DEFAULT_MODEL) —
    // the client's body.model is ignored so a tampered request cannot select a
    // more expensive model and run up spend.
    model: process.env.CHAT_MODEL || DEFAULT_MODEL,
    max_tokens: Math.min(Number(body.max_tokens) || DEFAULT_MAX_TOKENS, cap),
    system: typeof body.system === 'string' ? body.system : undefined,
    messages: body.messages,
    tools: Array.isArray(body.tools) ? body.tools.slice(0, MAX_TOOLS) : undefined,
    stream: true,
  };

  let upstream;
  try {
    upstream = await fetch(ANTHROPIC_URL, {
      method: 'POST',
      headers: {
        'x-api-key': apiKey,
        'anthropic-version': ANTHROPIC_VERSION,
        'content-type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  } catch (err) {
    context.error('Upstream request to Anthropic failed:', err.message);
    return jsonError('Upstream request failed', 502, cors);
  }

  const responseHeaders = {
    'content-type': upstream.headers.get('content-type') || 'application/json',
    'cache-control': 'no-store',
    ...cors,
  };

  // Stream the SSE body straight through (error bodies pass through as JSON).
  // CHAT_BUFFER_RESPONSE=true buffers instead — the widget parses a complete
  // SSE payload the same way, just without incremental rendering.
  if (process.env.CHAT_BUFFER_RESPONSE === 'true' || !upstream.body) {
    return { status: upstream.status, headers: responseHeaders, body: await upstream.text() };
  }
  return { status: upstream.status, headers: responseHeaders, body: upstream.body };
}

app.http('chat', {
  methods: ['POST', 'OPTIONS'],
  authLevel: 'anonymous',
  route: 'chat',
  handler: chatHandler,
});
