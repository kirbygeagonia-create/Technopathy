# TechnoPath — Automated Fix & Verification Prompt
### For: Windsurf Kimi K2.5 AI
### Project: `https://github.com/kirbygeagonia-create/Technopathy.git`

---

## HOW YOU MUST OPERATE — READ FIRST

You are a Senior Software Engineer tasked with fixing every issue listed in this document across the TechnoPath codebase. You must follow this exact loop for **every single issue**:

```
LOOP for each issue:
  1. READ     → Open and read the exact file and line(s) listed
  2. FIX      → Apply the exact code change described
  3. SAVE     → Write the file
  4. VERIFY   → Re-open the file and confirm the fix is present
  5. REPORT   → Print: ✅ FIXED & VERIFIED: [Issue ID] — [one-line description]
             OR  ❌ FAILED: [Issue ID] — [reason] → retry from step 1

After all issues are fixed:
  6. RUN FULL VERIFICATION SCAN → Re-check every issue from the checklist below
  7. Print final VERIFICATION REPORT
  8. If any check fails → go back to step 1 for that issue
  9. Only stop when ALL checks pass
```

Do **not** skip an issue. Do **not** assume a fix is in place without reading the file first. Do **not** stop until the Final Verification Report shows all ✅.

---

## ISSUE LIST — FIX IN ORDER

---

### ISSUE-01 🔴 SQL Injection in Chatbot Analytics
**File:** `chatbot_flask/app.py`
**Lines:** 223, 229

**Problem:** Raw SQL is built using Python's `.format()` with user input — a direct SQL injection vector.

**Find this code:**
```python
cursor = conn.execute(
    "SELECT COUNT(*) FROM chat_history WHERE created_at >= datetime('now', '-{} days')".format(days)
)
```
and:
```python
cursor = conn.execute(
    "SELECT user_message, bot_reply FROM chat_history WHERE created_at >= datetime('now', '-{} days') ORDER BY created_at DESC".format(days)
)
```

**Replace with (parameterized queries):**
```python
cursor = conn.execute(
    "SELECT COUNT(*) FROM chat_history WHERE created_at >= datetime('now', ? || ' days')",
    (f'-{days}',)
)
```
and:
```python
cursor = conn.execute(
    "SELECT user_message, bot_reply FROM chat_history WHERE created_at >= datetime('now', ? || ' days') ORDER BY created_at DESC",
    (f'-{days}',)
)
```

**Verify:** Confirm `.format(days)` no longer appears in any SQL string in this file.

---

### ISSUE-02 🔴 Rate Limiter Disabled — Re-Enable It
**File:** `chatbot_flask/app.py`
**Lines:** ~24–30 (commented-out limiter block) and ~207 (commented-out decorator)

**Problem:** The Flask-Limiter is fully commented out, leaving the OpenAI `/chat` endpoint completely unprotected.

**Step 1 — Uncomment and restore the limiter initialization. Find:**
```python
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["60 per minute"],
#     storage_uri="memory://",
# )
```
**Replace with:**
```python
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"],
    storage_uri="memory://",
)
```

**Step 2 — Re-add the rate limit decorator on the chat route. Find:**
```python
@app.route("/chat", methods=["POST"])
# @limiter.limit("20 per minute")  # Temporarily disabled
def chat():
```
**Replace with:**
```python
@app.route("/chat", methods=["POST"])
@limiter.limit("20 per minute")
def chat():
```

**Verify:** Confirm `limiter = Limiter(` is uncommented AND `@limiter.limit("20 per minute")` is active above the `chat()` function.

---

### ISSUE-03 🟠 JWT Tokens Stored in Insecure localStorage
**File:** `frontend/src/stores/authStore.js`

**Problem:** Both the access token and refresh token are stored in `localStorage`, which is fully readable by any JavaScript on the page (XSS risk).

