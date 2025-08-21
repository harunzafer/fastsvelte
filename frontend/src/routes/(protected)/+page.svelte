<script lang="ts">
	import { authStore } from '$lib/auth/auth.svelte';
	import { listNotes, organizeNote } from '$lib/api/gen/notes';
	import { getStats } from '$lib/api/gen/statistics';
	import { onMount } from 'svelte';
	import type { NoteResponse, StatsResponse } from '$lib/api/gen/model';
	import Alert from '$lib/components/Alert.svelte';

	let notes = $state<NoteResponse[]>([]);
	let recentNotes = $state<NoteResponse[]>([]);
	let stats = $state<StatsResponse | null>(null);
	let loading = $state(true);
	let organizing = $state<Record<number, boolean>>({});
	let errorMessage = $state('');
	let showError = $state(false);
	let successMessage = $state('');
	let showSuccess = $state(false);

	onMount(async () => {
		loading = true;
		try {
			// Load stats and notes in parallel
			const [statsResponse, notesResponse] = await Promise.all([getStats(), listNotes()]);

			stats = statsResponse.data;
			notes = notesResponse.data || [];

			// Get 5 most recent notes for dashboard
			recentNotes = notes
				.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
				.slice(0, 5);
		} catch (error) {
			console.error('Failed to load dashboard data:', error);
		} finally {
			loading = false;
		}
	});

	async function handleOrganize(noteId: number) {
		organizing[noteId] = true;
		try {
			const response = await organizeNote(noteId);
			// Update the note in the recentNotes array
			const noteIndex = recentNotes.findIndex((note) => note.id === noteId);
			if (noteIndex !== -1) {
				recentNotes[noteIndex] = response.data;
			}
			successMessage = 'Note organized and improved!';
			showSuccess = true;
		} catch (error) {

			// Handle specific error types
			if (
				(error as any).response?.status === 403 &&
				(error as any).response?.data?.code === 'QUOTA_EXCEEDED'
			) {
				const feature = (error as any).response.data.details?.feature_key;
				if (feature === 'token_limit') {
					errorMessage =
						'Your current plan has reached the AI processing limit. Please upgrade your plan to continue using AI organization features.';
				} else {
					errorMessage =
						'Your current plan does not support this feature. Please upgrade your plan to continue.';
				}
			} else {
				errorMessage = 'Failed to organize note. Please try again later.';
			}
			showError = true;
		} finally {
			organizing[noteId] = false;
		}
	}

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString();
	}
</script>

<svelte:head>
	<title>Dashboard - FastSvelte</title>
</svelte:head>

<!-- Success Alert -->
<Alert
	type="success"
	message={successMessage}
	bind:show={showSuccess}
	autoDismiss={true}
	autoDismissDelay={3000}
/>

<!-- Error Alert -->
<Alert type="error" message={errorMessage} bind:show={showError} autoDismiss={true} />

<!-- Page Header -->
<div class="mb-8">
	<h1 class="text-3xl font-bold">Welcome back, {authStore.user?.first_name}!</h1>
	<p class="text-base-content/60 mt-2">Here's what's happening with your notes.</p>
</div>

