<script lang="ts">
	import { authStore } from '$lib/auth/auth.svelte';
	import { updateUserInfo, updateUserAvatar } from '$lib/api/gen/users';
	import { updatePassword } from '$lib/api/gen/password-management';
	import { onMount } from 'svelte';

	let isLoading = $state(false);
	let profileForm = $state({
		firstName: '',
		lastName: ''
	});
	let passwordForm = $state({
		newPassword: '',
		confirmPassword: ''
	});
	let profileMessage = $state('');
	let passwordMessage = $state('');
	let avatarMessage = $state('');
	let showPasswordForm = $state(false);
	let avatarFile: File | null = $state(null);

	onMount(() => {
		if (authStore.user) {
			profileForm.firstName = authStore.user.first_name || '';
			profileForm.lastName = authStore.user.last_name || '';
		}
	});

	async function updateProfile(event: Event) {
		event.preventDefault();

		if (!profileForm.firstName.trim() || !profileForm.lastName.trim()) {
			profileMessage = 'Both first name and last name are required';
			return;
		}

		isLoading = true;
		profileMessage = '';

		try {
			await updateUserInfo({
				first_name: profileForm.firstName.trim(),
				last_name: profileForm.lastName.trim()
			});

			// Update auth store
			if (authStore.user) {
				authStore.user.first_name = profileForm.firstName.trim();
				authStore.user.last_name = profileForm.lastName.trim();
			}

			profileMessage = 'Profile updated successfully';
		} catch (error) {
			profileMessage = 'Failed to update profile';
		} finally {
			isLoading = false;
		}
	}

	async function handleUpdatePassword(event: Event) {
		event.preventDefault();

		if (!passwordForm.newPassword || passwordForm.newPassword.length < 8) {
			passwordMessage = 'Password must be at least 8 characters long';
			return;
		}

		if (passwordForm.newPassword !== passwordForm.confirmPassword) {
			passwordMessage = 'Passwords do not match';
			return;
		}

		isLoading = true;
		passwordMessage = '';

		try {
			await updatePassword({
				new_password: passwordForm.newPassword
			});

			passwordForm.newPassword = '';
			passwordForm.confirmPassword = '';
			passwordMessage = 'Password updated successfully';
			showPasswordForm = false;
		} catch (error) {
			passwordMessage = 'Failed to update password';
		} finally {
			isLoading = false;
		}
	}

	function showModal() {
		document.querySelector<HTMLDialogElement>('#avatar-upload-modal')?.showModal();
	}

	function handleAvatarFileChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.files && target.files[0]) {
			const file = target.files[0];

			// Validate file type
			if (!file.type.match(/^image\/(jpeg|jpg|png|webp)$/)) {
				avatarMessage = 'Please select a JPEG, PNG, or WebP image';
				return;
			}

			// Validate file size (2MB)
			if (file.size > 2 * 1024 * 1024) {
				avatarMessage = 'Image must be smaller than 2MB';
				return;
			}

			avatarFile = file;
			avatarMessage = '';
		}
	}

	async function uploadAvatar() {
		if (!avatarFile) {
			avatarMessage = 'Please select an image first';
			return;
		}

		isLoading = true;
		avatarMessage = '';

		try {
			// Convert file to base64 data URL
			const reader = new FileReader();
			reader.onload = async (e) => {
				const avatarData = e.target?.result as string;

				try {
					await updateUserAvatar({
						avatar_data: avatarData
					});

					// Update auth store with new avatar
					if (authStore.user) {
						authStore.user.avatar_url = avatarData;
					}

					avatarMessage = 'Avatar updated successfully';
					avatarFile = null;

					// Close modal
					document.querySelector<HTMLDialogElement>('#avatar-upload-modal')?.close();
				} catch (error) {
					avatarMessage = 'Failed to upload avatar';
				} finally {
					isLoading = false;
				}
			};

			reader.onerror = () => {
				avatarMessage = 'Failed to read file';
				isLoading = false;
			};

			reader.readAsDataURL(avatarFile);
		} catch (error) {
			avatarMessage = 'Failed to upload avatar';
			isLoading = false;
		}
	}