**Find the login action and add a security comment + move the refresh token to sessionStorage. Find:**
```javascript
localStorage.setItem('tp_token',   access)
localStorage.setItem('tp_refresh', refresh)
localStorage.setItem('tp_user',    JSON.stringify(user))
```
**Replace with:**
```javascript
// SECURITY: access token in sessionStorage (cleared on tab close)
// Refresh token should move to httpOnly cookie in a future backend update
sessionStorage.setItem('tp_token',   access)
sessionStorage.setItem('tp_refresh', refresh)
sessionStorage.setItem('tp_user',    JSON.stringify(user))
```

**Also update the state initializer at the top of the store. Find:**
```javascript
state: () => ({
    user:         JSON.parse(localStorage.getItem('tp_user')  || 'null'),
    token:        localStorage.getItem('tp_token')            || null,
    refreshToken: localStorage.getItem('tp_refresh')          || null,
  }),
```
**Replace with:**
```javascript
state: () => ({
    user:         JSON.parse(sessionStorage.getItem('tp_user')  || 'null'),
    token:        sessionStorage.getItem('tp_token')            || null,
    refreshToken: sessionStorage.getItem('tp_refresh')          || null,
  }),
```

**Also update the logout action. Find:**
```javascript
localStorage.removeItem('tp_token')
localStorage.removeItem('tp_refresh')
localStorage.removeItem('tp_user')
```
**Replace with:**
```javascript
sessionStorage.removeItem('tp_token')
sessionStorage.removeItem('tp_refresh')
sessionStorage.removeItem('tp_user')
```

**Also update the clearTokens action. Find:**
```javascript
localStorage.removeItem('tp_token')
localStorage.removeItem('tp_refresh')
localStorage.removeItem('tp_user')
```
**Replace with (in clearTokens only):**
```javascript
sessionStorage.removeItem('tp_token')
sessionStorage.removeItem('tp_refresh')
sessionStorage.removeItem('tp_user')
```

**File:** `frontend/src/services/api.js`
**Also update the api.js interceptor. Find:**
```javascript
const token = localStorage.getItem('tp_token')
```
**Replace with:**
```javascript
const token = sessionStorage.getItem('tp_token')
```
**And find:**
```javascript
const refresh = localStorage.getItem('tp_refresh')
```
**Replace with:**
```javascript
const refresh = sessionStorage.getItem('tp_refresh')
```
**And find:**
```javascript
localStorage.setItem('tp_token', newToken)
```
**Replace with:**
```javascript
sessionStorage.setItem('tp_token', newToken)
```
**And find:**
```javascript
localStorage.removeItem('tp_token')
localStorage.removeItem('tp_refresh')
```
**Replace with:**
```javascript
sessionStorage.removeItem('tp_token')
sessionStorage.removeItem('tp_refresh')
```

**Verify:** Run: `grep -rn "localStorage.getItem('tp_" frontend/src/` — the output must be empty.

---

### ISSUE-04 🟠 Environment Variable Name Mismatch — Chatbot URL
**File:** `frontend/.env.example`

**Problem:** The code reads `VITE_FLASK_CHATBOT_URL` but the `.env.example` defines `VITE_CHATBOT_URL` (wrong name) pointing to port `5000` (wrong port — Flask runs on `5187`).

**Find:**
```
VITE_CHATBOT_URL=http://localhost:5000
```
**Replace with:**
```
VITE_FLASK_CHATBOT_URL=http://localhost:5187
```

**Verify:** Confirm `VITE_FLASK_CHATBOT_URL` exists and `VITE_CHATBOT_URL` does not exist in `.env.example`. Confirm port is `5187`.

---

### ISSUE-05 🟠 Flask Debug Mode Hardcoded True
**File:** `chatbot_flask/app.py`
**Line:** Last line of file (inside `if __name__ == "__main__":`)

**Problem:** `debug=True` is hardcoded, enabling the Werkzeug interactive debugger (remote code execution risk).

**Find:**
```python
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5187, debug=True)
```
**Replace with:**
```python
if __name__ == "__main__":
    init_db()
    _flask_debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5187, debug=_flask_debug)
```

**Verify:** Confirm `debug=True` no longer exists as a literal in `app.run(...)`.

---

### ISSUE-06 🟠 Git Merge Conflict Markers in .gitignore
**File:** `.gitignore`

