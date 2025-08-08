// frontend/src/lib/util/session.ts
import { goto } from '$app/navigation';
import { logout as logoutUser } from '$lib/api/gen/authentication';
import { getCurrentUser } from '$lib/api/gen/users';
import { LOGIN_PATH } from '$lib/config/constants';
import { AUTH_CHECK_EXPIRES_MS } from '$lib/config/settings';
import { authStore } from '$lib/store/auth.svelte';

// Track when we last successfully verified authentication to avoid excessive API calls
let lastSuccessfulCheck = 0;

// Prevent multiple concurrent authentication checks
let isChecking = false;

// BroadcastChannel for cross-tab authentication synchronization
// Ensures logout in one tab affects all other open tabs
const authChannel = new BroadcastChannel('fastsvelte-auth');

authChannel.addEventListener('message', (event) => {
	if (event.data.type === 'logout') {
		// Clear auth state when logout happens in another tab
		authStore.clear();
		lastSuccessfulCheck = 0; // Reset timestamp to force re-auth
		goto(LOGIN_PATH);
	}
});

/**
 * Verifies current user authentication by calling the /users/me endpoint
 * @returns Promise<boolean> - true if authenticated, false otherwise
 */
export async function validateCurrentUser(): Promise<boolean> {
	try {
		authStore.setLoading(true);
		const response = await getCurrentUser();
		authStore.setUser(response.data);
		return true;
	} catch (error) {
		// Clear auth state on any authentication failure
		authStore.clear();

		// Redirect to login if not already there (avoid redirect loops)
		if (!window.location.pathname.startsWith(LOGIN_PATH)) {
			window.location.href = LOGIN_PATH;
		}

		return false;
	}
}

/**
 * Rate-limited authentication check to prevent excessive API calls
 * Only checks authentication if:
 * - No check is currently in progress AND
 * - User is not authenticated OR last successful check was > 20 seconds ago
 *
 * @param caller - Optional string identifier for debugging purposes
 * @returns Promise<boolean> - true if authenticated, false otherwise
 */
export async function ensureAuthenticated(caller?: string): Promise<boolean> {
	if (caller) {
		console.log('ensureAuthenticated called by:', caller);
	}

	// Prevent concurrent authentication requests
	if (isChecking) {
		if (caller) {
			console.log(`${caller}: Auth check already in progress, returning current state`);
		}
		return authStore.isAuthenticated;
	}

	const now = Date.now();

	// Skip check if user is authenticated and we verified recently
	// This prevents excessive API calls while maintaining reasonable security
	if (authStore.isAuthenticated && now - lastSuccessfulCheck < AUTH_CHECK_EXPIRES_MS) {
		if (caller) {
			console.log(`${caller}: Recent successful auth, skipping check`);
		}
		return true;
	}

	if (caller) {
		console.log(`${caller}: Performing auth validation`);
	}

	isChecking = true;

	// Set loading state when starting auth check
	if (!authStore.isAuthenticated) {
		authStore.setLoading(true);
	}

	try {
		const success = await validateCurrentUser();
		if (success) {
			// Only update timestamp on successful authentication
			lastSuccessfulCheck = now;
			if (caller) {
				console.log(`${caller}: Auth validation successful`);
			}
		} else if (caller) {
			console.log(`${caller}: Auth validation failed`);
		}
		// Failed auth attempts don't update lastSuccessfulCheck
		// This ensures we keep trying until authentication succeeds
		return success;
	} finally {
		// Always reset the checking flag to allow future calls
		isChecking = false;
	}
}

/**
 * Logs out the current user and handles cleanup
 * - Calls backend logout endpoint
 * - Clears local auth state
 * - Notifies other tabs via BroadcastChannel
 * - Redirects to login page
 */
export async function logout(): Promise<void> {
	try {
		await logoutUser();
	} catch (error) {
		console.error('Logout failed:', error);
	} finally {
		// Clean up auth state regardless of logout API success/failure
		authStore.clear();
		lastSuccessfulCheck = 0; // Reset timestamp to force re-auth on next check

		// Notify other tabs about logout
		authChannel.postMessage({ type: 'logout' });

		// Navigate to login page
		goto(LOGIN_PATH);
	}
}
