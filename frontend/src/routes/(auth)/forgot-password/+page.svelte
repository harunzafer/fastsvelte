<script>
    import Logo from "$lib/components/Logo.svelte";
    import ThemeToggle from "$lib/components/ThemeToggle.svelte";
    import { forgotPassword } from "$lib/api/gen/password-management";
    import { useFormValidation } from "$lib/util/useFormValidation.svelte";
    import { z } from "zod";

    let isSubmitting = $state(false);
    let isSubmitted = $state(false);
    let error = $state("");

    const schema = z.object({
        email: z.string().email("Please enter a valid email address")
    });

    const { formData, errors, handleSubmit } = useFormValidation({
        schema,
        initialValues: { email: "" }
    });

    async function onSubmit() {
        isSubmitting = true;
        error = "";

        try {
            await forgotPassword({ email: formData.email.trim().toLowerCase() });
            isSubmitted = true;
        } catch (err) {
            console.error("Forgot password error:", err);
            error = "An error occurred. Please try again.";
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
    
    {#if isSubmitted}
        <h3 class="mt-8 text-center text-xl font-semibold md:mt-12 lg:mt-24">Check Your Email</h3>
        <h3 class="text-base-content/70 mt-2 text-center text-sm">
            If an account with that email exists, we've sent you a password reset link.
        </h3>
        <div class="mt-6 md:mt-10">
            <a href="/login" class="btn btn-primary btn-wide mt-4 max-w-full gap-3 md:mt-6">
                <span class="iconify lucide--arrow-left size-4"></span>
                Back to Login
            </a>
        </div>
    {:else}
        <h3 class="mt-8 text-center text-xl font-semibold md:mt-12 lg:mt-24">Forgot Password</h3>
        <h3 class="text-base-content/70 mt-2 text-center text-sm">
            Enter your email address and we'll send you a link to reset your password.
        </h3>
        
        <form onsubmit={(e) => handleSubmit(e, onSubmit)} class="mt-6 md:mt-10">
            <fieldset class="fieldset">
                <legend class="fieldset-legend">Email Address</legend>
                <label class="input w-full focus:outline-0" class:input-error={errors.email}>
                    <span class="iconify lucide--mail text-base-content/80 size-5"></span>
                    <input 
                        bind:value={formData.email}
                        name="email"
                        class="grow focus:outline-0" 
                        placeholder="Email Address" 
                        type="email"
                        disabled={isSubmitting}
                    />
                </label>
                {#if errors.email}
                    <div class="label">
                        <span class="label-text-alt text-error">{errors.email}</span>
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
                    Sending...
                {:else}
                    <span class="iconify lucide--mail-plus size-4"></span>
                    Send Reset Link
                {/if}
            </button>
            
            <p class="text-base-content/80 mt-4 text-center text-sm md:mt-6">
                Remember your password?
                <a class="text-primary ms-1 hover:underline" href="/login">Login</a>
            </p>
        </form>
    {/if}
</div>