**Problem:** The file contains unresolved Git merge conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`). This breaks ignore rules below the conflict.

**Action:** Open `.gitignore`. Locate the conflict block. Remove all conflict marker lines (`<<<<<<< HEAD`, `=======`, `>>>>>>> [hash]`). Keep the desired content from both sides by merging them into a clean list (keep all unique entries from both sides). Then add the following lines if not already present:
```
# Node installers — do not commit binary runtimes
*.msi
*.zip
node-installer.msi
node-portable.zip
nodejs.msi

# Python
__pycache__/
*.pyc
*.pyo
.env
*.db
*.sqlite3

# Build outputs
dist/
node_modules/
staticfiles/
```

**Verify:** Run: `grep -c "<<<<<<" .gitignore` — must output `0`.

---

### ISSUE-07 🟡 Feedback Rating — No Range Validation
**File:** `backend_django/apps/feedback/serializers.py`

**Problem:** `rating` is an unvalidated `IntegerField` — any integer (negative, huge) is accepted.

**Find:**
```python
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['is_flagged', 'flag_reason', 'created_at']
```
**Replace with:**
```python
class FeedbackSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
        allow_null=True,
        required=False,
        help_text='Rating must be between 1 and 5.'
    )

    class Meta:
        model = Feedback
        fields = [
            'id', 'rating', 'comment', 'category',
            'facility', 'room', 'is_anonymous', 'location', 'created_at'
        ]
        read_only_fields = ['id', 'is_flagged', 'flag_reason', 'created_at']
