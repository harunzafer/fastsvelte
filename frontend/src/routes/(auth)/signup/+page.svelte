<script lang="ts">
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/store/auth.svelte';
	import { validateCurrentUser } from '$lib/util/session';
	import { signup as registerUser } from '$lib/api/gen/authentication';
	import { z } from 'zod';

	let firstName = $state('');
	let lastName = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let isLoading = $state(false);
	let errors: Record<string, string> = $state({});

	// Zod validation schema
	const signupSchema = z
		.object({
			firstName: z.string().min(1, 'First name is required'),
			lastName: z.string().min(1, 'Last name is required'),
			email: z.email({ message: 'Invalid email address' }),
			password: z
				.string()
				.min(1, 'Password is required')
				.min(6, 'Password must be at least 6 characters'),
			confirmPassword: z.string().min(1, 'Please confirm your password')
		})
		.refine((data) => data.password === data.confirmPassword, {
			message: "Passwords don't match",
			path: ['confirmPassword']
		});

	// // Redirect if already authenticated
	// $effect(() => {
	// 	if (authStore.isAuthenticated) {
	// 		goto('/');
	// 	}
	// });

	function validateForm() {
		errors = {};

		try {
			signupSchema.parse({ firstName, lastName, email, password, confirmPassword });
			return true;
		} catch (error) {
			if (error instanceof z.ZodError) {
				error.issues.forEach((err) => {
					if (err.path[0]) {
						errors[err.path[0] as string] = err.message;
					}
				});
			}
			return false;
		}
	}

	async function handleSignup(event: SubmitEvent) {
		event.preventDefault();

		// Clear previous errors
		errors = {};

		// Validate form
		if (!validateForm()) {
			return;
		}

		isLoading = true;

		try {
			// Step 1: Register user
			await registerUser({
				email,
				password,
				first_name: firstName,
				last_name: lastName
			});

			// Step 2: Get full user data after successful registration
			const success = await validateCurrentUser();

			if (success && authStore.user) {
				// Redirect to dashboard
				goto('/');
			} else {
				errors.general = 'Registration succeeded but failed to get user data';
			}
		} catch (err) {
			console.error('Signup failed:', err);
			errors.general = err.response?.data?.detail || 'Registration failed. Please try again.';
		} finally {
			isLoading = false;
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleSignup(event);
		}
	}

	// Real-time validation functions
	function handleFirstNameBlur() {
		try {
			signupSchema.shape.firstName.parse(firstName);
			if (errors.firstName) {
				const { firstName: _, ...rest } = errors;
				errors = rest;
			}
		} catch (error) {
			if (error instanceof z.ZodError) {
				errors.firstName = error.errors[0]?.message || 'Invalid first name';
			}
		}
	}

	function handleLastNameBlur() {
		try {
			signupSchema.shape.lastName.parse(lastName);
			if (errors.lastName) {
				const { lastName: _, ...rest } = errors;
				errors = rest;
			}
		} catch (error) {
			if (error instanceof z.ZodError) {
				errors.lastName = error.errors[0]?.message || 'Invalid last name';
			}
		}
	}

	function handleEmailBlur() {
		try {
			signupSchema.shape.email.parse(email);
			if (errors.email) {
				const { email: _, ...rest } = errors;
				errors = rest;
			}
		} catch (error) {
			if (error instanceof z.ZodError) {
				errors.email = error.errors[0]?.message || 'Invalid email';
			}
		}
	}

	function handlePasswordBlur() {
		try {
			signupSchema.shape.password.parse(password);
			if (errors.password) {
				const { password: _, ...rest } = errors;
				errors = rest;
			}
		} catch (error) {
			if (error instanceof z.ZodError) {
				errors.password = error.errors[0]?.message || 'Invalid password';
			}
		}
	}

	function handleConfirmPasswordBlur() {
		try {
			signupSchema.parse({ firstName, lastName, email, password, confirmPassword });
			if (errors.confirmPassword) {
				const { confirmPassword: _, ...rest } = errors;
				errors = rest;
			}
		} catch (error) {
			if (error instanceof z.ZodError) {
				const confirmPasswordError = error.errors.find((err) => err.path[0] === 'confirmPassword');
				if (confirmPasswordError) {
					errors.confirmPassword = confirmPasswordError.message;
				}
			}
		}
	}

	function handleGoogleSignup() {
		// TODO: Implement Google OAuth signup
		console.log('Google signup clicked');
	}
</script>

<svelte:head>
	<title>Sign Up - FastSvelte</title>
</svelte:head>

