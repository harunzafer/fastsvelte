<script lang="ts">
	import ConfigProvider from '$lib/context/ConfigProvider.svelte';
	import '$lib/styles/app.css';

	let { children } = $props();
</script>

<ConfigProvider>
	{@render children()}
</ConfigProvider>
