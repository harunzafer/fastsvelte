<script lang="ts">
	import Logo from '$lib/components/Logo.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import { z } from 'zod';
	import { useFormValidation } from './useFormValidation.svelte';
	import { login } from '$lib/api/gen/authentication';
	import { goto } from '$app/navigation';
	import { DASHBOARD_PATH } from '$lib/config/constants';

	let showPassword = $state(false);
	let loading = $state(false);
	let apiError = $state('');

	const schema = z.object({
		email: z.string().email('Enter a valid email'),
		password: z.string().min(6, 'Password must be at least 6 characters'),
		agreement: z.boolean().refine((val) => val, {
			message: 'Accept terms to continue'
		})
	});

	const { formData, errors, handleChange, handleSubmit } = useFormValidation({
		schema,
		initialValues: {
			email: '',
			password: '',
			agreement: false
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
				if (err?.response?.status === 401) {
					apiError = 'Invalid email or password.';
				} else {
					apiError = 'Login failed. Please try again later.';
				}
			} finally {
				loading = false;
			}
		});
	};
</script>

<form onsubmit={submitLogin} novalidate class="flex flex-col items-stretch p-6 md:p-8 lg:p-16">
	<div class="flex items-center justify-between">
		<a href="/dashboards/ecommerce">
			<Logo />
		</a>
		<ThemeToggle class="btn btn-circle btn-outline border-base-300" />
	</div>

	<h3 class="mt-8 text-center text-xl font-semibold md:mt-12 lg:mt-24">Login</h3>
	<h3 class="text-base-content/70 mt-2 text-center text-sm">
		Seamless Access, Secure Connection: Your Gateway to a Personalized Experience.
	</h3>
	<div class="mt-6 md:mt-10">
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

		<div class="text-end">
			<a class="label-text text-base-content/80 text-xs" href="/auth/forgot-password">
				Forgot Password?
			</a>
		</div>

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
				<span class="iconify lucide--log-in size-4"></span>
				Login
			{/if}
		</button>

		{#if apiError}
			<p class="text-error mt-2 animate-pulse text-center text-sm">{apiError}</p>
		{/if}

		<button class="btn btn-ghost btn-wide border-base-300 mt-4 max-w-full gap-3">
			<img alt="" class="size-6" src="/images/brand-logo/google-mini.svg" />
			Login with Google
		</button>

		<p class="text-base-content/80 mt-4 text-center text-sm md:mt-6">
			Haven&apos;t account
			<a class="text-primary ms-1 hover:underline" href="/"> Create One </a>
		</p>
	</div>
</form>
