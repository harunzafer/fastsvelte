<script lang="ts">
	// @ts-ignore
	import { afterNavigate } from '$app/navigation';
	// @ts-ignore
	import { page } from '$app/state';
	import Logo from '$lib/components/Logo.svelte';
	import { useConfig } from '$lib/context/ConfigProvider.svelte';
	import SimpleBar from 'simplebar';
	import 'simplebar/dist/simplebar.min.css';
	import SidebarMenuItem, { type ISidebarMenuItem } from './SidebarMenuItem.svelte';
	import { getActivatedItemParentKeys } from './helpers';

	let { menuItems }: { menuItems: ISidebarMenuItem[] } = $props();

	const { config } = useConfig();

	let activatedParents = $state(new Set(getActivatedItemParentKeys(menuItems, page.url.pathname)));
	let scrollRef: HTMLDivElement;
	let simplebar: SimpleBar | undefined;

	afterNavigate(() => {
		activatedParents = new Set(getActivatedItemParentKeys(menuItems, page.url.pathname));
		setTimeout(() => {
			const contentElement = simplebar?.getContentElement();
			const scrollElement = simplebar?.getScrollElement();
			if (contentElement) {
				const activatedItem = contentElement.querySelector<HTMLElement>('.active');
				const top = activatedItem?.getBoundingClientRect().top;
				if (activatedItem && scrollElement && top && top !== 0) {
					scrollElement.scrollTo({ top: scrollElement.scrollTop + top - 300, behavior: 'smooth' });
				}
			}
		}, 100);

		if (window.innerWidth <= 64 * 16) {
			const sidebarTrigger = document.querySelector<HTMLInputElement>(
				'#layout-sidebar-toggle-trigger'
			);
			if (sidebarTrigger) {
				sidebarTrigger.checked = false;
			}
		}
	});

	$effect(() => {
		simplebar = new SimpleBar(scrollRef);
	});
</script>

<input
	class="hidden"
	id="layout-sidebar-toggle-trigger"
	type="checkbox"
	aria-label="Toggle layout sidebar"
/>
<input
	type="checkbox"
	id="layout-sidebar-hover-trigger"
	class="hidden"
	aria-label="Dense layout sidebar"
/>
<div id="layout-sidebar-hover" class="bg-base-300 h-screen w-1"></div>
<div
	id="layout-sidebar"
	class="sidebar-menu flex flex-col"
	data-theme={$config.sidebarTheme === 'dark' && ['light', 'contrast'].includes($config.theme)
		? 'dark'
		: undefined}
>
	<div class="flex h-16 min-h-16 items-center justify-between gap-3 ps-5 pe-4">
		<a href="/">
			<Logo />
		</a>
		<!-- Toggle button to auto hide the sidebar. Disabled by default-->

		<!-- <label
			for="layout-sidebar-hover-trigger"
			title="Toggle sidebar hover"
			class="btn btn-circle btn-ghost btn-sm text-base-content/50 relative max-lg:hidden"
		>
			<span
				class="iconify lucide--panel-left-close absolute size-4.5 opacity-100 transition-all duration-300 group-has-[[id=layout-sidebar-hover-trigger]:checked]/html:opacity-0"
			/>
			<span
				class="iconify lucide--panel-left-dashed absolute size-4.5 opacity-0 transition-all duration-300 group-has-[[id=layout-sidebar-hover-trigger]:checked]/html:opacity-100"
			/>
		</label> -->
	</div>

	<div class="relative min-h-0 grow">
		<div bind:this={scrollRef} class="size-full">
			<div class="mb-3 space-y-0.5 px-2.5">
				{#each menuItems as item, index (index)}
					<SidebarMenuItem {...item} activated={activatedParents} />
				{/each}
			</div>
		</div>
		<div
			class="from-base-100/60 pointer-events-none absolute start-0 end-0 bottom-0 h-7 bg-linear-to-t to-transparent"
		></div>
	</div>
</div>

<label for="layout-sidebar-toggle-trigger" id="layout-sidebar-backdrop"></label>
