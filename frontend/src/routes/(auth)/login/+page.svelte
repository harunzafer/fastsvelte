<script lang="ts">
	import Logo from '$lib/components/Logo.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import { z } from 'zod';
	import { useFormValidation } from '$lib/util/useFormValidation.svelte';
	import { login } from '$lib/api/gen/authentication';
	import { initiateGoogleOAuth, checkOAuthError } from '$lib/auth/oauth/google';
	import { goto } from '$app/navigation';
	import {
		DASHBOARD_PATH,
		FORGOT_PASSWORD_PATH,
		REGISTER_PATH,
		VERIFY_EMAIL_PATH
	} from '$lib/config/constants';
	import { onMount } from 'svelte';
	import { page } from '$app/state';

	let showPassword = $state(false);
	let loading = $state(false);
	let apiError = $state('');
	let showVerificationSuccess = $state(false);
	let showPasswordResetSuccess = $state(false);
	let oauthError = $state('');

	onMount(() => {
		// Check if user came from email verification
		const verified = page.url.searchParams.get('verified');
		if (verified === 'true') {
			showVerificationSuccess = true;
		}

		// Check if user came from password reset
		const message = page.url.searchParams.get('message');
		if (message === 'password-reset-success') {
			showPasswordResetSuccess = true;
		}

		// Check for OAuth errors
		const oauthErrorMessage = checkOAuthError(page.url.searchParams);
		if (oauthErrorMessage) {
			oauthError = oauthErrorMessage;
		}
	});

	const schema = z.object({
		email: z.email('Invalid email address'),
		password: z.string().min(6, 'Password must be at least 6 characters')
	});

	const { formData, errors, handleChange, handleSubmit } = useFormValidation({
		schema,
		initialValues: {
			email: '',
			password: ''
		}
	});

	const submitLogin = async (e: Event) => {
		handleSubmit(e, async (data) => {
			loading = true;
			apiError = '';
			try {
				const res = await login({ email: data.email, password: data.password });
				goto(DASHBOARD_PATH); // redirect on success
			} catch (err: any) {
				if (err?.response?.data?.code === 'EMAIL_NOT_VERIFIED') {
					// Redirect to verification page with email
					goto(`${VERIFY_EMAIL_PATH}?email=${encodeURIComponent(data.email)}`);
				} else if (err?.response?.status === 401) {
					apiError = 'Invalid email or password.';
				} else {
					apiError = 'Login failed. Please try again later.';
				}
			} finally {
				loading = false;
			}
		});
	};

	const handleGoogleLogin = () => initiateGoogleOAuth(
		(error) => apiError = error,
		(isLoading) => loading = isLoading
	);
</script>

<form onsubmit={submitLogin} novalidate class="flex flex-col items-stretch p-6 md:p-8 lg:p-16">
	<div class="flex items-center justify-between">
		<a href="/dashboards/ecommerce">
			<Logo />
		</a>
		<ThemeToggle class="btn btn-circle btn-outline border-base-300" />
	</div>

	<h3 class="mt-8 text-center text-xl font-semibold md:mt-12 lg:mt-24">Login</h3>
	{#if showVerificationSuccess}
		<div class="alert alert-success mt-3">
			<span class="iconify lucide--check-circle size-5"></span>
			<span>Email verified successfully! You can now log in to your account.</span>
		</div>
	{/if}
	{#if showPasswordResetSuccess}
		<div class="alert alert-success mt-3">
			<span class="iconify lucide--check-circle size-5"></span>
			<span>Password reset successfully! You can now log in with your new password.</span>
		</div>
	{/if}
	{#if oauthError}
		<div class="alert alert-warning mt-3">
			<span class="iconify lucide--alert-triangle size-5"></span>
			<span>{oauthError}</span>
		</div>
	{/if}
	<div class="mt-5 md:mt-3">
		<fieldset class="fieldset">
			<legend class="fieldset-legend">Email Address</legend>
			<label class="input w-full focus:outline-0">
				<span class="iconify lucide--mail text-base-content/80 size-5"></span>
				<input
					class="grow focus:outline-0"
					placeholder="Email Address"
					name="email"
					type="email"
					bind:value={formData.email}
					oninput={handleChange}
					data-error={errors.email ? true : undefined}
				/>
			</label>
			<p
				class="text-error data-error:block hidden text-sm"
				data-error={errors.email ? true : undefined}
			>
				{errors.email}
			</p>
		</fieldset>

		<fieldset class="fieldset">
			<legend class="fieldset-legend">Password</legend>
			<label class="input w-full focus:outline-0">
				<span class="iconify lucide--key-round text-base-content/80 size-5"></span>
				<input
					class="grow focus:outline-0"
					placeholder="Password"
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
				class="text-error data-error:block hidden text-sm"
				data-error={errors.password ? true : undefined}
			>
				{errors.password}
			</p>
		</fieldset>

		<div class="text-end">
			<a class="label-text text-base-content/80 text-xs" href={FORGOT_PASSWORD_PATH}>
				Forgot Password?
			</a>
		</div>

		<button
			type="submit"
			class="btn btn-primary btn-wide mt-4 max-w-full gap-3 md:mt-6"
			disabled={loading}
		>
			{#if loading}
				<span class="loading loading-dots loading-sm"></span>
			{:else}
				<span class="iconify lucide--log-in size-4"></span>
				Login
			{/if}
		</button>

		{#if apiError}
			<p class="text-error mt-2 animate-pulse text-center text-sm">{apiError}</p>
		{/if}

		<button
			type="button"
			class="btn btn-ghost btn-wide border-base-300 mt-4 max-w-full gap-3"
			onclick={handleGoogleLogin}
			disabled={loading}
		>
			<img alt="" class="size-6" src="/images/brand-logo/google-mini.svg" />
			Login with Google
		</button>

		<p class="text-base-content/80 mt-4 text-center text-sm md:mt-6">
			Haven&apos;t account
			<a class="text-primary ms-1 hover:underline" href={REGISTER_PATH}> Create One </a>
		</p>
	</div>
</form>
