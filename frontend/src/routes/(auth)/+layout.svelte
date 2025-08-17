<script lang="ts">
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/auth/auth.svelte';
	import { ensureAuthenticated } from '$lib/auth/session';
	import { DASHBOARD_PATH } from '$lib/config/constants';
	import { onMount } from 'svelte';

	let { children } = $props();

	onMount(async () => {
		// Check if user is already authenticated
		try {
			// await ensureAuthenticated('auth layout onMount');

			// If we get here, user is authenticated - redirect to dashboard
			if (authStore.isAuthenticated) {
				console.log('User already authenticated, redirecting to dashboard');
				goto(DASHBOARD_PATH);
			}
		} catch (error) {
			// User is not authenticated, which is what we want for auth pages
			console.log('User not authenticated, showing auth pages');
		}
	});
</script>

<div class="grid grid-cols-12 overflow-auto sm:h-screen">
	<div
		class="relative hidden bg-[#FFE9D1] lg:col-span-7 lg:block xl:col-span-8 2xl:col-span-9 dark:bg-[#14181c]"
	>
		<div class="absolute inset-0 flex items-center justify-center">
			<img src="/images/auth/auth-hero.png" class="object-cover" alt="Authentication hero" />
		</div>
		<div class="animate-bounce-2 absolute right-[20%] bottom-[15%]">
			<div class="card bg-base-100/80 w-64 backdrop-blur-lg">
				<div class="card-body p-5">
					<div class="flex flex-col items-center justify-center">
						<div class="mask mask-squircle overflow-hidden">
							<img
								src="/images/landing/testimonial-avatar-1.jpg"
								class="bg-base-200 size-14"
								alt=""
							/>
						</div>
						<div class="mt-3 flex items-center justify-center gap-0.5">
							<span class="iconify lucide--star size-4 text-orange-600">/</span>
							<span class="iconify lucide--star size-4 text-orange-600">/</span>
							<span class="iconify lucide--star size-4 text-orange-600">/</span>
							<span class="iconify lucide--star size-4 text-orange-600">/</span>
							<span class="iconify lucide--star size-4 text-orange-600">/</span>
						</div>
						<p class="mt-1 text-lg font-medium">Pouya Saadeghi</p>
						<p class="text-base-content/60 text-sm">Creator of daisyUI</p>
					</div>
					<p class="mt-2 text-center text-sm">
						This is the ultimate admin dashboard for any React project
					</p>
				</div>
			</div>
		</div>
	</div>
	<div class="col-span-12 lg:col-span-5 xl:col-span-4 2xl:col-span-3">
		<!-- {@render children()} -->

		{#if authStore.isLoading}
			<!-- Show loading while checking auth status -->
			<div class="flex h-screen items-center justify-center">
				<div class="loading loading-spinner loading-lg"></div>
			</div>
		{:else if !authStore.isAuthenticated}
			<!-- User is not authenticated - show auth pages -->
			{@render children()}
		{:else}
			<!-- User is authenticated but redirect is in progress -->
			<div class="flex h-screen items-center justify-center">
				<p>Redirecting to dashboard...</p>
			</div>
		{/if}
	</div>
</div>
