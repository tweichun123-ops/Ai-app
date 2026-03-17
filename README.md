# Ai-app

Demo backend for AI companion flows (authentication, onboarding, chat, closet, and call).

## Security hardening added

- `/api/users/*` endpoints now require `Authorization: Bearer <access_token>`.
- Access token user scope is enforced: token user must match `{user_id}` in URL.
- SMS verification code is randomized per request (6 digits), and no longer returned via API payload.
- Verification code requests are rate-limited per phone (`60s` retry window).

## Local run

```bash
cd backend
python demo_server.py
```

Server starts at `http://0.0.0.0:8000`.
