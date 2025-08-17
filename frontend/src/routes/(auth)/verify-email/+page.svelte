<script lang="ts">
	import Logo from '$lib/components/Logo.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';

	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { resendVerificationEmail, verifyEmail } from '$lib/api/gen/email-verification';

	let email = $state('');
	let isResending = $state(false);
	let resendSuccess = $state(false);
	let resendError = $state('');
	let isVerifying = $state(false);
	let verificationError = $state('');

	onMount(async () => {
		const token = page.url.searchParams.get('token');
		email = page.url.searchParams.get('email') || '';

		// If no token and no email, this is likely direct navigation
		// We'll show the "please login" message instead of redirecting

		// If there's a verification token, handle email verification
		if (token) {
			await handleEmailVerification(token);
		}
	});

	const handleEmailVerification = async (token: string) => {
		isVerifying = true;
		verificationError = '';

		try {
			await verifyEmail({ token });
			// Verification successful - redirect to login
			goto('/login?verified=true');
		} catch (err: any) {
			if (err?.response?.status === 400) {
				verificationError = 'Invalid or expired verification token.';
			} else {
				verificationError = 'Verification failed. Please try again.';
			}
		} finally {
			isVerifying = false;
		}
	};

	const handleResendEmail = async () => {
		isResending = true;
		resendError = '';
		resendSuccess = false;

		try {
			await resendVerificationEmail({ email });
			resendSuccess = true;
			resendError = '';
		} catch (err: any) {
			if (err?.response?.status === 404) {
				resendError = 'No account found with this email address.';
			} else if (err?.response?.data?.message?.includes('already verified')) {
				resendError = 'Email is already verified. Please try logging in.';
			} else {
				resendError = 'Failed to resend verification email. Please try again.';
			}
			resendSuccess = false;
		} finally {
			isResending = false;
		}
	};
</script>

<div class="flex flex-col items-stretch p-6 md:p-8 lg:p-16">
	<div class="flex items-center justify-between">
		<a href="/">
			<Logo />
		</a>
		<ThemeToggle class="btn btn-circle btn-outline border-base-300" />
	</div>

	<div class="mt-8 text-center md:mt-12 lg:mt-24">
		{#if isVerifying}
			<!-- Verifying token -->
			<div class="flex flex-col items-center gap-4">
				<span class="loading loading-spinner loading-lg text-primary"></span>
				<h3 class="text-xl font-semibold">Verifying your email...</h3>
				<p class="text-base-content/70 text-sm">Please wait while we verify your email address.</p>
			</div>
		{:else if verificationError}
			<!-- Verification failed -->
			<div class="flex flex-col items-center gap-4">
				<span class="iconify lucide--x-circle text-error size-16"></span>
				<h3 class="text-error text-xl font-semibold">Verification Failed</h3>
				<p class="text-base-content/70 max-w-md text-sm">
					{verificationError}
				</p>
				<p class="text-base-content/70 text-sm">You can request a new verification link below.</p>
			</div>
		{:else}
			<!-- Default verification page -->
			<div class="flex flex-col items-center gap-4">
				<span class="iconify lucide--mail text-primary size-16"></span>
				<h3 class="text-xl font-semibold">Check Your Email</h3>
				{#if email}
					<p class="text-base-content/70 max-w-md text-sm">
						We've sent a verification link to your email address. Click the link in the email to
						verify your account.
					</p>
					<p class="text-primary text-sm font-medium">
						{email}
					</p>
				{:else}
					<p class="text-base-content/70 max-w-md text-sm">
						Please log in with your email and password to continue with email verification.
					</p>
				{/if}
			</div>
		{/if}
	</div>

	<div class="mt-8 space-y-4">
		{#if email}
			<!-- Show resend section only if we have an email -->
			<div class="text-center">
				<p class="text-base-content/70 mb-4 text-sm">
					Didn't receive the email? Check your spam folder or resend the verification email.
				</p>

				<button class="btn btn-primary gap-2" onclick={handleResendEmail} disabled={isResending}>
					{#if isResending}
						<span class="loading loading-dots loading-sm"></span>
						Sending...
					{:else}
						<span class="iconify lucide--send size-4"></span>
						Resend Verification Email
					{/if}
				</button>

				{#if resendSuccess}
					<p class="text-success mt-2 text-sm">
						✓ Verification email sent successfully! Check your inbox.
					</p>
				{/if}

				{#if resendError}
					<p class="text-error mt-2 text-sm">
						{resendError}
					</p>
				{/if}
			</div>
		{/if}

		<!-- Navigation links -->
		<div class="border-base-300 border-t pt-4 text-center">
			{#if email}
				<p class="text-base-content/80 text-sm">
					Remember your password?
					<a class="text-primary ml-1 hover:underline" href="/login"> Back to Login </a>
				</p>
				<p class="text-base-content/80 mt-2 text-sm">
					Need to change your password?
					<a class="text-primary ml-1 hover:underline" href="/auth/forgot-password">
						Reset Password
					</a>
				</p>
			{:else}
				<p class="text-base-content/80 text-sm">
					<a class="text-primary hover:underline" href="/login"> ← Back to Login </a>
				</p>
				<p class="text-base-content/80 mt-2 text-sm">
					Don't have an account?
					<a class="text-primary ml-1 hover:underline" href="/signup"> Sign Up </a>
				</p>
			{/if}
		</div>
	</div>
</div>
