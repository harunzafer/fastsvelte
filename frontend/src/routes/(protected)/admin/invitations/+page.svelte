<script lang="ts">
	import { onMount } from 'svelte';
	import { z } from 'zod';
	import { useFormValidation } from '$lib/util/useFormValidation.svelte';
	import {
		createInvitation,
		getPendingInvitations,
		revokeInvitation
	} from '$lib/api/gen/invitations';
	import { authStore } from '$lib/auth/auth.svelte';
	import type { InvitationResponse } from '$lib/api/gen/model/invitationResponse';

	let pendingInvitations = $state<InvitationResponse[]>([]);
	let loading = $state(false);
	let formLoading = $state(false);
	let apiError = $state('');
	let successMessage = $state('');

	const schema = z.object({
		email: z.email('Invalid email address'),
		role: z.string().min(1, 'Please select a role')
	});

	const { formData, errors, handleChange, handleSubmit, handleClear } = useFormValidation({
		schema,
		initialValues: {
			email: '',
			role: 'member' as const
		}
	});

	const loadPendingInvitations = async () => {
		loading = true;
		try {
			const response = await getPendingInvitations();
			pendingInvitations = response.data;
		} catch (err: any) {
			console.error('Failed to load invitations:', err);
			apiError = 'Failed to load pending invitations';
		} finally {
			loading = false;
		}
	};

	const submitInvitation = async (e: Event) => {
		handleSubmit(e, async (data) => {
			formLoading = true;
			apiError = '';
			successMessage = '';
			try {
				await createInvitation({
					email: data.email.toLowerCase().trim(),
					role: data.role
				});

				successMessage = `Invitation sent to ${data.email}`;
				handleClear();
				await loadPendingInvitations(); // Refresh the list
			} catch (err: any) {
				if (err?.response?.status === 400) {
					apiError = 'Invalid invitation data. Please check your inputs.';
				} else if (err?.response?.status === 409) {
					// Handle EmailAlreadyExists exception
					const details = err?.response?.data?.details;
					if (details?.same_organization) {
						apiError = 'This user is already a member of this organization.';
					} else {
						apiError = 'This user already exists in another organization.';
					}
				} else {
					apiError = 'Failed to send invitation. Please try again.';
				}
			} finally {
				formLoading = false;
			}
		});
	};

	const getRoleDisplayName = (role: string) => {
		switch (role) {
			case 'sys_admin':
				return 'Sys Admin';
			case 'org_admin':
				return 'Admin';
			case 'member':
				return 'Member';
			case 'readonly':
				return 'Read Only';
			default:
				return role;
		}
	};

	const formatDate = (dateString: string) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	};

	const handleRevokeInvitation = async (invitationId: number) => {
		if (!confirm('Are you sure you want to cancel this invitation?')) {
			return;
		}

		// Clear previous messages
		apiError = '';
		successMessage = '';

		try {
			const response = await revokeInvitation(invitationId);
			console.log('Revoke response:', response);

			// Refresh the list immediately
			await loadPendingInvitations();

			successMessage = 'Invitation cancelled successfully';
		} catch (err: any) {
			console.error('Failed to revoke invitation:', err);
			console.error('Error details:', err?.response);
			apiError = 'Failed to cancel invitation';
		}
	};

	const getAvailableRoles = () => {
		// System admins can invite org admins, org admins can invite members/readonly
		if (authStore.user?.role?.name === 'sys_admin') {
			return [
				{ value: 'org_admin', label: 'Organization Admin' },
				{ value: 'member', label: 'Member' },
				{ value: 'readonly', label: 'Read Only' }
			];
		} else {
			return [
				{ value: 'member', label: 'Member' },
				{ value: 'readonly', label: 'Read Only' }
			];
		}
	};

	onMount(() => {
		loadPendingInvitations();
	});
</script>