<!-- Usage Statistics -->
<div class="mb-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
	<div class="card bg-base-100 cursor-pointer p-6 shadow transition-all hover:shadow-md">
		<div class="flex items-start justify-between">
			<div>
				<p class="text-sm font-medium opacity-70">Total Notes</p>
				{#if loading}
					<div class="skeleton mt-2 h-8 w-16"></div>
				{:else}
					<p class="text-primary mt-2 text-3xl font-bold">{stats?.total_notes || 0}</p>
				{/if}
				<p class="mt-1 text-sm opacity-60">All time</p>
			</div>
			<div class="text-primary opacity-80">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					class="h-8 w-8 stroke-current"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
					></path>
				</svg>
			</div>
		</div>
	</div>

	<div class="card bg-base-100 cursor-pointer p-6 shadow transition-all hover:shadow-md">
		<div class="flex items-start justify-between">
			<div>
				<p class="text-sm font-medium opacity-70">Recent Activity</p>
				{#if loading}
					<div class="skeleton mt-2 h-8 w-16"></div>
				{:else}
					<p class="text-secondary mt-2 text-3xl font-bold">{stats?.recent_notes || 0}</p>
				{/if}
				<p class="mt-1 text-sm opacity-60">Last 30 days</p>
			</div>
			<div class="text-secondary opacity-80">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					class="h-8 w-8 stroke-current"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
					></path>
				</svg>
			</div>
		</div>
	</div>

	<div class="card bg-base-100 cursor-pointer p-6 shadow transition-all hover:shadow-md">
		<div class="flex items-start justify-between">
			<div>
				<p class="text-sm font-medium opacity-70">AI Organized</p>
				<p class="text-accent mt-2 text-3xl font-bold">{stats?.ai_summaries_generated || 0}</p>
				<p class="mt-1 text-sm opacity-60">Notes improved</p>
			</div>
			<div class="text-accent opacity-80">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					class="h-8 w-8 stroke-current"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
					></path>
				</svg>
			</div>
		</div>
	</div>
</div>

<!-- Recent Notes -->
<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
	<div class="card bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Recent Notes</h2>

			{#if loading}
				<div class="space-y-4">
					{#each Array(3) as _}
						<div class="border-base-300 border-l-4 pl-4">
							<div class="skeleton mb-2 h-4 w-32"></div>
							<div class="skeleton mb-1 h-3 w-full"></div>
							<div class="skeleton h-3 w-20"></div>
						</div>
					{/each}
				</div>
			{:else if recentNotes.length === 0}
				<div class="py-8 text-center">
					<p class="text-base-content/60">No notes yet. Create your first note to get started!</p>
				</div>
			{:else}
				<div class="space-y-4">
					{#each recentNotes as note}
						<div class="border-primary border-l-4 pl-4">
							<div class="flex items-start justify-between">
								<div class="flex-1">
									<h3 class="font-medium">{note.title}</h3>
									<p class="mt-1 line-clamp-2 text-sm opacity-70">{note.content}</p>
									<p class="mt-2 text-xs opacity-50">{formatDate(note.updated_at)}</p>
								</div>
								<button
									class="btn btn-sm btn-ghost btn-circle ml-2"
									class:loading={organizing[note.id]}
									disabled={organizing[note.id]}
									onclick={() => handleOrganize(note.id)}
									title="AI Organize & Improve"
								>
									{#if !organizing[note.id]}
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											class="h-4 w-4 stroke-current"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"
											></path>
										</svg>
									{/if}
								</button>
							</div>
						</div>
					{/each}
				</div>
			{/if}

			<div class="card-actions justify-end">
				<a href="/notes" class="btn btn-primary btn-sm">View All Notes</a>
			</div>
		</div>
	</div>

	<!-- Quick Actions -->
	<div class="card bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Quick Actions</h2>

			<div class="grid grid-cols-2 gap-4">
				<a href="/notes?action=new" class="btn btn-outline btn-lg h-20 flex-col gap-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						class="h-6 w-6 stroke-current"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 6v6m0 0v6m0-6h6m-6 0H6"
						></path>
					</svg>
					<span class="text-xs">New Note</span>
				</a>

				<a href="/notes" class="btn btn-outline btn-lg h-20 flex-col gap-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						class="h-6 w-6 stroke-current"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
						></path>
					</svg>
					<span class="text-xs">Browse Notes</span>
				</a>

				<button class="btn btn-outline btn-lg h-20 flex-col gap-2" disabled>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						class="h-6 w-6 stroke-current"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
						></path>
					</svg>
					<span class="text-xs">AI Insights</span>
				</button>

				<button class="btn btn-outline btn-lg h-20 flex-col gap-2" disabled>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						class="h-6 w-6 stroke-current"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"
						></path>
					</svg>
					<span class="text-xs">Export</span>
				</button>
			</div>
		</div>
	</div>
</div>
