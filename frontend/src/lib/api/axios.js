// src/lib/api/axios.js

/**
 * IMPORTANT: This file must remain as .js (not .ts) for Orval compatibility.
 *
 * Orval requires a mutator file that it can import from its CommonJS context.
 * When using TypeScript files, Orval cannot properly resolve the exported
 * axiosInstance function, resulting in the error:
 * "Your mutator file doesn't have the axiosInstance exported function"
 *
 * Related issue: https://github.com/orval-labs/orval/issues/886
 *
 * This JavaScript file serves as the mutator for Orval code generation,
 * while the rest of our codebase can use TypeScript and the generated
 * API functions normally.
 *
 * NOTE: We use window.location.href instead of SvelteKit's goto() because:
 * 1. This file is used by Orval-generated code across the app
 * 2. goto() requires SvelteKit's app context and may not be available
 *    in all contexts where axios interceptors run
 * 3. window.location.href works universally in any browser context
 * 4. For auth failures, a hard redirect (page reload) is often preferable
 *    to ensure complete state reset
 */

import Axios from 'axios';
import { PUBLIC_API_BASE_URL } from '$env/static/public';
import { browser } from '$app/environment';
import { LOGIN_PATH } from '$lib/config/constants';
import { authStore } from '$lib/auth/auth.svelte';

export const axiosInstance = Axios.create({
	baseURL: PUBLIC_API_BASE_URL,
	withCredentials: true
});

// Response interceptor to handle authentication errors globally
axiosInstance.interceptors.response.use(
	// Pass through successful responses
	(response) => response,

	// Handle error responses
	(error) => {
		// Handle 401 Unauthorized responses
		if (error.response?.status === 401 && browser) {
			const url = error.config?.url || '';

			// Exclude auth-related endpoints - they handle their own 401s
			const isAuthEndpoint = url.includes('/users/me') || url.includes('/auth/login');

			if (!isAuthEndpoint) {
				console.log('API returned 401, clearing auth and redirecting to login');

				// Clear auth state immediately
				authStore.clear();

				// Only redirect if not already on login page
				if (!window.location.pathname.startsWith(LOGIN_PATH)) {
					// Use window.location for immediate redirect
					window.location.href = LOGIN_PATH;
				}
			}
		}

		// Re-throw the error so components can still handle it if needed
		return Promise.reject(error);
	}
);
