<script lang="ts">
	import { onMount } from 'svelte';
	import { activateUser, listUsers, suspendUser } from '$lib/api/gen/users';
	import type { SystemAdminUserResponse } from '$lib/api/gen/model/systemAdminUserResponse';

	let users = $state<SystemAdminUserResponse[]>([]);
	let loading = $state(true);
	let error = $state('');
	let processingUsers = $state(new Set<number>());

	onMount(async () => {
		await loadUsers();
	});

	async function loadUsers() {
		try {
			loading = true;
			error = '';
			const response = await listUsers();
			users = response.data;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load users';
			if (err.response?.status === 403) {
				error = 'Access denied: System administrator privileges required';
			}
		} finally {
			loading = false;
		}
	}

	async function handleSuspendUser(userId: number) {
		if (!confirm('Are you sure you want to suspend this user?')) return;

		try {
			processingUsers.add(userId);
			processingUsers = new Set(processingUsers);

			await suspendUser(userId);
			await loadUsers();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to suspend user';
		} finally {
			processingUsers.delete(userId);
			processingUsers = new Set(processingUsers);
		}
	}

	async function handleActivateUser(userId: number) {
		try {
			processingUsers.add(userId);
			processingUsers = new Set(processingUsers);

			await activateUser(userId);
			await loadUsers();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to activate user';
		} finally {
			processingUsers.delete(userId);
			processingUsers = new Set(processingUsers);
		}
	}
</script>

<div class="container mx-auto p-6">
	<div class="mb-6 flex items-center justify-between">
		<h1 class="text-3xl font-bold">System Users</h1>
		<button class="btn btn-outline btn-sm" onclick={() => loadUsers()}>
			<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
				/>
			</svg>
			Refresh
		</button>
	</div>

	{#if error}
		<div class="alert alert-error mb-6">
			<svg class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
				/>
			</svg>
			<span>{error}</span>
		</div>
	{/if}

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<span class="loading loading-spinner loading-lg"></span>
		</div>
	{:else}
		<div class="card bg-base-100 shadow-xl">
			<div class="card-body">
				<div class="overflow-x-auto">
					<table class="table">
						<thead>
							<tr>
								<th>ID</th>
								<th>Name</th>
								<th>Email</th>
								<th>Status</th>
								<th class="text-right">Actions</th>
							</tr>
						</thead>
						<tbody>
							{#each users as user (user.id)}
								<tr>
									<td class="font-mono text-sm">{user.id}</td>
									<td>
										<div class="font-semibold">
											{user.first_name || 'No'}
											{user.last_name || 'Name'}
										</div>
									</td>
									<td class="text-sm">{user.email}</td>
									<td>
										{#if user.is_active}
											<div class="badge badge-success">Active</div>
										{:else}
											<div class="badge badge-error">Suspended</div>
										{/if}
									</td>
									<td class="text-right">
										<div class="flex justify-end gap-2">
											{#if processingUsers.has(user.id)}
												<span class="loading loading-spinner loading-xs"></span>
											{:else if user.is_active}
												<button
													class="btn btn-error btn-xs"
													onclick={() => handleSuspendUser(user.id)}
												>
													Suspend
												</button>
											{:else}
												<button
													class="btn btn-success btn-xs"
													onclick={() => handleActivateUser(user.id)}
												>
													Activate
												</button>
											{/if}
										</div>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>

					{#if users.length === 0 && !loading}
						<div class="text-base-content/60 py-8 text-center">No users found</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
