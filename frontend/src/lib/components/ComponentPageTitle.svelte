<script lang="ts">
    type IComponentPageTitle = {
        label?: string;
        title: string;
        description: string;
    };

    let { title, label, description }: IComponentPageTitle = $props();
</script>

<div class="flex flex-col items-center justify-center space-y-0.5">
    {#if label}
        <div
            class="text-base-content/80 border-base-300 flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs leading-none tracking-[0.2px]">
            <div class="status status-sm bg-base-content/30"></div>
            {label}
        </div>
    {/if}
    <p
        class="from-base-content to-base-content/75 bg-linear-to-b bg-clip-text pb-1 text-3xl font-bold tracking-tight text-transparent lg:text-4xl 2xl:text-5xl">
        {title}
    </p>
    <p class="text-base-content/80 max-w-lg text-center max-md:text-sm">
        {description}
    </p>
</div>
