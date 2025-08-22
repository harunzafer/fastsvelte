<script lang="ts">
	import { onMount } from 'svelte';
	import { getUserSettings, setUserSetting } from '$lib/api/gen/settings';
	import type { UserSettingWithDefinition } from '$lib/api/gen/model';
	import { authStore } from '$lib/auth/auth.svelte.js';
	import { useConfig } from '$lib/context/ConfigProvider.svelte';
	import { mapUserThemeToConfig } from '$lib/utils/theme';

	let loading = $state(true);
	let saving = $state(false);
	let settings = $state<UserSettingWithDefinition[]>([]);
	let settingsMap = $state<Record<string, UserSettingWithDefinition>>({});
	let error = $state<string | null>(null);

	// Form values
	let theme = $state('light');
	let notificationsEnabled = $state(false);

	// Original values for comparison
	let originalTheme = $state('light');
	let originalNotificationsEnabled = $state(false);

	// Track if there are unsaved changes
	const hasChanges = $derived(
		theme !== originalTheme || notificationsEnabled !== originalNotificationsEnabled
	);

	// Theme configuration
	const { changeTheme } = useConfig();

	// Apply theme changes when settings are saved
	function applyThemeChange(newTheme: string) {
		const configTheme = mapUserThemeToConfig(newTheme);
		changeTheme(configTheme);
	}

	onMount(async () => {
		if (!authStore.user?.id) return;

		try {
			const response = await getUserSettings(authStore.user.id);
			settings = response.data;

			// Convert to map for easy access
			settingsMap = settings.reduce(
				(acc, setting) => {
					acc[setting.key] = setting;
					return acc;
				},
				{} as Record<string, UserSettingWithDefinition>
			);

			// Set form values from existing settings
			theme = settingsMap.theme?.value || 'light';
			notificationsEnabled = settingsMap.notifications_enabled?.value === 'true';

			// Store original values for comparison
			originalTheme = theme;
			originalNotificationsEnabled = notificationsEnabled;

			// Apply the initial theme from user settings
			applyThemeChange(theme);
		} catch (err) {
			console.error('Failed to load user settings:', err);
			error = 'Failed to load settings. Please try again.';
		} finally {
			loading = false;
		}
	});

	async function saveAllSettings() {
		if (!authStore.user?.id || saving) return;

		saving = true;
		error = null;

		try {
			// Save theme if changed
			if (theme !== originalTheme) {
				const themeResponse = await setUserSetting(authStore.user.id, {
					key: 'theme',
					value: theme
				});
				settingsMap.theme = themeResponse.data;
				originalTheme = theme;
				// Apply the theme change to the page
				applyThemeChange(theme);
			}

			// Save notifications if changed
			if (notificationsEnabled !== originalNotificationsEnabled) {
				const notifResponse = await setUserSetting(authStore.user.id, {
					key: 'notifications_enabled',
					value: notificationsEnabled.toString()
				});
				settingsMap.notifications_enabled = notifResponse.data;
				originalNotificationsEnabled = notificationsEnabled;
			}

			// Show success feedback briefly
			// TODO: Add toast notification
		} catch (err) {
			console.error('Failed to save settings:', err);
			error = 'Failed to save settings. Please try again.';
		} finally {
			saving = false;
		}
	}
</script>

<div class="container mx-auto max-w-4xl p-6">
	<!-- Page Header -->
	<div class="bg-primary/10 rounded-box relative mb-6 overflow-hidden p-6">
		<div class="flex justify-between">
			<div>
				<div class="flex items-center gap-1">
					<p class="text-base-content/80 text-sm">Settings</p>
					<span class="iconify lucide--chevron-right text-base-content/80 size-3.5"></span>
					<p class="text-sm">User Preferences</p>
				</div>
				<p class="text-primary mt-4 text-xl font-medium">My Settings</p>
				<p class="text-base-content/80">
					Configure your personal preferences and account settings.
				</p>
			</div>
		</div>
		<span
			class="iconify lucide--settings text-primary/5 absolute start-1/2 -bottom-12 size-44 -rotate-25"
		></span>
	</div>

	{#if error}
		<div class="alert alert-error mb-6">
			<span class="iconify lucide--alert-circle size-5"></span>
			<span>{error}</span>
		</div>
	{/if}

	{#if loading}
		<div class="flex justify-center py-12">
			<span class="loading loading-spinner loading-lg"></span>
		</div>
	{:else}
		<!-- Appearance Settings -->
		<div class="card bg-base-100 card-border mb-6">
			<div class="card-body">
				<div class="mb-6 flex items-center gap-2">
					<span class="iconify lucide--palette size-5"></span>
					<p class="text-lg font-medium">Appearance</p>
				</div>

				<div class="grid grid-cols-1 gap-5 xl:grid-cols-5">
					<div class="xl:col-span-2">
						<div class="flex items-center gap-2">
							<span class="iconify lucide--monitor size-4" />
							<p class="font-medium">Theme</p>
						</div>
						<p class="text-base-content/60 text-sm">Choose your preferred color theme</p>
					</div>
					<div class="xl:col-span-3">
						<div class="space-y-2">
							<select class="select w-full max-w-xs" bind:value={theme} disabled={saving}>
								<option value="light">Light</option>
								<option value="dark">Dark</option>
								<option value="auto">Auto (System)</option>
							</select>
							<p class="text-base-content/60 text-xs">
								Changes apply immediately across all your sessions
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Notification Settings -->
		<div class="card bg-base-100 card-border mb-6">
			<div class="card-body">
				<div class="mb-6 flex items-center gap-2">
					<span class="iconify lucide--bell size-5"></span>
					<p class="text-lg font-medium">Notifications</p>
				</div>

				<div class="grid grid-cols-1 gap-5 xl:grid-cols-5">
					<div class="xl:col-span-2">
						<div class="flex items-center gap-2">
							<span class="iconify lucide--mail size-4" />
							<p class="font-medium">Email Notifications</p>
						</div>
						<p class="text-base-content/60 text-sm">Receive important updates via email</p>
					</div>
					<div class="xl:col-span-3">
						<div class="space-y-2">
							<label class="flex cursor-pointer items-center gap-3">
								<input
									type="checkbox"
									class="toggle toggle-primary"
									bind:checked={notificationsEnabled}
									disabled={saving}
								/>
								<span class="font-medium">
									{notificationsEnabled ? 'Enabled' : 'Disabled'}
								</span>
							</label>
							<p class="text-base-content/60 text-xs">
								Get notified about important account updates, security alerts, and feature
								announcements
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Save Changes Button -->
		<div class="mb-6">
			<div class="flex justify-end">
				<button
					class="btn btn-primary"
					class:loading={saving}
					disabled={!hasChanges || saving}
					onclick={saveAllSettings}
				>
					{#if saving}
						<span class="loading loading-spinner loading-sm"></span>
						Saving...
					{:else}
						<span class="iconify lucide--save size-4"></span>
						Save Changes
					{/if}
				</button>
			</div>
		</div>
	{/if}
</div>
