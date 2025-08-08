<script lang="ts">
	// Mock data - replace with real API calls
	let stats = $state({
		totalUsers: 1247,
		activeUsers: 892,
		totalNotes: 5642,
		monthlyRevenue: 12450
	});

	let recentUsers = $state([
		{
			id: 1,
			name: 'John Doe',
			email: 'john@example.com',
			status: 'active',
			joinedAt: '2025-01-15'
		},
		{
			id: 2,
			name: 'Jane Smith',
			email: 'jane@example.com',
			status: 'active',
			joinedAt: '2025-01-14'
		},
		{
			id: 3,
			name: 'Bob Johnson',
			email: 'bob@example.com',
			status: 'inactive',
			joinedAt: '2025-01-13'
		},
		{
			id: 4,
			name: 'Alice Brown',
			email: 'alice@example.com',
			status: 'active',
			joinedAt: '2025-01-12'
		}
	]);

	let recentActivity = $state([
		{ type: 'user_signup', message: 'New user registered: john@example.com', time: '2 min ago' },
		{ type: 'note_created', message: 'Note created by jane@example.com', time: '5 min ago' },
		{ type: 'user_login', message: 'User logged in: bob@example.com', time: '12 min ago' },
		{ type: 'ai_processed', message: 'AI processing completed for note #542', time: '18 min ago' }
	]);

	function getActivityIcon(type: string) {
		switch (type) {
			case 'user_signup':
				return '👤';
			case 'note_created':
				return '📝';
			case 'user_login':
				return '🔑';
			case 'ai_processed':
				return '🤖';
			default:
				return '📋';
		}
	}

	function getStatusBadge(status: string) {
		return status === 'active' ? 'badge-success' : 'badge-warning';
	}
</script>

<svelte:head>
	<title>Admin Dashboard - FastSvelte</title>
</svelte:head>

<!-- Page Header -->
<div class="mb-8">
	<h1 class="text-3xl font-bold">System Administration</h1>
	<p class="text-base-content/60 mt-2">
		Manage users, monitor system health, and oversee operations.
	</p>
</div>

<!-- System Status Alert -->
<div class="alert alert-info mb-6">
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		class="h-6 w-6 shrink-0 stroke-current"
	>
		<path
			stroke-linecap="round"
			stroke-linejoin="round"
			stroke-width="2"
			d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
		></path>
	</svg>
	<span>System maintenance scheduled for tonight at 2:00 AM UTC</span>
</div>

<!-- Stats Cards -->
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
					d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
				></path>
			</svg>
		</div>
		<div class="stat-title">Total Users</div>
		<div class="stat-value text-primary">{stats.totalUsers.toLocaleString()}</div>
		<div class="stat-desc">↗︎ 12% more than last month</div>
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
					d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"
				></path>
			</svg>
		</div>
		<div class="stat-title">Active Users</div>
		<div class="stat-value text-secondary">{stats.activeUsers.toLocaleString()}</div>
		<div class="stat-desc">↗︎ 8% more than last month</div>
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
					d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
				></path>
			</svg>
		</div>
		<div class="stat-title">Total Notes</div>
		<div class="stat-value text-accent">{stats.totalNotes.toLocaleString()}</div>
		<div class="stat-desc">↗︎ 22% more than last month</div>
	</div>

	<div class="stat">
		<div class="stat-figure text-success">
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
					d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
				></path>
			</svg>
		</div>
		<div class="stat-title">Monthly Revenue</div>
		<div class="stat-value text-success">${(stats.monthlyRevenue / 100).toFixed(0)}</div>
		<div class="stat-desc">↗︎ 15% more than last month</div>
	</div>
</div>

<!-- Main Content Grid -->
<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
	<!-- Recent Users Card -->
	<div class="card bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Recent Users</h2>

			<div class="overflow-x-auto">
				<table class="table-zebra table">
					<thead>
						<tr>
							<th>Name</th>
							<th>Email</th>
							<th>Status</th>
							<th>Joined</th>
						</tr>
					</thead>
					<tbody>
						{#each recentUsers as user}
							<tr>
								<td>
									<div class="flex items-center gap-3">
										<div class="avatar placeholder">
											<div class="bg-neutral text-neutral-content w-8 rounded-full">
												<span class="text-xs"
													>{user.name
														.split(' ')
														.map((n) => n[0])
														.join('')}</span
												>
											</div>
										</div>
										<div class="font-medium">{user.name}</div>
									</div>
								</td>
								<td class="text-sm opacity-70">{user.email}</td>
								<td>
									<span class="badge {getStatusBadge(user.status)} badge-sm">
										{user.status}
									</span>
								</td>
								<td class="text-sm opacity-70">{user.joinedAt}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<div class="card-actions justify-end">
				<button class="btn btn-primary btn-sm">View All Users</button>
			</div>
		</div>
	</div>

	<!-- Recent Activity Card -->
	<div class="card bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Recent Activity</h2>

			<div class="space-y-4">
				{#each recentActivity as activity}
					<div class="flex items-start gap-3">
						<div class="text-2xl">{getActivityIcon(activity.type)}</div>
						<div class="flex-1">
							<p class="text-sm">{activity.message}</p>
							<p class="text-xs opacity-60">{activity.time}</p>
						</div>
					</div>
				{/each}
			</div>

			<div class="card-actions justify-end">
				<button class="btn btn-primary btn-sm">View All Activity</button>
			</div>
		</div>
	</div>
</div>

<!-- Quick Actions -->
<div class="mt-8">
	<h2 class="mb-4 text-2xl font-bold">Quick Actions</h2>
	<div class="grid grid-cols-2 gap-4 md:grid-cols-4">
		<button class="btn btn-outline btn-lg h-24 flex-col gap-2">
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
					d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
				></path>
			</svg>
			<span class="text-sm">Add User</span>
		</button>

		<button class="btn btn-outline btn-lg h-24 flex-col gap-2">
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
					d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
				></path>
			</svg>
			<span class="text-sm">Manage Notes</span>
		</button>

		<button class="btn btn-outline btn-lg h-24 flex-col gap-2">
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
					d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
				></path>
			</svg>
			<span class="text-sm">Analytics</span>
		</button>

		<button class="btn btn-outline btn-lg h-24 flex-col gap-2">
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
					d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
				></path>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
				></path>
			</svg>
			<span class="text-sm">Settings</span>
		</button>
	</div>
</div>
