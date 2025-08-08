<script lang="ts">
    // @ts-ignore
    import { page } from "$app/stores";
    import Logo from "$lib/components/Logo.svelte";
    import SidebarMenuItem from "$lib/components/admin-layout/SidebarMenuItem.svelte";
    import { getActivatedItemParentKeys } from "$lib/components/admin-layout/helpers";
    import SimpleBar from "simplebar";
    import "simplebar/dist/simplebar.min.css";
    import type { ISidebarMenuItem } from "../admin-layout/SidebarMenuItem.svelte";

    let { menuItems }: { menuItems: ISidebarMenuItem[] } = $props();

    let scrollRef: HTMLDivElement;

    let activatedParents = $derived(new Set(getActivatedItemParentKeys(menuItems, $page.url.pathname)));

    $effect(() => {
        new SimpleBar(scrollRef);
    });
</script>

<input class="hidden" id="layout-sidebar-toggle-trigger" type="checkbox" aria-label="Toggle layout sidebar" />

<div
    class="border-base-300/80 bg-base-100 sticky top-0 bottom-0 flex h-screen w-64 min-w-64 flex-col border-s border-e border-dashed">
    <div class="border-base-300 flex h-16 min-h-16 items-center gap-4 border-b border-dashed px-5">
        <a href="/dashboards/ecommerce">
            <Logo />
        </a>
        <hr class="border-base-300 h-6 border-e" />
        <p class="text-base-content/60 mt-0.5 text-lg font-medium">Design</p>
    </div>

    <div class="relative min-h-0 grow">
        <div bind:this={scrollRef} class="size-full">
            <div class="sidebar-menu mt-4 space-y-0.5 px-2.5 pb-4">
                {#each menuItems as item, index (index)}
                    <SidebarMenuItem {...item} activated={activatedParents} />
                {/each}
            </div>
        </div>
    </div>

    <div class="mt-2">
        <a href="/dashboards/ecommerce" target="_blank" class="group rounded-box relative mx-2.5 block gap-3">
            <div
                class="rounded-box absolute inset-0 bg-gradient-to-r from-transparent to-transparent transition-opacity duration-300 group-hover:opacity-0">
            </div>
            <div
                class="from-primary to-secondary rounded-box absolute inset-0 bg-gradient-to-r opacity-0 transition-opacity duration-300 group-hover:opacity-100">
            </div>

            <div class="relative flex h-10 items-center gap-3 px-3">
                <i
                    class="iconify lucide--monitor-dot text-primary size-4.5 transition-all duration-300 group-hover:text-white"
                ></i>
                <p
                    class="from-primary to-secondary bg-gradient-to-r bg-clip-text font-medium text-transparent transition-all duration-300 group-hover:text-white">
                    Dashboard
                </p>
                <i
                    class="iconify lucide--chevron-right text-secondary ms-auto size-4.5 transition-all duration-300 group-hover:text-white"
                ></i>
            </div>
        </a>
        <hr class="border-base-300 mt-2 border-dashed" />
        <a
            href="https://nexus.daisyui.com/docs/"
            target="_blank"
            class="bg-base-200/60 hover:bg-base-200 rounded-box m-2.5 mb-2 flex cursor-pointer items-center gap-3 px-3.5 py-2 transition-all">
            <span class="iconify lucide--book-open-text size-5"></span>
            <div class="grow -space-y-0.5">
                <p class="text-sm font-medium">Documentation</p>
                <p class="text-base-content/60 text-xs">Installations</p>
            </div>
            <span class="iconify lucide--external-link text-base-content/60 size-4" />
        </a>
    </div>
</div>

<label for="layout-sidebar-toggle-trigger" id="layout-sidebar-backdrop"></label>
