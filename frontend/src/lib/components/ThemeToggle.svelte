<script lang="ts" module>
	type IThemeToggleDropdown = {
		iconClass?: string;
		class?: string;
	};
</script>

<script lang="ts">
	import { useConfig } from '$lib/context/ConfigProvider.svelte';

	const { iconClass, ...props }: IThemeToggleDropdown = $props();

	const { toggleTheme } = useConfig();
</script>

<button
	class={`relative overflow-hidden ${props.class ?? ''}`}
	on:click={toggleTheme}
	aria-label="Toggle Theme"
>
	<span
		class={`iconify lucide--sun size-4.5 absolute -translate-y-4 opacity-0 transition-all duration-300 group-data-[theme=light]/html:translate-y-0 group-data-[theme=light]/html:opacity-100 ${iconClass ?? ''}`}
	></span>
	<span
		class={`iconify lucide--moon size-4.5 absolute translate-y-4 opacity-0 transition-all duration-300 group-data-[theme=dark]/html:translate-y-0 group-data-[theme=dark]/html:opacity-100 ${iconClass ?? ''}`}
	></span>
	<span
		class={`iconify lucide--palette size-4.5 absolute opacity-100 group-data-[theme=dark]/html:opacity-0 group-data-[theme=light]/html:opacity-0 ${iconClass ?? ''}`}
	></span>
</button>
