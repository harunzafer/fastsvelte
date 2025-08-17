<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { DASHBOARD_PATH } from '$lib/config/constants';
	import { ensureAuthenticated } from '$lib/auth/session';
	import { authStore } from '$lib/auth/auth.svelte';

	let { children } = $props();

	onMount(async () => {
		// First ensure user is authenticated
		await ensureAuthenticated('admin onMount');

		// Then check role access (assuming 'admin' role name)
		if (authStore.user?.role?.name !== 'admin') {
			console.log('admin access denied');
			goto(DASHBOARD_PATH);
		}
	});
</script>

{#if authStore.isLoading}
	<div class="flex h-screen items-center justify-center">
		<div class="loading loading-spinner loading-lg"></div>
	</div>
{:else if authStore.isAuthenticated && authStore.user?.role?.name === 'admin'}
	{@render children()}
{:else}
	<div class="flex h-screen items-center justify-center">
		<p>Redirecting...</p>
	</div>
{/if}