<div class="bg-base-200 flex min-h-screen items-center justify-center p-4">
	<div class="card bg-base-100 w-full max-w-md shadow-xl">
		<div class="card-body">
			<!-- Header -->
			<div class="mb-6 text-center">
				<h1 class="text-3xl font-bold">Create Account</h1>
				<p class="text-base-content/60 mt-2">Sign up to get started</p>
			</div>

			<!-- General Error Alert -->
			{#if errors.general}
				<div class="alert alert-error mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-6 w-6 shrink-0 stroke-current"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<span>{errors.general}</span>
				</div>
			{/if}

			<!-- Signup Form -->
			<form onsubmit={handleSignup}>
				<!-- Name Fields -->
				<div class="mb-4 grid grid-cols-2 gap-4">
					<!-- First Name -->
					<div class="form-control">
						<label class="label" for="firstName">
							<span class="label-text">First Name</span>
						</label>
						<input
							id="firstName"
							type="text"
							placeholder="First name"
							class="input input-bordered w-full"
							class:input-error={errors.firstName}
							bind:value={firstName}
							onblur={handleFirstNameBlur}
							onkeydown={handleKeydown}
							disabled={isLoading}
							required
						/>
						{#if errors.firstName}
							<div class="label">
								<span class="label-text-alt text-error">{errors.firstName}</span>
							</div>
						{/if}
					</div>

					<!-- Last Name -->
					<div class="form-control">
						<label class="label" for="lastName">
							<span class="label-text">Last Name</span>
						</label>
						<input
							id="lastName"
							type="text"
							placeholder="Last name"
							class="input input-bordered w-full"
							class:input-error={errors.lastName}
							bind:value={lastName}
							onblur={handleLastNameBlur}
							onkeydown={handleKeydown}
							disabled={isLoading}
							required
						/>
						{#if errors.lastName}
							<div class="label">
								<span class="label-text-alt text-error">{errors.lastName}</span>
							</div>
						{/if}
					</div>
				</div>

				<!-- Email Input -->
				<div class="form-control mb-4">
					<label class="label" for="email">
						<span class="label-text">Email</span>
					</label>
					<input
						id="email"
						type="email"
						placeholder="Enter your email"
						class="input input-bordered w-full"
						class:input-error={errors.email}
						bind:value={email}
						onblur={handleEmailBlur}
						onkeydown={handleKeydown}
						disabled={isLoading}
						required
					/>
					{#if errors.email}
						<div class="label">
							<span class="label-text-alt text-error">{errors.email}</span>
						</div>
					{/if}
				</div>

				<!-- Password Input -->
				<div class="form-control mb-4">
					<label class="label" for="password">
						<span class="label-text">Password</span>
					</label>
					<input
						id="password"
						type="password"
						placeholder="Create a password"
						class="input input-bordered w-full"
						class:input-error={errors.password}
						bind:value={password}
						onblur={handlePasswordBlur}
						onkeydown={handleKeydown}
						disabled={isLoading}
						required
					/>
					{#if errors.password}
						<div class="label">
							<span class="label-text-alt text-error">{errors.password}</span>
						</div>
					{/if}
				</div>

				<!-- Confirm Password Input -->
				<div class="form-control mb-6">
					<label class="label" for="confirmPassword">
						<span class="label-text">Confirm Password</span>
					</label>
					<input
						id="confirmPassword"
						type="password"
						placeholder="Confirm your password"
						class="input input-bordered w-full"
						class:input-error={errors.confirmPassword}
						bind:value={confirmPassword}
						onblur={handleConfirmPasswordBlur}
						onkeydown={handleKeydown}
						disabled={isLoading}
						required
					/>
					{#if errors.confirmPassword}
						<div class="label">
							<span class="label-text-alt text-error">{errors.confirmPassword}</span>
						</div>
					{/if}
				</div>

				<!-- Submit Button -->
				<button
					type="submit"
					class="btn btn-primary w-full"
					class:loading={isLoading}
					disabled={isLoading}
				>
					{isLoading ? 'Creating Account...' : 'Create Account'}
				</button>
			</form>

			<!-- Divider -->
			<div class="divider">OR</div>

			<!-- Google Signup Button -->
			<button
				type="button"
				class="btn btn-outline mb-4 w-full"
				onclick={handleGoogleSignup}
				disabled={isLoading}
			>
				<svg class="mr-2 h-5 w-5" viewBox="0 0 24 24">
					<path
						fill="#4285F4"
						d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
					/>
					<path
						fill="#34A853"
						d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
					/>
					<path
						fill="#FBBC05"
						d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
					/>
					<path
						fill="#EA4335"
						d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
					/>
				</svg>
				Continue with Google
			</button>

			<!-- Sign In Link -->
			<div class="text-center">
				<p class="text-base-content/60">
					Already have an account?
					<a href="/login" class="link link-primary">Sign in</a>
				</p>
			</div>
		</div>
	</div>
</div>