</script>

<div class="container mx-auto max-w-4xl p-6">
	<div class="mb-8">
		<h1 class="text-3xl font-bold">Profile Settings</h1>
		<div class="text-base-content/70 mt-2 flex items-center gap-2">
			{#if authStore.user}
				<span>{authStore.user.first_name} {authStore.user.last_name} • {authStore.user.email}</span>
				<div class="badge badge-outline badge-sm">{authStore.user.role?.name || 'Member'}</div>
			{:else}
				<span>Manage your account information and preferences</span>
			{/if}
		</div>
	</div>

	<div class="grid gap-8 lg:grid-cols-3">
		<!-- Profile Picture Section -->
		<div class="lg:col-span-1">
			<div class="card bg-base-100 shadow-sm">
				<div class="card-body items-center text-center">
					<h2 class="card-title">Profile Picture</h2>

					<button
						type="button"
						class="avatar group relative size-32 cursor-pointer overflow-hidden rounded-full"
						onclick={showModal}
						aria-label="Change profile picture"
					>
						<div class="bg-base-200 p-1">
							{#if authStore.user?.avatar_url}
								<img src={authStore.user.avatar_url} alt="Profile" class="rounded-full" />
							{:else}
								<div
									class="bg-primary text-primary-content flex size-full items-center justify-center rounded-full text-4xl font-bold"
								>
									{(authStore.user?.first_name?.[0] || '') + (authStore.user?.last_name?.[0] || '')}
								</div>
							{/if}
						</div>
						<div
							class="absolute right-0 bottom-0 left-0 bg-black/60 text-center text-sm font-medium text-white opacity-0 backdrop-blur-sm transition-all group-hover:opacity-100"
						>
							Edit
						</div>
					</button>

					<p class="text-base-content/70 text-sm">Click to change your profile picture</p>
				</div>
			</div>
		</div>

		<!-- Profile Information Section -->
		<div class="lg:col-span-2">
			<div class="card bg-base-100 shadow-sm">
				<div class="card-body">
					<h2 class="card-title">Personal Information</h2>

					<form onsubmit={updateProfile} class="space-y-4">
						<div class="grid gap-4 md:grid-cols-2">
							<div class="form-control">
								<label class="label" for="firstName">
									<span class="label-text">First Name</span>
								</label>
								<input
									id="firstName"
									type="text"
									class="input input-bordered"
									bind:value={profileForm.firstName}
									required
								/>
							</div>

							<div class="form-control">
								<label class="label" for="lastName">
									<span class="label-text">Last Name</span>
								</label>
								<input
									id="lastName"
									type="text"
									class="input input-bordered"
									bind:value={profileForm.lastName}
									required
								/>
							</div>
						</div>

						{#if profileMessage}
							<div
								class="alert {profileMessage.includes('successfully')
									? 'alert-success'
									: 'alert-error'}"
							>
								<span>{profileMessage}</span>
							</div>
						{/if}

						<div class="card-actions justify-end">
							<button type="submit" class="btn btn-primary" disabled={isLoading}>
								{#if isLoading}
									<span class="loading loading-spinner loading-sm"></span>
								{/if}
								Update Profile
							</button>
						</div>
					</form>
				</div>
			</div>

			<!-- Password Section -->
			<div class="card bg-base-100 mt-6 shadow-sm">
				<div class="card-body">
					<div class="flex items-center justify-between">
						<h2 class="card-title">Password</h2>
						{#if !showPasswordForm}
							<button class="btn btn-outline btn-sm" onclick={() => (showPasswordForm = true)}>
								Change Password
							</button>
						{/if}
					</div>

					{#if showPasswordForm}
						<form onsubmit={handleUpdatePassword} class="space-y-4">
							<div class="grid gap-4 md:grid-cols-2">
								<div class="form-control">
									<label class="label" for="newPassword">
										<span class="label-text">New Password</span>
									</label>
									<input
										id="newPassword"
										type="password"
										class="input input-bordered"
										bind:value={passwordForm.newPassword}
										placeholder="Enter new password"
										required
									/>
									<div class="label">
										<span class="label-text-alt">Minimum 8 characters</span>
									</div>
								</div>

								<div class="form-control">
									<label class="label" for="confirmPassword">
										<span class="label-text">Confirm Password</span>
									</label>
									<input
										id="confirmPassword"
										type="password"
										class="input input-bordered"
										bind:value={passwordForm.confirmPassword}
										placeholder="Confirm new password"
										required
									/>
								</div>
							</div>

							{#if passwordMessage}
								<div
									class="alert {passwordMessage.includes('successfully')
										? 'alert-success'
										: 'alert-error'}"
								>
									<span>{passwordMessage}</span>
								</div>
							{/if}

							<div class="card-actions justify-end gap-2">
								<button
									type="button"
									class="btn btn-ghost"
									onclick={() => {
										showPasswordForm = false;
										passwordForm.newPassword = '';
										passwordForm.confirmPassword = '';
										passwordMessage = '';
									}}
								>
									Cancel
								</button>
								<button type="submit" class="btn btn-primary" disabled={isLoading}>
									{#if isLoading}
										<span class="loading loading-spinner loading-sm"></span>
									{/if}
									Update Password
								</button>
							</div>
						</form>
					{:else}
						<p class="text-base-content/70">••••••••</p>
					{/if}
				</div>
			</div>
		</div>
	</div>
</div>

<!-- Avatar Upload Modal -->
<dialog id="avatar-upload-modal" class="modal">
	<div class="modal-box">
		<div class="flex items-center justify-between">
			<h3 class="text-lg font-bold">Change Profile Picture</h3>
			<form method="dialog">
				<button class="btn btn-ghost btn-sm btn-circle" aria-label="Close modal">
					<span class="iconify lucide--x size-4"></span>
				</button>
			</form>
		</div>

		<div class="py-4">
			<div class="form-control">
				<label class="label" for="avatarFile">
					<span class="label-text">Choose Image</span>
				</label>
				<input
					id="avatarFile"
					type="file"
					accept="image/jpeg,image/jpg,image/png,image/webp"
					class="file-input file-input-bordered"
					onchange={handleAvatarFileChange}
				/>
				<div class="label">
					<span class="label-text-alt">JPEG, PNG, or WebP • Max 2MB</span>
				</div>
			</div>

			{#if avatarFile}
				<div class="mt-4">
					<div class="alert alert-info">
						<span class="iconify lucide--info size-4"></span>
						<span>Selected: {avatarFile.name} ({Math.round(avatarFile.size / 1024)}KB)</span>
					</div>
				</div>
			{/if}

			{#if avatarMessage}
				<div
					class="alert mt-4 {avatarMessage.includes('successfully')
						? 'alert-success'
						: 'alert-error'}"
				>
					<span>{avatarMessage}</span>
				</div>
			{/if}

			<div class="mt-6 flex justify-end gap-2">
				<form method="dialog">
					<button
						class="btn btn-ghost"
						onclick={() => {
							avatarFile = null;
							avatarMessage = '';
						}}
					>
						Cancel
					</button>
				</form>
				<button class="btn btn-primary" onclick={uploadAvatar} disabled={!avatarFile || isLoading}>
					{#if isLoading}
						<span class="loading loading-spinner loading-sm"></span>
					{:else}
						<span class="iconify lucide--upload size-4"></span>
					{/if}
					Upload
				</button>
			</div>
		</div>
	</div>
	<form method="dialog" class="modal-backdrop">
		<button>close</button>
	</form>
</dialog>
