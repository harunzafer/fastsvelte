<script>
	import Logo from '$lib/components/Logo.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import { resetPasswordWithToken } from '$lib/api/gen/password-management';
	import { useFormValidation } from '$lib/util/useFormValidation.svelte';
	import { z } from 'zod';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	let showPassword = $state(false);
	let isSubmitting = $state(false);
	let error = $state('');

	const token = $page.url.searchParams.get('token') || '';

	if (!token) {
		goto('/login');
	}

	const schema = z
		.object({
			password: z.string().min(8, 'Password must be at least 8 characters'),
			confirmPassword: z.string().min(8, 'Password must be at least 8 characters')
		})
		.refine((data) => data.password === data.confirmPassword, {
			message: "Passwords don't match",
			path: ['confirmPassword']
		});

	const { formData, errors, handleSubmit } = useFormValidation({
		schema,
		initialValues: { password: '', confirmPassword: '' }
	});

	async function onSubmit() {
		isSubmitting = true;
		error = '';

		try {
			await resetPasswordWithToken({
				token,
				new_password: formData.password
			});
			goto('/login?message=password-reset-success');
		} catch (err) {
			console.error('Reset password error:', err);
			if (err.response?.status === 400) {
				error = 'Invalid or expired reset token. Please request a new password reset.';
			} else {
				error = 'An error occurred. Please try again.';
			}
		} finally {
			isSubmitting = false;
		}
	}
</script>

<div class="flex flex-col items-stretch p-8 lg:p-16">
	<div class="flex items-center justify-between">
		<a href="/">
			<Logo />
		</a>
		<ThemeToggle class="btn btn-circle btn-outline border-base-300" />
	</div>
	<h3 class="mt-8 text-center text-xl font-semibold md:mt-12 lg:mt-24">Reset Password</h3>
	<h3 class="text-base-content/70 mt-2 text-center text-sm">Enter your new password below.</h3>

	<form onsubmit={(e) => handleSubmit(e, onSubmit)} class="mt-6 md:mt-10">
		<fieldset class="fieldset">
			<legend class="fieldset-legend">New Password</legend>
			<label class="input w-full focus:outline-0" class:input-error={errors.password}>
				<span class="iconify lucide--key-round text-base-content/80 size-5"></span>
				<input
					bind:value={formData.password}
					name="password"
					class="grow focus:outline-0"
					placeholder="New Password"
					type={showPassword ? 'text' : 'password'}
					disabled={isSubmitting}
				/>
				<button
					type="button"
					class="btn btn-xs btn-ghost btn-circle"
					onclick={() => (showPassword = !showPassword)}
					aria-label="Toggle password visibility"
				>
					{#if showPassword}
						<span class="iconify lucide--eye-off size-4"></span>
					{:else}
						<span class="iconify lucide--eye size-4"></span>
					{/if}
				</button>
			</label>
			{#if errors.password}
				<div class="label">
					<span class="label-text-alt text-error">{errors.password}</span>
				</div>
			{/if}
		</fieldset>

		<fieldset class="fieldset">
			<legend class="fieldset-legend">Confirm Password</legend>
			<label class="input w-full focus:outline-0" class:input-error={errors.confirmPassword}>
				<span class="iconify lucide--key-round text-base-content/80 size-5"></span>
				<input
					bind:value={formData.confirmPassword}
					name="confirmPassword"
					class="grow focus:outline-0"
					placeholder="Confirm Password"
					type={showPassword ? 'text' : 'password'}
					disabled={isSubmitting}
				/>
				<button
					type="button"
					class="btn btn-xs btn-ghost btn-circle"
					onclick={() => (showPassword = !showPassword)}
					aria-label="Toggle password visibility"
				>
					{#if showPassword}
						<span class="iconify lucide--eye-off size-4"></span>
					{:else}
						<span class="iconify lucide--eye size-4"></span>
					{/if}
				</button>
			</label>
			{#if errors.confirmPassword}
				<div class="label">
					<span class="label-text-alt text-error">{errors.confirmPassword}</span>
				</div>
			{/if}
		</fieldset>

		{#if error}
			<div class="alert alert-error mt-4">
				<span class="iconify lucide--alert-circle size-4"></span>
				<span>{error}</span>
			</div>
		{/if}

		<button
			type="submit"
			class="btn btn-primary btn-wide mt-4 max-w-full gap-3 md:mt-6"
			disabled={isSubmitting}
		>
			{#if isSubmitting}
				<span class="loading loading-spinner loading-sm"></span>
				Resetting...
			{:else}
				<span class="iconify lucide--check size-4"></span>
				Reset Password
			{/if}
		</button>

		<p class="mt-4 text-center text-sm md:mt-6">
			Remember your password?
			<a class="text-primary ms-1.5 hover:underline" href="/login">Login</a>
		</p>
	</form>
</div>
