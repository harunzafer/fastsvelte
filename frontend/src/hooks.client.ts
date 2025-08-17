import type { ClientInit } from '@sveltejs/kit';
import { ensureAuthenticated } from '$lib/auth/session';

export const init: ClientInit = async () => {
	// Check authentication immediately on SPA startup
	try {
		await ensureAuthenticated('ClientInit');
	} catch (err) {
		console.error(err);
	}
};
