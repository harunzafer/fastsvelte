<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/store/auth.svelte';
	import { ensureAuthenticated } from '$lib/util/session';
	import { DASHBOARD_PATH } from '$lib/config/constants';

	let { children } = $props();

	onMount(async () => {
		// First ensure user is authenticated
		await ensureAuthenticated('org onMount');

		// Then check role access
		if (authStore.user?.role?.name !== 'org_admin') {
			console.log('org admin access denied');
			goto(DASHBOARD_PATH);
		}
	});
</script>

{#if authStore.isLoading}
	<div class="flex h-screen items-center justify-center">
		<div class="loading loading-spinner loading-lg"></div>
	</div>
{:else if authStore.isAuthenticated && authStore.user?.role?.name === 'org_admin'}
	{@render children()}
{:else}
	<div class="flex h-screen items-center justify-center">
		<p>Redirecting...</p>
	</div>
{/if}
