<script lang="ts">
	import { authStore } from '$lib/store/auth.svelte';
	import { logout } from '$lib/util/session';

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
	<!-- Your existing theme component with dynamic data -->
	<div class="drawer drawer-end">
		<input id="topbar-profile-drawer" type="checkbox" class="drawer-toggle" />
		<div class="drawer-content">
			<label for="topbar-profile-drawer" class="btn btn-ghost max-sm:btn-square gap-2 px-1.5">
				<div class="avatar">
					<div class="bg-base-200 mask mask-squircle w-8">
						<img src="/images/avatars/1.png" alt="Avatar" />
					</div>
				</div>
				<div class="text-start max-sm:hidden">
					<p class="text-sm/none">{user.first_name || 'User'}</p>
					<p class="text-base-content/50 mt-0.5 text-xs/none">{user.role?.name || 'Member'}</p>
				</div>
			</label>
		</div>
		<div class="drawer-side">
			<label for="topbar-profile-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
			<div class="h-full w-72 p-2 sm:w-84">
				<div class="bg-base-100 rounded-box relative flex h-full flex-col pt-4 sm:pt-8">
					<label
						for="topbar-profile-drawer"
						class="btn btn-xs btn-circle btn-ghost absolute start-2 top-2"
						aria-label="Close"
					>
						<span class="iconify lucide--x size-4" />
					</label>

					<div class="flex flex-col items-center">
						<div class="relative">
							<div
								class="avatar bg-base-200 isolate size-20 cursor-pointer overflow-hidden rounded-full px-1 pt-1 md:size-24"
							>
								<img src="/images/avatars/1.png" alt="User Avatar" />
							</div>
							<div
								class="bg-base-100 absolute end-0 bottom-0 flex items-center justify-center rounded-full p-1.5 shadow-sm"
							>
								<span class="iconify lucide--pencil size-4" />
							</div>
						</div>

						<p class="mt-4 text-lg/none font-medium sm:mt-8">
							{user.first_name}
							{user.last_name}
						</p>
						<p class="text-base-content/60 mt-1 text-sm">{user.email}</p>

						<!-- Team avatars section - you might want to fetch team members -->
						<div class="mt-4 flex items-center gap-2 *:cursor-pointer sm:mt-6">
							<div class="avatar bg-base-200 size-10 overflow-hidden rounded-full px-1 pt-1">
								<img src="/images/avatars/2.png" alt="Team member" />
							</div>
							<div class="avatar bg-base-200 size-10 overflow-hidden rounded-full px-1 pt-1">
								<img src="/images/avatars/3.png" alt="Team member" />
							</div>
							<div class="avatar bg-base-200 size-10 overflow-hidden rounded-full px-1 pt-1">
								<img src="/images/avatars/4.png" alt="Team member" />
							</div>
							<div
								class="bg-base-200 border-base-300 flex size-10 items-center justify-center rounded-full border border-dashed"
							>
								<span class="iconify lucide--plus size-4.5" />
							</div>
						</div>
					</div>

					<div class="border-base-300 mt-4 grow overflow-auto border-t border-dashed px-2 sm:mt-6">
						<ul class="menu w-full p-2">
							<li class="menu-title">Account</li>
							<li>
								<a href="/profile">
									<span class="iconify lucide--user size-4.5" />
									<span>View Profile</span>
								</a>
							</li>
							<li>
								<a href="/team">
									<span class="iconify lucide--users size-4.5" />
									<span>Team</span>
								</a>
							</li>
							<li>
								<a href="/invites">
									<span class="iconify lucide--mail-plus size-4.5" />
									<span>Invites</span>
									<div class="badge badge-sm">4</div>
								</a>
							</li>

							<li class="menu-title">Platform</li>
							<li>
								<a href="/settings">
									<span class="iconify lucide--settings size-4.5" />
									<span>Settings</span>
								</a>
							</li>
							<li>
								<a href="/billing">
									<span class="iconify lucide--credit-card size-4.5" />
									<span>Billing</span>
								</a>
							</li>
							<li>
								<a href="/support">
									<span class="iconify lucide--help-circle size-4.5" />
									<span>Support</span>
								</a>
							</li>

							<li>
								<button class="text-error hover:bg-error/10" onclick={handleLogout}>
									<span class="iconify lucide--log-out size-4.5" />
									<span>Sign Out</span>
								</button>
							</li>
						</ul>
					</div>

					<div
						class="rounded-box from-primary to-secondary text-primary-content m-4 mt-auto flex cursor-pointer flex-col items-center justify-center bg-linear-to-br p-4 text-center transition-all hover:opacity-95 sm:p-6"
					>
						<div
							class="bg-primary-content/10 border-primary-content/10 flex items-center justify-center rounded-full border p-1.5 sm:p-2.5"
						>
							<span class="iconify lucide--zap size-5 sm:size-6" />
						</div>
						<p
							class="mt-2 font-mono text-[11px] font-medium tracking-wider uppercase opacity-70 sm:mt-4"
						>
							Upgrade your plan
						</p>
						<p class="mt-1 leading-none font-medium sm:text-lg">
							Save <span class="font-semibold underline">30%</span> today
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
{:else}
	<!-- Not authenticated state -->
	<a href="/login" class="btn btn-primary">Sign In</a>
{/if}
