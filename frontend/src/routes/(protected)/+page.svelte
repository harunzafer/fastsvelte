<script lang="ts">
	import { authStore } from '$lib/auth/auth.svelte';

	// Mock data for user dashboard
	let userStats = $state({
		totalNotes: 42,
		thisMonth: 8,
		aiProcessed: 15
	});

	let recentNotes = $state([
		{
			id: 1,
			title: 'Project Meeting Notes',
			content: 'Discussed Q1 goals and milestones...',
			updated_at: '2025-01-15'
		},
		{
			id: 2,
			title: 'Research Ideas',
			content: 'New AI applications for content...',
			updated_at: '2025-01-14'
		},
		{
			id: 3,
			title: 'Daily Standup',
			content: 'Team updates and blockers...',
			updated_at: '2025-01-13'
		}
	]);
</script>

<svelte:head>
	<title>Dashboard - FastSvelte</title>
</svelte:head>

<!-- Page Header -->
<div class="mb-8">
	<h1 class="text-3xl font-bold">Welcome back, {authStore.user?.first_name}!</h1>
	<p class="text-base-content/60 mt-2">Here's what's happening with your notes.</p>
</div>

<!-- User Stats -->
<div class="stats stats-vertical lg:stats-horizontal mb-8 w-full shadow">
	<div class="stat">
		<div class="stat-figure text-primary">
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
		<div class="stat-title">Total Notes</div>
		<div class="stat-value text-primary">{userStats.totalNotes}</div>
		<div class="stat-desc">All time</div>
	</div>

	<div class="stat">
		<div class="stat-figure text-secondary">
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
		<div class="stat-title">This Month</div>
		<div class="stat-value text-secondary">{userStats.thisMonth}</div>
		<div class="stat-desc">New notes created</div>
	</div>

	<div class="stat">
		<div class="stat-figure text-accent">
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
		<div class="stat-title">AI Processed</div>
		<div class="stat-value text-accent">{userStats.aiProcessed}</div>
		<div class="stat-desc">Enhanced with AI</div>
	</div>
</div>

<!-- Recent Notes -->
<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
	<div class="card bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Recent Notes</h2>

			<div class="space-y-4">
				{#each recentNotes as note}
					<div class="border-primary border-l-4 pl-4">
						<h3 class="font-medium">{note.title}</h3>
						<p class="line-clamp-2 text-sm opacity-70">{note.content}</p>
						<p class="mt-1 text-xs opacity-50">{note.updated_at}</p>
					</div>
				{/each}
			</div>

			<div class="card-actions justify-end">
				<button class="btn btn-primary btn-sm">View All Notes</button>
			</div>
		</div>
	</div>

	<!-- Quick Actions -->
	<div class="card bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Quick Actions</h2>

			<div class="grid grid-cols-2 gap-4">
				<button class="btn btn-outline btn-lg h-20 flex-col gap-2">
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
				</button>

				<button class="btn btn-outline btn-lg h-20 flex-col gap-2">
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
					<span class="text-xs">Search</span>
				</button>

				<button class="btn btn-outline btn-lg h-20 flex-col gap-2">
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
					<span class="text-xs">AI Process</span>
				</button>

				<button class="btn btn-outline btn-lg h-20 flex-col gap-2">
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
					<span class="text-xs">Share</span>
				</button>
			</div>
		</div>
	</div>
</div>
