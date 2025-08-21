<script lang="ts">
	import Logo from '$lib/components/Logo.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import { z } from 'zod';
	import { useFormValidation } from '$lib/util/useFormValidation.svelte';
	import { acceptInvitation } from '$lib/api/gen/invitations';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { LOGIN_PATH } from '$lib/config/constants';

	let showPassword = $state(false);
	let loading = $state(false);
	let apiError = $state('');
	let invitationToken = $state('');
	let successState = $state(false);

	const schema = z.object({
		firstName: z.string().min(1, 'First name is required'),
		lastName: z.string().min(1, 'Last name is required'),
		password: z.string().min(6, 'Password must be at least 6 characters'),
		organizationName: z.string().optional()
	});

	const { formData, errors, handleChange, handleSubmit } = useFormValidation({
		schema,
		initialValues: {
			firstName: '',
			lastName: '',
			password: '',
			organizationName: ''
		}
	});

	onMount(() => {
		const token = $page.url.searchParams.get('token');
		if (!token) {
			apiError = 'Invalid invitation link. Please check your email for the correct link.';
		} else {
			invitationToken = token;
		}
	});

	const submitInvitationAcceptance = async (e: Event) => {
		if (!invitationToken) {
			apiError = 'Invalid invitation link. Please check your email for the correct link.';
			return;
		}

		handleSubmit(e, async (data) => {
			loading = true;
			apiError = '';
			try {
				await acceptInvitation({
					token: invitationToken,
					password: data.password,
					first_name: data.firstName,
					last_name: data.lastName,
					organization_name: data.organizationName || undefined
				});
				successState = true;
			} catch (err: any) {
				if (err?.response?.status === 400) {
					apiError =
						'Invalid or expired invitation. Please contact your administrator for a new invitation.';
				} else if (err?.response?.status === 409) {
					apiError = 'An account with this email already exists.';
				} else {
					apiError = 'Failed to accept invitation. Please try again later.';
				}
			} finally {
				loading = false;
			}
		});
	};

	const handleLogin = () => {
		goto(LOGIN_PATH);
	};
</script>

<div class="flex flex-col items-stretch p-6 md:p-8 lg:p-16">
	<div class="flex items-center justify-between">
		<a href="/">
			<Logo />
		</a>
		<ThemeToggle class="btn btn-circle btn-outline border-base-300" />
	</div>

	{#if successState}
		<!-- Success State -->
		<div class="mt-8 text-center md:mt-12 lg:mt-24">
			<div class="mb-6">
				<span class="iconify lucide--check-circle text-success mb-4 block text-6xl"></span>
			</div>
			<h3 class="mb-2 text-2xl font-semibold">Welcome to the team!</h3>
			<p class="text-base-content/70 mb-6">
				Your account has been successfully created. You can now log in to access your dashboard.
			</p>
			<button type="button" class="btn btn-primary gap-2" onclick={handleLogin}>
				<span class="iconify lucide--log-in"></span>
				Continue to Login
			</button>
		</div>
	{:else}
		<!-- Form State -->
		<h3 class="mt-8 text-center text-xl font-semibold md:mt-12 lg:mt-24">Accept Invitation</h3>
		<h3 class="text-base-content/70 mt-2 text-center text-sm">
			Complete your account setup to join the organization.
		</h3>

		<form onsubmit={submitInvitationAcceptance} novalidate class="mt-6 md:mt-10">
			<div class="grid grid-cols-1 gap-x-4 xl:grid-cols-2">
				<fieldset class="fieldset">
					<legend class="fieldset-legend">First Name</legend>
					<label class="input w-full focus:outline-0">
						<span class="iconify lucide--user text-base-content/80 size-5"></span>
						<input
							class="grow focus:outline-0"
							placeholder="First Name"
							name="firstName"
							type="text"
							bind:value={formData.firstName}
							oninput={handleChange}
							data-error={errors.firstName ? true : undefined}
						/>
					</label>
					<p
						class="text-error hidden text-sm data-error:block"
						data-error={errors.firstName ? true : undefined}
					>
						{errors.firstName}
					</p>
				</fieldset>
				<fieldset class="fieldset">
					<legend class="fieldset-legend">Last Name</legend>
					<label class="input w-full focus:outline-0">
						<span class="iconify lucide--user text-base-content/80 size-5"></span>
						<input
							class="grow focus:outline-0"
							placeholder="Last Name"
							name="lastName"
							type="text"
							bind:value={formData.lastName}
							oninput={handleChange}
							data-error={errors.lastName ? true : undefined}
						/>
					</label>
					<p
						class="text-error hidden text-sm data-error:block"
						data-error={errors.lastName ? true : undefined}
					>
						{errors.lastName}
					</p>
				</fieldset>
			</div>

			<fieldset class="fieldset">
				<legend class="fieldset-legend">Password</legend>
				<label class="input w-full focus:outline-0">
					<span class="iconify lucide--key-round text-base-content/80 size-5"></span>
					<input
						class="grow focus:outline-0"
						placeholder="Create a secure password"
						name="password"
						type={showPassword ? 'text' : 'password'}
						bind:value={formData.password}
						oninput={handleChange}
						data-error={errors.password ? true : undefined}
					/>
					<button
						aria-label="Password"
						class="btn btn-xs btn-ghost btn-circle"
						onclick={() => (showPassword = !showPassword)}
						type="button"
					>
						{#if showPassword}
							<span class="iconify lucide--eye-off size-4"></span>
						{:else}
							<span class="iconify lucide--eye size-4"></span>
						{/if}
					</button>
				</label>
				<p
					class="text-error hidden text-sm data-error:block"
					data-error={errors.password ? true : undefined}
				>
					{errors.password}
				</p>
			</fieldset>

			<fieldset class="fieldset">
				<legend class="fieldset-legend">Organization Name (Optional)</legend>
				<label class="input w-full focus:outline-0">
					<span class="iconify lucide--building text-base-content/80 size-5"></span>
					<input
						class="grow focus:outline-0"
						placeholder="Leave empty to use default name"
						name="organizationName"
						type="text"
						bind:value={formData.organizationName}
						oninput={handleChange}
					/>
				</label>
				<p class="text-base-content/60 mt-1 text-xs">
					Only required for system admin invitations without an organization
				</p>
			</fieldset>

			<button
				type="submit"
				class="btn btn-primary btn-wide mt-6 max-w-full gap-3"
				disabled={loading || !invitationToken}
			>
				{#if loading}
					<span class="loading loading-dots loading-sm"></span>
				{:else}
					<span class="iconify lucide--user-check size-4"></span>
				{/if}
				Accept Invitation
			</button>

			{#if apiError}
				<p class="text-error mt-2 animate-pulse text-center text-sm">{apiError}</p>
			{/if}

			<p class="text-base-content/80 mt-6 text-center text-sm">
				Already have an account?
				<a class="text-primary ms-1 hover:underline" href={LOGIN_PATH}>Sign In</a>
			</p>
		</form>
	{/if}
</div>
