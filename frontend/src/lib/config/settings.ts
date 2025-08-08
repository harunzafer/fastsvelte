// frontend/src/lib/config/settings.ts

// Environment-specific configuration.
// Use for configguration that may differ between local, staging, and production.
// Use constants.ts for the configuration that doesn't change between environments.

import { PUBLIC_API_BASE_URL, PUBLIC_AUTH_RECHECK_INTERVAL_MS } from '$env/static/public';

// Or with more robust validation:
export const AUTH_CHECK_EXPIRES_MS = (() => {
	const value = Number(PUBLIC_AUTH_RECHECK_INTERVAL_MS);
	return isNaN(value) ? 300_000 : value; // Fallback to 5 minutes if invalid
})();

export const API_BASE_URL = PUBLIC_API_BASE_URL;
