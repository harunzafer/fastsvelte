<script lang="ts">
	import { authStore } from '$lib/auth/auth.svelte';
	import { logout } from '$lib/auth/session';

	const handleLogout = async () => {
		try {
			await logout();
			// authStore.clear() is already handled in the logout function
		} catch (error) {
			console.error('Logout failed:', error);
		}
	};

	console.log(JSON.stringify(authStore, null, 2));

	// Using Svelte 5 runes - no $ prefix needed for reactive access
	const user = $derived(authStore.user);
	const isLoading = $derived(authStore.isLoading);
</script>

{#if isLoading}
	<!-- Loading state -->
	<div class="btn btn-ghost max-sm:btn-square gap-2 px-1.5">
		<div class="avatar">
			<div class="bg-base-200 mask mask-squircle w-8">
				<div class="skeleton h-full w-full"></div>
			</div>
		</div>
	</div>
{:else if user}
	<!-- Profile dropdown -->
	<div class="dropdown dropdown-bottom dropdown-end">
		<div tabindex="0" role="button" class="btn btn-ghost max-sm:btn-square gap-2 px-1.5">
			<div class="avatar">
				<div class="bg-base-200 mask mask-squircle w-8">
					{#if user.avatar_url}
						<img src={user.avatar_url} alt="Avatar" />
					{:else}
						<div
							class="bg-primary text-primary-content flex size-full items-center justify-center text-xs font-bold"
						>
							{(user.first_name?.[0] || '') + (user.last_name?.[0] || '')}
						</div>
					{/if}
				</div>
			</div>
			<div class="text-start max-sm:hidden">
				<p class="text-sm/none">{user.first_name || 'User'}</p>
				<p class="text-base-content/50 mt-0.5 text-xs/none">{user.role?.name || 'Member'}</p>
			</div>
			<span class="iconify lucide--chevron-down text-base-content/60 size-4 max-sm:hidden"></span>
		</div>
		<ul
			role="menu"
			tabindex="0"
			class="dropdown-content menu bg-base-100 rounded-box shadow-base-content/4 mt-1 w-64 p-2 shadow-[0px_10px_40px_0px]"
		>
			<li class="menu-title">
				<div class="flex flex-col">
					<span>Account</span>
					<span class="text-base-content/60 text-xs font-normal">{user.email}</span>
				</div>
			</li>
			<li>
				<a href="/profile">
					<span class="iconify lucide--user size-4.5" />
					<span>Profile</span>
				</a>
			</li>
			<li>
				<a href="/settings/user">
					<span class="iconify lucide--settings size-4.5" />
					<span>User Preferences</span>
				</a>
			</li>
			<li>
				<a href="/billing">
					<span class="iconify lucide--credit-card size-4.5" />
					<span>Billing</span>
				</a>
			</li>
			<div class="divider my-1"></div>
			<li>
				<button class="text-error hover:bg-error/10" onclick={handleLogout}>
					<span class="iconify lucide--log-out size-4.5" />
					<span>Sign Out</span>
				</button>
			</li>
		</ul>
	</div>
{:else}
	<!-- Not authenticated state -->
	<a href="/login" class="btn btn-primary">Sign In</a>
{/if}
