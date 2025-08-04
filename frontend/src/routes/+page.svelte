<script lang="ts">
	import { getPing } from '$lib/api/gen/ping'; // adjust if needed
	import { onMount } from 'svelte';

	let result: string = 'loading...';

	onMount(async () => {
	console.log('🚀 About to call getPing()...');
	try {
		const res = await getPing(); // Orval-generated
		console.log('✅ Ping result:', res);
        result = res.data;
	} catch (err) {
		console.error('❌ Ping failed:', err);
	}
});

</script>

<h1>Ping Test</h1>
<p>{result}</p>
