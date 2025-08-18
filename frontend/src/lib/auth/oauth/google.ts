import { getGoogleAuthUrl } from '$lib/api/gen/authentication';

/**
 * OAuth error code to user-friendly message mapping
 */
const OAUTH_ERROR_MESSAGES: Record<string, string> = {
  oauth_cancelled: 'Google login was cancelled. Please try again if you want to sign in.',
  oauth_invalid_request: 'Invalid OAuth request. Please try again.',
  oauth_unauthorized: 'OAuth client not authorized. Please contact support.',
  oauth_unsupported: 'OAuth response type not supported. Please contact support.',
  oauth_invalid_scope: 'Invalid OAuth scope requested. Please contact support.',
  oauth_server_error: 'Google server error. Please try again later.',
  oauth_unavailable: 'Google OAuth temporarily unavailable. Please try again later.',
  oauth_missing_code: 'OAuth authorization failed. Please try again.',
  oauth_invalid_state: 'Invalid OAuth state. Please try again.',
  oauth_error: 'OAuth login failed. Please try again.',
  oauth_failed: 'Google login failed. Please try again.'
};

/**
 * Get user-friendly error message from OAuth error code
 * 
 * @param errorCode - OAuth error code from URL parameter
 * @returns User-friendly error message
 */
export function getOAuthErrorMessage(errorCode: string): string {
  return OAUTH_ERROR_MESSAGES[errorCode] || 'An error occurred during Google login. Please try again.';
}

/**
 * Check URL parameters for OAuth errors and return error message if found
 * 
 * @param searchParams - URLSearchParams from page URL
 * @returns Error message string or null if no error
 */
export function checkOAuthError(searchParams: URLSearchParams): string | null {
  const error = searchParams.get('error');
  return error ? getOAuthErrorMessage(error) : null;
}

/**
 * Initiates Google OAuth flow for both login and signup
 * 
 * @param onError - Callback to handle errors (typically sets apiError state)
 * @param onLoading - Callback to handle loading state (typically sets loading state)
 * @returns Promise that resolves when OAuth initiation succeeds or throws on error
 */
export async function initiateGoogleOAuth(
  onError: (error: string) => void,
  onLoading: (loading: boolean) => void
): Promise<void> {
  try {
    onLoading(true);
    onError(''); // Clear any previous errors
    
    // Get Google authorization URL from backend
    const response = await getGoogleAuthUrl();
    
    // Redirect to Google OAuth - backend will handle callback and redirect back to dashboard
    window.location.href = response.data.authorization_url;
  } catch (err: any) {
    console.error('Google OAuth initiation failed:', err);
    onError('Failed to initiate Google login. Please try again.');
    onLoading(false);
  }
}

/**
 * Convenience wrapper for component usage with reactive state
 * 
 * @param apiError - Svelte reactive state for error messages
 * @param loading - Svelte reactive state for loading state
 */
export function createGoogleOAuthHandler(
  apiError: { value: string },
  loading: { value: boolean }
) {
  return () => initiateGoogleOAuth(
    (error) => apiError.value = error,
    (isLoading) => loading.value = isLoading
  );
}