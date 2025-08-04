# FastSvelte Frontend Auth Flow (SPA Mode)

FastSvelte uses secure, session-based authentication with HTTP-only cookies. This guide explains how session management works on the frontend. No tokens are used — authentication is verified via the `/me` endpoint.

## 1. Session Check (`checkAuthStatus`)

On every page load or navigation, we run `checkAuthStatus()` to validate the session via `/api/user/me`. If valid, the user is stored in `authStore`; otherwise, the session is cleared.

## 2. 401 Handler in `api.ts`

All API requests use a shared `apiFetch()` wrapper. If a request returns `401 Unauthorized`, we assume the session is invalid and redirect to `/login`.

## 3. Cross-tab Debounce with `localStorage`

To prevent redundant `/me` calls (especially when opening multiple tabs), we:
- Store the last check timestamp in `localStorage`
- Skip the check if it ran within the last 10 seconds

## 4. Random Backoff (0–100ms)

To avoid simultaneous `/me` requests when many tabs are opened at once, we introduce a short random delay before calling the API. This prevents server bursts without affecting perceived speed.

## 5. UI Gating with `authStore.isLoading`

While the session check is in progress, we show a loading indicator. This prevents rendering protected content before the session is verified, avoiding race conditions and UI flash.