```

**Verify:** Confirm `min_value=1` and `max_value=5` are present in the serializer. Confirm `__all__` is gone.

---

### ISSUE-08 🟡 Audit Log — Hard-Coded 300 Limit With No Pagination
**File:** `backend_django/apps/users/views.py`
**Class:** `AuditLogView`

**Problem:** Results are silently sliced at `[:300]` with no pagination headers or count metadata returned to the client.

**Find:**
```python
qs = qs[:300]
return Response([{
```
**Replace with:**
```python
# Pagination
page_size = min(int(request.query_params.get('page_size', 50)), 200)
page      = max(int(request.query_params.get('page', 1)), 1)
total     = qs.count()
qs        = qs[(page - 1) * page_size : page * page_size]
return Response({
    'count':     total,
    'page':      page,
    'page_size': page_size,
    'pages':     (total + page_size - 1) // page_size,
    'results': [{
```
**And close the dict/list properly — find the closing bracket of the Response list:**
```python
} for l in qs])
```
**Replace with:**
```python
} for l in qs]
})
```

**Verify:** The `AuditLogView.get()` response must contain keys `count`, `page`, `page_size`, `pages`, and `results`.

---

### ISSUE-09 🟡 Token Refresh Uses Relative URL — Breaks in Production
**File:** `frontend/src/services/api.js`
**Line:** Inside the response error interceptor

**Problem:** The token refresh call uses a plain `axios.post('/api/auth/refresh/', ...)` relative URL that only works in local Vite dev (where the proxy exists). In production it fails silently.

**Find:**
```javascript
const res = await axios.post('/api/auth/refresh/', { refresh })
```
**Replace with:**
```javascript
const backendUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
const res = await axios.post(`${backendUrl}/auth/refresh/`, { refresh })
```

**Verify:** Confirm no bare `axios.post('/api/auth/refresh/'` exists in the file. Confirm `VITE_API_BASE_URL` is used for the refresh URL.

---

### ISSUE-10 🟡 Broken Announcement Scopes — Add Clarifying Comment
**File:** `backend_django/apps/announcements/views.py`
**Class:** `AnnouncementPublicListView.get()`

**Problem:** The scopes `all_college` and `basic_ed_only` check for roles (`college_student`, `basic_ed_student`) that do not exist in `AdminUser.ROLE_CHOICES`. These scopes silently drop all matching announcements — they are permanently invisible to every user.

**Find:**
```python
elif a.scope == 'all_college' and getattr(user, 'role', None) == 'college_student':
    visible.append(a)
elif a.scope == 'basic_ed_only' and getattr(user, 'role', None) == 'basic_ed_student':
    visible.append(a)
```
**Replace with:**
```python
# NOTE: 'all_college' and 'basic_ed_only' scopes are reserved for a future
# student-facing authentication system. The roles 'college_student' and
# 'basic_ed_student' do not currently exist in AdminUser.ROLE_CHOICES.
# Until student auth is implemented, announcements with these scopes are
# intentionally not shown to any user. Do not add these scopes via the
# admin panel without first implementing student role support.
elif a.scope == 'all_college' and getattr(user, 'role', None) == 'college_student':
    visible.append(a)  # Placeholder — no users currently hold this role
elif a.scope == 'basic_ed_only' and getattr(user, 'role', None) == 'basic_ed_student':
    visible.append(a)  # Placeholder — no users currently hold this role
```

**Also add the same note as a docstring on the model's `is_visible_to()` method in `backend_django/apps/announcements/models.py`. Find:**
```python
def is_visible_to(self, user):
    """Check if this announcement should be visible to a given user"""
```
**Replace with:**
```python
def is_visible_to(self, user):
    """Check if this announcement should be visible to a given user.

    NOTE: 'all_college' and 'basic_ed_only' scopes require student role support
    (roles: 'college_student', 'basic_ed_student') which is not yet implemented.
    These scopes will match no users until student auth is added.
    """
```

**Verify:** Confirm the clarifying comment block is present in both files.

---

### ISSUE-11 🟡 Flask Chatbot Service Missing From Render Deployment
**File:** `render.yaml`

**Problem:** The Flask chatbot service has no entry in `render.yaml`. It will not deploy on Render.

**Append the following service block at the end of the `services:` list in `render.yaml`:**
```yaml
  # Chatbot - Flask AI Service
  - type: web
    name: technopath-chatbot
    runtime: python
    plan: free
    rootDir: chatbot_flask
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: FLASK_DEBUG
        value: "false"
      - key: OPENAI_API_KEY
        sync: false  # Set this manually in the Render dashboard — never commit the key
```

**Verify:** Confirm `name: technopath-chatbot` exists in `render.yaml`. Confirm `FLASK_DEBUG: false` is set. Confirm `OPENAI_API_KEY` has `sync: false`.

---

### ISSUE-12 🔵 DEBUG Defaults to True in Django Settings
**File:** `backend_django/technopath/settings.py`
**Line:** ~9

**Problem:** `default=True` for `DEBUG` means any misconfigured deployment runs in debug mode, exposing full stack traces to the public.

**Find:**
```python
_debug = config('DEBUG', default=True, cast=bool)
```
**Replace with:**
```python
_debug = config('DEBUG', default=False, cast=bool)
```
**And find:**
```python
DEBUG = config('DEBUG', default=True, cast=bool)
```
**Replace with:**
```python
DEBUG = config('DEBUG', default=False, cast=bool)
```

**Verify:** Run: `grep "default=True" backend_django/technopath/settings.py` — result must be empty.

---

### ISSUE-13 🔵 WhiteNoise Listed in Requirements but Missing From Middleware
**File:** `backend_django/technopath/settings.py`

**Problem:** `whitenoise` is in `requirements.txt` but `WhiteNoiseMiddleware` is absent from `MIDDLEWARE`, so it never actually serves static files.

**Find:**
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
```
**Replace with:**
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
```

**Also add the WhiteNoise storage backend after the `STATIC_ROOT` line. Find:**
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```
**Replace with:**
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Verify:** Confirm `whitenoise.middleware.WhiteNoiseMiddleware` appears in `MIDDLEWARE` immediately after `SecurityMiddleware`. Confirm `STATICFILES_STORAGE` is set.

---

### ISSUE-14 🔵 API Throttle Rates Excessively Permissive (1000/min)
**File:** `backend_django/technopath/settings.py`

**Problem:** 1000 requests per minute per IP provides no meaningful protection.

**Find:**
```python
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/minute',
        'user': '1000/minute',
    },
```
**Replace with:**
```python
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '120/minute',
    },
```

**Verify:** Confirm no `1000/minute` value exists in `settings.py`.

---

### ISSUE-15 🔵 Production Guard for Missing DATABASE_URL
**File:** `backend_django/technopath/settings.py`

**Problem:** If `DATABASE_URL` is missing in a production Render deployment, Django silently falls back to SQLite — which Render wipes on every restart, causing total data loss.

**Find the database configuration block:**
```python
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production - use PostgreSQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Local development - use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'technopath.db',
        }
    }
```
**Replace with:**
```python
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production — use PostgreSQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
elif not DEBUG:
    # Safety guard: refuse to start in production without a real database.
    # Render's free SQLite would be wiped on every restart — all data lost.
    raise RuntimeError(
        '\n\n'
        '  DATABASE_URL is not set and DEBUG=False.\n'
        '  This means the app is running in production without a database.\n'
        '  Create a PostgreSQL instance in Render and set DATABASE_URL.\n'
        '  Never use SQLite in production on Render (it is wiped on restart).\n'
    )
else:
    # Local development — SQLite is fine
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'technopath.db',
        }
    }
```

**Verify:** Confirm the `elif not DEBUG: raise RuntimeError(...)` guard block is present.

---

### ISSUE-16 🔵 Insecure Placeholder in .env.example
**File:** `.env.example` (root level)

**Problem:** The example `SECRET_KEY` uses Django's own `django-insecure-` prefix, which is a known test value and could be copied into production by mistake.

**Find:**
```
SECRET_KEY=django-insecure-technopath-seait-dev-key-change-in-production
```
**Replace with:**
```
SECRET_KEY=REPLACE_WITH_50_RANDOM_CHARS_NEVER_COMMIT_THIS_VALUE
```

**Verify:** Confirm `django-insecure-` no longer appears in `.env.example`.

---

### ISSUE-17 🔵 PWA skipWaiting Conflicts With registerType: prompt
**File:** `frontend/vite.config.js`

**Problem:** `skipWaiting: true` activates a new Service Worker immediately, but `registerType: 'prompt'` shows the user a confirmation prompt first. These settings contradict each other — the SW updates regardless of the user's choice.

**Find:**
```javascript
      workbox: {
        cleanupOutdatedCaches: true,
        skipWaiting: true,
        clientsClaim: true,
```
**Replace with:**
```javascript
      workbox: {
        cleanupOutdatedCaches: true,
        // skipWaiting removed: registerType 'prompt' shows the user a dialog before
        // activating a new SW. Setting skipWaiting:true would override that dialog
        // and update immediately, making the prompt meaningless.
        clientsClaim: true,
```

**Verify:** Confirm `skipWaiting` does not exist in `vite.config.js`.

---

### ISSUE-18 🔵 Missing 404 Catch-All Route in Vue Router
**File:** `frontend/src/router/index.js`

**Problem:** No catch-all route defined — unmatched URLs render a blank white page with no feedback.

**Find the closing of the `routes` array (the last route before `]`):**
```javascript
  { path: '/info/:type',      component: () => import('../views/InfoView.vue'), props: true },
```
**After that line, add:**
```javascript
  { path: '/info/:type',      component: () => import('../views/InfoView.vue'), props: true },

  // 404 — catch all unmatched routes
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/HomeView.vue'), // Redirect to Home as fallback
    beforeEnter: (to, from, next) => {
      console.warn(`[Router] No route matched: ${to.fullPath} — redirecting to home`)
      next('/')
    }
  },
```

**Verify:** Confirm `/:pathMatch(.*)*` exists in the routes array.

---

### ISSUE-19 🔵 Splash Screen Shows on Every Refresh — Add Session Guard
**File:** `frontend/src/router/index.js`
**Inside:** `router.beforeEach()`

**Problem:** The splash screen triggers on every direct navigation to `/` — including browser refreshes — because `from.matched.length === 0` is always true on page reload.

**Find:**
```javascript
router.beforeEach((to, from, next) => {
  // Show splash only when directly accessing home (initial load/refresh)
  // NOT when navigating from other pages like /navigate, /settings, etc.
  // from.matched.length === 0 means no previous route (initial load)
  const isInitialLoad = from.matched.length === 0
  if (to.path === '/' && isInitialLoad) {
    next('/splash')
    return
  }
```
**Replace with:**
```javascript
router.beforeEach((to, from, next) => {
  // Show splash only once per browser session (not on every refresh)
  const isInitialLoad = from.matched.length === 0
  const hasSeenSplash = sessionStorage.getItem('tp_splash_seen')
  if (to.path === '/' && isInitialLoad && !hasSeenSplash) {
    sessionStorage.setItem('tp_splash_seen', '1')
    next('/splash')
    return
  }
```

**Verify:** Confirm `sessionStorage.getItem('tp_splash_seen')` is present in the router guard.

---

### ISSUE-20 🔵 Flask Chatbot Ignores Conversation History Sent by Frontend
**File:** `chatbot_flask/app.py`
**Function:** `generate_reply()`

**Problem:** The frontend sends a `history` array with each `/chat` request, but the Flask server ignores it entirely. Every OpenAI call is a single-turn exchange with no context of prior messages.

**Find the `generate_reply` function:**
```python
def generate_reply(message: str) -> str:
    """Generate AI-powered response using OpenAI GPT, with rule-based fallback."""
    if not OPENAI_ENABLED or not client:
        return generate_rule_based_reply(message)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": CAMPUS_CONTEXT},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.7
        )
```
**Replace with:**
```python
def generate_reply(message: str, history: list = None) -> str:
    """Generate AI-powered response using OpenAI GPT, with rule-based fallback.
    
    Args:
        message: The current user message.
        history: Optional list of prior turns [{role, content}, ...] for context.
    """
    if not OPENAI_ENABLED or not client:
        return generate_rule_based_reply(message)
    try:
        # Build message list: system prompt + prior history (last 6 turns) + current message
        prior = (history or [])[-6:]
        messages = [{"role": "system", "content": CAMPUS_CONTEXT}]
        messages.extend({"role": h["role"], "content": str(h["content"])[:500]} for h in prior)
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
```

**Also update the call-site in the `/chat` endpoint. Find:**
```python
    reply = generate_reply(message)
```
**Replace with:**
```python
    history = data.get("history", [])
    reply = generate_reply(message, history=history)
```

**Verify:** Confirm `generate_reply` accepts a `history` parameter. Confirm `history = data.get("history", [])` is in the `/chat` endpoint. Confirm `messages.extend(...)` with prior history is present.

---

## FINAL VERIFICATION CHECKLIST

After completing all fixes above, re-check every item below. Print `✅` or `❌` for each.

```
SECURITY
[ ] ISSUE-01: grep -n "\.format(days)" chatbot_flask/app.py  → must return 0 results
[ ] ISSUE-02: grep -n "limiter = Limiter" chatbot_flask/app.py  → must return 1 result (uncommented)
[ ] ISSUE-02: grep -n "@limiter.limit" chatbot_flask/app.py  → must return 1 result (uncommented)
[ ] ISSUE-03: grep -rn "localStorage.getItem('tp_" frontend/src/  → must return 0 results
[ ] ISSUE-05: grep -n "debug=True" chatbot_flask/app.py  → must return 0 results
[ ] ISSUE-12: grep -n "default=True" backend_django/technopath/settings.py  → must return 0 results
[ ] ISSUE-16: grep -n "django-insecure" .env.example  → must return 0 results

CONFIGURATION
[ ] ISSUE-04: grep -n "VITE_FLASK_CHATBOT_URL" frontend/.env.example  → must return 1 result with port 5187
[ ] ISSUE-04: grep -n "VITE_CHATBOT_URL" frontend/.env.example  → must return 0 results
[ ] ISSUE-06: grep -c "<<<<<<" .gitignore  → must return 0
[ ] ISSUE-11: grep -n "technopath-chatbot" render.yaml  → must return 1 result
[ ] ISSUE-11: grep -n "FLASK_DEBUG" render.yaml  → must return 1 result

BACKEND
[ ] ISSUE-07: grep -n "min_value=1" backend_django/apps/feedback/serializers.py  → must return 1 result
[ ] ISSUE-07: grep -n "__all__" backend_django/apps/feedback/serializers.py  → must return 0 results
[ ] ISSUE-08: grep -n "'count'" backend_django/apps/users/views.py  → must return 1+ result in AuditLogView
[ ] ISSUE-09: grep -n "VITE_API_BASE_URL" frontend/src/services/api.js  → must return 1+ result in refresh call
[ ] ISSUE-13: grep -n "WhiteNoiseMiddleware" backend_django/technopath/settings.py  → must return 1 result
[ ] ISSUE-13: grep -n "STATICFILES_STORAGE" backend_django/technopath/settings.py  → must return 1 result
[ ] ISSUE-14: grep -n "1000/minute" backend_django/technopath/settings.py  → must return 0 results
[ ] ISSUE-15: grep -n "RuntimeError" backend_django/technopath/settings.py  → must return 1 result

FRONTEND
[ ] ISSUE-17: grep -n "skipWaiting" frontend/vite.config.js  → must return 0 results
[ ] ISSUE-18: grep -n "pathMatch" frontend/src/router/index.js  → must return 1 result
[ ] ISSUE-19: grep -n "tp_splash_seen" frontend/src/router/index.js  → must return 1 result

CHATBOT
[ ] ISSUE-20: grep -n "history: list" chatbot_flask/app.py  → must return 1 result
[ ] ISSUE-20: grep -n 'data.get("history"' chatbot_flask/app.py  → must return 1 result
```

---

## FINAL REPORT FORMAT

Print this block when all checks are complete:

```
╔══════════════════════════════════════════════════════════╗
║         TECHNOPATHY FIX & VERIFICATION REPORT           ║
╠══════════════════════════════════════════════════════════╣
║  ISSUE-01  SQL Injection Fixed            ✅ / ❌       ║
║  ISSUE-02  Rate Limiter Re-Enabled        ✅ / ❌       ║
║  ISSUE-03  JWT Moved to sessionStorage    ✅ / ❌       ║
║  ISSUE-04  Env Var Name Fixed             ✅ / ❌       ║
║  ISSUE-05  Flask Debug Guard Added        ✅ / ❌       ║
║  ISSUE-06  .gitignore Conflict Resolved   ✅ / ❌       ║
║  ISSUE-07  Feedback Rating Validated      ✅ / ❌       ║
║  ISSUE-08  Audit Log Paginated            ✅ / ❌       ║
║  ISSUE-09  Token Refresh URL Fixed        ✅ / ❌       ║
║  ISSUE-10  Broken Scopes Documented       ✅ / ❌       ║
║  ISSUE-11  Flask Added to render.yaml     ✅ / ❌       ║
║  ISSUE-12  DEBUG Default Fixed            ✅ / ❌       ║
║  ISSUE-13  WhiteNoise Configured          ✅ / ❌       ║
║  ISSUE-14  Throttle Rates Tightened       ✅ / ❌       ║
║  ISSUE-15  DB Guard Added                 ✅ / ❌       ║
║  ISSUE-16  .env.example Sanitized         ✅ / ❌       ║
║  ISSUE-17  PWA skipWaiting Removed        ✅ / ❌       ║
║  ISSUE-18  404 Route Added                ✅ / ❌       ║
║  ISSUE-19  Splash Session Guard Added     ✅ / ❌       ║
║  ISSUE-20  Chatbot History Context Fixed  ✅ / ❌       ║
╠══════════════════════════════════════════════════════════╣
║  TOTAL:  ___ / 20 PASSED                                ║
║  STATUS: [ ALL CLEAR ✅ ] or [ NEEDS RETRY ❌ ]         ║
╚══════════════════════════════════════════════════════════╝
```

**If any item shows ❌ — do NOT stop. Return to that issue's section, re-apply the fix, re-run its verification command, and update the report. Repeat until all 20 show ✅.**
