<script lang="ts">
	import { manageSubscription } from '$lib/api/gen/subscription';
	import { getCurrentPlan } from '$lib/api/gen/plan';
	import type { CurrentOrgPlanDetail } from '$lib/api/gen/model';
	import { onMount } from 'svelte';

	let loading = false;
	let planLoading = true;
	let currentPlan: CurrentOrgPlanDetail | null = null;

	onMount(async () => {
		try {
			const response = await getCurrentPlan();
			currentPlan = response.data;
		} catch (error) {
			console.error('Failed to fetch current plan:', error);
		} finally {
			planLoading = false;
		}
	});

	async function handleManageSubscription() {
		loading = true;
		try {
			const response = await manageSubscription();
			// Redirect to Stripe Customer Portal
			window.location.href = response.data.url;
		} catch (error) {
			console.error('Failed to create portal session:', error);
			// TODO: Show error toast/notification
		} finally {
			loading = false;
		}
	}

	function formatDate(dateStr: string | null | undefined): string {
		if (!dateStr) return '--';
		return new Date(dateStr).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	}

	function getStatusBadgeClass(status: string | null | undefined): string {
		switch (status?.toLowerCase()) {
			case 'active':
				return 'badge-success';
			case 'canceled':
			case 'cancelled':
				return 'badge-error';
			case 'past_due':
				return 'badge-warning';
			default:
				return 'badge-neutral';
		}
	}
</script>

<div class="container mx-auto max-w-4xl p-6">
	<!-- Page Header -->
	<div class="bg-primary/10 rounded-box relative mb-6 overflow-hidden p-6">
		<div class="flex justify-between">
			<div>
				<div class="flex items-center gap-1">
					<p class="text-base-content/80 text-sm">Account</p>
					<span class="iconify lucide--chevron-right text-base-content/80 size-3.5"></span>
					<p class="text-sm">Billing</p>
				</div>
				<p class="text-primary mt-4 text-xl font-medium">Subscription Management</p>
				<p class="text-base-content/80">
					Manage your subscription, billing history, and payment methods.
				</p>
			</div>
		</div>
		<span
			class="iconify lucide--credit-card text-primary/5 absolute start-1/2 -bottom-12 size-44 -rotate-25"
		></span>
	</div>

	<!-- Current Subscription Card -->
	<div class="card bg-base-100 card-border mb-6">
		<div class="card-body">
			<div class="mb-4 flex items-center gap-2">
				<span class="iconify lucide--package size-5"></span>
				<p class="text-lg font-medium">Current Subscription</p>
			</div>

			{#if planLoading}
				<div class="flex justify-center py-8">
					<span class="loading loading-spinner loading-md"></span>
				</div>
			{:else if currentPlan}
				<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
					<!-- Plan Status -->
					<div class="space-y-2">
						<p class="text-base-content/60 text-sm">Plan</p>
						<div class="flex items-center gap-2">
							<div class="badge badge-sm {getStatusBadgeClass(currentPlan.status)}">
								{currentPlan.status || 'Unknown'}
							</div>
							<p class="font-medium">{currentPlan.name}</p>
						</div>
						{#if currentPlan.description}
							<p class="text-base-content/60 text-sm">{currentPlan.description}</p>
						{/if}
					</div>

					<!-- Current Period -->
					<div class="space-y-2">
						<p class="text-base-content/60 text-sm">Current Period</p>
						<p class="font-medium">{formatDate(currentPlan.current_period_starts_at)}</p>
						<p class="text-base-content/60 text-xs">
							Started: {formatDate(currentPlan.subscription_started_at)}
						</p>
					</div>

					<!-- Next Billing Date -->
					<div class="space-y-2">
						<p class="text-base-content/60 text-sm">Next Billing Date</p>
						<p class="font-medium">{formatDate(currentPlan.current_period_ends_at)}</p>
						{#if currentPlan.ended_at}
							<p class="text-error text-xs">
								Ended: {formatDate(currentPlan.ended_at)}
							</p>
						{/if}
					</div>
				</div>

				<!-- Plan Features -->
				{#if currentPlan.features}
					<div class="divider">Plan Features</div>
					<div class="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
						{#if currentPlan.features.max_notes}
							<div class="flex items-center gap-2">
								<span class="iconify lucide--notebook text-primary size-4"></span>
								<span class="text-sm"
									>Max Notes: {currentPlan.features.max_notes === -1
										? 'Unlimited'
										: currentPlan.features.max_notes}</span
								>
							</div>
						{/if}
						{#if currentPlan.features.token_limit}
							<div class="flex items-center gap-2">
								<span class="iconify lucide--zap text-primary size-4"></span>
								<span class="text-sm"
									>Token Limit: {currentPlan.features.token_limit === -1
										? 'Unlimited'
										: currentPlan.features.token_limit}</span
								>
							</div>
						{/if}
						{#if currentPlan.features.enable_ai !== null}
							<div class="flex items-center gap-2">
								<span class="iconify lucide--brain text-primary size-4"></span>
								<span class="text-sm"
									>AI Features: {currentPlan.features.enable_ai ? 'Enabled' : 'Disabled'}</span
								>
							</div>
						{/if}
					</div>
				{/if}
			{:else}
				<div class="py-8 text-center">
					<p class="text-base-content/60">No subscription found</p>
				</div>
			{/if}
		</div>
	</div>

	<!-- Actions Card -->
	<div class="card bg-base-100 card-border">
		<div class="card-body">
			<div class="mb-4 flex items-center gap-2">
				<span class="iconify lucide--settings size-5"></span>
				<p class="text-lg font-medium">Manage Subscription</p>
			</div>

			<p class="text-base-content/60 mb-6">
				Access the Stripe Customer Portal to manage your subscription, update payment methods, view
				billing history, and download invoices.
			</p>

			<div class="flex gap-3">
				<button
					class="btn btn-primary"
					class:loading
					disabled={loading}
					on:click={handleManageSubscription}
				>
					<span class="iconify lucide--external-link size-4"></span>
					{loading ? 'Loading...' : 'Manage Subscription'}
				</button>
			</div>
		</div>
	</div>

	<!-- Features Card -->
	<div class="card bg-base-100 card-border mt-6">
		<div class="card-body">
			<div class="mb-4 flex items-center gap-2">
				<span class="iconify lucide--star size-5"></span>
				<p class="text-lg font-medium">What you can do</p>
			</div>

			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				<div class="flex items-start gap-3">
					<span class="iconify lucide--check text-success mt-0.5 size-4"></span>
					<div>
						<p class="font-medium">Update Payment Method</p>
						<p class="text-base-content/60 text-sm">
							Change your credit card or payment information
						</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<span class="iconify lucide--check text-success mt-0.5 size-4"></span>
					<div>
						<p class="font-medium">View Billing History</p>
						<p class="text-base-content/60 text-sm">Access all your past invoices and payments</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<span class="iconify lucide--check text-success mt-0.5 size-4"></span>
					<div>
						<p class="font-medium">Upgrade or Downgrade</p>
						<p class="text-base-content/60 text-sm">Change your subscription plan anytime</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<span class="iconify lucide--check text-success mt-0.5 size-4"></span>
					<div>
						<p class="font-medium">Download Invoices</p>
						<p class="text-base-content/60 text-sm">Get PDF copies of all your invoices</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
