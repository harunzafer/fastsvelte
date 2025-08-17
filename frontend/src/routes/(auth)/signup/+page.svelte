<script lang="ts">
	import Logo from '$lib/components/Logo.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import { z } from 'zod';
	import { useFormValidation } from '$lib/util/useFormValidation.svelte';
	import { signup } from '$lib/api/gen/authentication'; // Assuming this exists
	import { goto } from '$app/navigation';
	import { DASHBOARD_PATH, VERIFY_EMAIL_PATH } from '$lib/config/constants';

	let showPassword = $state(false);
	let loading = $state(false);
	let apiError = $state('');

	const schema = z.object({
		firstName: z.string().min(1, 'First name is required'),
		lastName: z.string().min(1, 'Last name is required'),
		email: z.email('Invalid email address'),
		password: z.string().min(6, 'Password must be at least 6 characters'),
		agreement: z.boolean().refine((val) => val, {
			message: 'Accept terms to continue'
		})
	});

	const { formData, errors, handleChange, handleSubmit } = useFormValidation({
		schema,
		initialValues: {
			firstName: '',
			lastName: '',
			email: '',
			password: '',
			agreement: false
		}
	});

	const submitSignup = async (e: Event) => {
		handleSubmit(e, async (data) => {
			loading = true;
			apiError = '';
			try {
				const res = await signup({
					email: data.email,
					password: data.password,
					first_name: data.firstName,
					last_name: data.lastName
				});
				// After successful signup, redirect to email verification page
				goto(VERIFY_EMAIL_PATH + `?email=${encodeURIComponent(data.email)}`);
			} catch (err: any) {
				if (err?.response?.status === 400) {
					apiError = 'Invalid data. Please check your inputs.';
				} else if (err?.response?.status === 409) {
					apiError = 'An account with this email already exists.';
				} else {
					apiError = 'Registration failed. Please try again later.';
				}
			} finally {
				loading = false;
			}
		});
	};
</script>

<form onsubmit={submitSignup} novalidate class="flex flex-col items-stretch p-6 md:p-8 lg:p-16">
	<div class="flex items-center justify-between">
		<a href="/dashboards/ecommerce">
			<Logo />
		</a>
		<ThemeToggle class="btn btn-circle btn-outline border-base-300" />
	</div>

	<h3 class="mt-8 text-center text-xl font-semibold md:mt-12 lg:mt-24">Register</h3>
	<h3 class="text-base-content/70 mt-2 text-center text-sm">
		Seamless Access, Secure Connection: Your Gateway to a Personalized Experience.
	</h3>
	<div class="mt-6 md:mt-10">
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

		<!-- Username field commented out as requested -->
		<!-- 
		<fieldset class="fieldset">
			<legend class="fieldset-legend">Username</legend>
			<label class="input w-full focus:outline-0">
				<span class="iconify lucide--user-square text-base-content/80 size-5"></span>
				<input class="grow focus:outline-0" placeholder="Username" type="text" />
			</label>
		</fieldset>
		-->

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
				class="text-error hidden text-sm data-error:block"
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
				class="text-error hidden text-sm data-error:block"
				data-error={errors.password ? true : undefined}
			>
				{errors.password}
			</p>
		</fieldset>

		<div class="mt-4 flex items-center gap-3 md:mt-6">
			<input
				aria-label="Agreement"
				class="checkbox checkbox-sm checkbox-primary"
				id="agreement"
				name="agreement"
				type="checkbox"
				bind:checked={formData.agreement}
				onchange={handleChange}
				data-error={errors.agreement ? true : undefined}
				data-testid="agreement"
			/>
			<label class="text-sm" for="agreement">
				I agree with
				<span class="text-primary ms-1 cursor-pointer hover:underline">terms and conditions</span>
			</label>
		</div>

		{#if errors.agreement}
			<p class="text-error text-sm">{errors.agreement}</p>
		{/if}

		<button
			type="submit"
			class="btn btn-primary btn-wide mt-4 max-w-full gap-3 md:mt-6"
			disabled={loading}
		>
			{#if loading}
				<span class="loading loading-dots loading-sm"></span>
			{:else}
				<span class="iconify lucide--user-plus size-4"></span>
				Register
			{/if}
		</button>

		{#if apiError}
			<p class="text-error mt-2 animate-pulse text-center text-sm">{apiError}</p>
		{/if}

		<button class="btn btn-ghost btn-wide border-base-300 mt-4 max-w-full gap-3" type="button">
			<img alt="" class="size-6" src="/images/brand-logo/google-mini.svg" />
			Register with Google
		</button>

		<p class="text-base-content/80 mt-4 text-center text-sm md:mt-6">
			I have already to
			<a class="text-primary ms-1 hover:underline" href="/login">Login</a>
		</p>
	</div>
</form>