<div class="p-6">
	<h1 class="mb-6 text-2xl font-semibold">Team Invitations</h1>

	<!-- Send Invitation Card -->
	<div class="card bg-base-100 border-base-200 mb-6 border shadow-sm">
		<div class="card-body">
			<h2 class="card-title mb-4 text-lg">
				<span class="iconify lucide--user-plus text-primary"></span>
				Send Invitation
			</h2>

			<form onsubmit={submitInvitation} class="space-y-4">
				<div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
					<!-- Form Elements Container -->
					<div class="flex flex-col gap-4 md:flex-row md:items-end md:gap-6">
						<!-- Email Field -->
						<div class="form-control">
							<label for="email" class="label">
								<span class="label-text">Email Address</span>
							</label>
							<div class="input input-bordered flex items-center gap-3 md:w-80">
								<span class="iconify lucide--mail text-base-content/60"></span>
								<input
									id="email"
									type="email"
									name="email"
									placeholder="user@example.com"
									class="grow"
									bind:value={formData.email}
									oninput={handleChange}
									data-error={errors.email ? true : undefined}
								/>
							</div>
							{#if errors.email}
								<div class="label">
									<span class="label-text-alt text-error">{errors.email}</span>
								</div>
							{/if}
						</div>

						<!-- Role Field -->
						<div class="form-control flex flex-col">
							<label for="role" class="label">
								<span class="label-text">Role</span>
							</label>
							<select
								id="role"
								name="role"
								class="select select-bordered w-full md:w-48"
								bind:value={formData.role}
								onchange={handleChange}
								data-error={errors.role ? true : undefined}
							>
								{#each getAvailableRoles() as roleOption}
									<option value={roleOption.value}>{roleOption.label}</option>
								{/each}
							</select>
							{#if errors.role}
								<div class="label">
									<span class="label-text-alt text-error">{errors.role}</span>
								</div>
							{/if}
						</div>
					</div>

					<!-- Submit Button Container -->
					<div class="lg:pb-1">
						<button
							type="submit"
							class="btn btn-primary w-full gap-2 lg:w-auto"
							disabled={formLoading}
						>
							{#if formLoading}
								<span class="loading loading-spinner loading-sm"></span>
							{:else}
								<span class="iconify lucide--send"></span>
							{/if}
							Send Invitation
						</button>
					</div>
				</div>

				{#if successMessage || apiError}
					<div class="flex justify-center">
						{#if successMessage}
							<div class="text-success flex items-center gap-2 text-sm">
								<span class="iconify lucide--check-circle"></span>
								{successMessage}
							</div>
						{/if}
						{#if apiError}
							<div class="text-error flex items-center gap-2 text-sm">
								<span class="iconify lucide--alert-circle"></span>
								{apiError}
							</div>
						{/if}
					</div>
				{/if}
			</form>
		</div>
	</div>

	<!-- Pending Invitations List -->
	<div class="card bg-base-100 border-base-200 border shadow-sm">
		<div class="card-body">
			<h2 class="card-title mb-4 text-lg">
				<span class="iconify lucide--clock text-warning"></span>
				Pending Invitations
			</h2>

			{#if loading}
				<div class="flex justify-center py-8">
					<span class="loading loading-spinner loading-lg"></span>
				</div>
			{:else if pendingInvitations.length === 0}
				<div class="py-8 text-center">
					<span class="iconify lucide--inbox text-base-content/30 mb-2 block text-4xl"></span>
					<p class="text-base-content/60">No pending invitations</p>
				</div>
			{:else}
				<div class="overflow-x-auto">
					<table class="table-zebra table">
						<thead>
							<tr>
								<th>Email</th>
								<th>Role</th>
								<th>Invited</th>
								<th>Expires</th>
								<th>Status</th>
								<th>Actions</th>
							</tr>
						</thead>
						<tbody>
							{#each pendingInvitations as invitation}
								<tr>
									<td>
										<div class="flex items-center gap-2">
											<span class="iconify lucide--mail text-base-content/60"></span>
											{invitation.email}
										</div>
									</td>
									<td>
										<div class="badge badge-neutral badge-sm">
											{getRoleDisplayName(invitation.role_name)}
										</div>
									</td>
									<td class="text-base-content/70 text-sm">
										{formatDate(invitation.created_at)}
									</td>
									<td class="text-base-content/70 text-sm">
										{formatDate(invitation.expires_at)}
									</td>
									<td>
										{#if invitation.accepted_at}
											<div class="badge badge-success gap-1">
												<span class="iconify lucide--check"></span>
												Accepted
											</div>
										{:else if new Date(invitation.expires_at) < new Date()}
											<div class="badge badge-error gap-1">
												<!-- <span class="iconify lucide--x"></span> -->
												Expired
											</div>
										{:else}
											<div class="badge badge-warning gap-1">
												<span class="iconify lucide--clock"></span>
												Pending
											</div>
										{/if}
									</td>
									<td>
										{#if !invitation.accepted_at && new Date(invitation.expires_at) >= new Date()}
											<button
												type="button"
												class="btn btn-ghost btn-sm text-error hover:bg-error/10"
												onclick={() => handleRevokeInvitation(invitation.id)}
											>
												<span class="iconify lucide--x size-4"></span>
												Cancel
											</button>
										{:else}
											<span class="text-base-content/40">—</span>
										{/if}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		</div>
	</div>
</div>
