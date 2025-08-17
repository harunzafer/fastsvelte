<script lang="ts">
	import Footer from '$lib/components/admin-layout/Footer.svelte';
	import Rightbar from '$lib/components/admin-layout/Rightbar.svelte';
	import Sidebar from '$lib/components/admin-layout/Sidebar.svelte';
	import Topbar from '$lib/components/admin-layout/Topbar.svelte';
	import { onMount } from 'svelte';
	import { adminMenuItems } from './menu';
	import { ensureAuthenticated } from '$lib/auth/session';
	import { authStore } from '$lib/auth/auth.svelte';

	let { children } = $props();

	onMount(async () => {
		await ensureAuthenticated('onMount');
	});
</script>

{#if authStore.isLoading}
	<!-- Loading state - prevents flash -->
	<div class="flex h-screen items-center justify-center">
		<div class="loading loading-spinner loading-lg"></div>
	</div>
{:else if authStore.isAuthenticated}
	<!-- Authenticated content -->
	<div class="size-full">
		<div class="flex">
			<Sidebar menuItems={adminMenuItems} />
			<div class="flex h-screen min-w-0 grow flex-col overflow-auto">
				<Topbar />
				<div id="layout-content">{@render children()}</div>
				<Footer />
			</div>
		</div>
		<Rightbar />
	</div>
{:else}
	<!-- Not authenticated - this shouldn't show since redirect happens -->
	<div class="flex h-screen items-center justify-center">
		<p>Redirecting to login...</p>
	</div>
{/if}
