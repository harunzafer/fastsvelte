<script lang="ts">
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import TopbarLanguageMenu from './TopbarLanguageMenu.svelte';
	import TopbarNotificationButton from './TopbarNotificationButton.svelte';
	import TopbarProfileMenu from './TopbarProfileMenu.svelte';
	import TopbarSearchButton from './TopbarSearchButton.svelte';
</script>

<div
	role="navigation"
	aria-label="Navbar"
	class="flex items-center justify-between px-3"
	id="layout-topbar"
>
	<div class="inline-flex items-center gap-3">
		<label
			class="btn btn-square btn-ghost btn-sm"
			aria-label="Leftmenu toggle"
			for="layout-sidebar-toggle-trigger"
		>
			<span class="iconify lucide--menu size-5"></span>
		</label>
		<!-- <TopbarSearchButton /> -->
	</div>
	<div class="inline-flex items-center gap-0.5">
		<!-- <TopbarLanguageMenu /> -->
		<ThemeToggle class="btn btn-sm btn-circle btn-ghost" />
		<!-- Advanced setting button. To enable this also enable the <Rightbar /> in src/routes/(protected)/+layout.svelte -->
		<!-- <label for="layout-rightbar-drawer" class="btn btn-circle btn-ghost btn-sm drawer-button">
			<span class="iconify lucide--settings-2 size-4.5"></span>
		</label> -->
		<!-- <TopbarNotificationButton /> -->
		<TopbarProfileMenu />
	</div>
</div>
