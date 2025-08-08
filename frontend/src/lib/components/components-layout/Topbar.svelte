<script>
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
</script>

<div
	role="navigation"
	aria-label="Navbar"
	class="border-base-300/80 bg-base-100 sticky top-0 z-1 h-16 border-b border-dashed px-4 md:px-8 xl:px-12 2xl:px-20"
>
	<div class="flex h-full items-center justify-between px-0">
		<div class="flex items-center gap-5">
			<a
				href="/dashboards/ecommerce"
				class="text-base-content/70 hover:text-base-content transition-all"
			>
				Dashboard
			</a>
			<a href="/components" class="font-medium"> Components </a>
		</div>
		<div class="inline-flex items-center gap-3">
			<ThemeToggle class="btn btn-sm btn-circle btn-ghost" />
			<a
				href="https://daisyui.com/store/244268?aff=Db6q2"
				target="_blank"
				class="btn from-primary to-secondary group/purchase text-primary-content btn-sm max-sm:btn-square relative gap-2 border-0 bg-linear-to-r text-sm"
			>
				<span class="iconify lucide--shopping-cart size-4" />
				<span class="max-sm:hidden">Buy Now</span>
				<div
					class="from-primary to-secondary absolute inset-x-0 top-1 -z-1 h-8 bg-linear-to-r opacity-40 blur-md transition-all duration-500 group-hover/purchase:opacity-60 group-hover/purchase:blur-lg"
				></div>
			</a>
		</div>
	</div>
</div>
