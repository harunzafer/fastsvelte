import type { ClientInit } from '@sveltejs/kit';


import axios from 'axios';
// import { auth, checkAuth } from '$lib/stores/auth.svelte';
// import { appContext } from '$lib/stores/clients.svelte';

export const init: ClientInit = async () => {
	// axios.defaults.baseURL = PUBLIC_API_BASE_URL;
	// axios.defaults.withCredentials = true;

	// try {
	// 	const auth = await checkAuth({ redirectToLogin: true, caller: 'hooks.client.ts' });
	// 	if (auth) {
	// 		await appContext.refresh();
	// 	}
	// } catch (err) {
	// 	console.error(err);
	// }
	
};
