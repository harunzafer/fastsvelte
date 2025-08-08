<script lang="ts">
	let { children } = $props();
</script>

<div class="grid grid-cols-12 overflow-auto sm:h-screen">
	<div
		class="relative hidden bg-[#FFE9D1] lg:col-span-7 lg:block xl:col-span-8 2xl:col-span-9 dark:bg-[#14181c]"
	>
		<div class="absolute inset-0 flex items-center justify-center">
			<img src="/images/auth/auth-hero.png" class="object-cover" alt="Authentication hero" />
		</div>
		<div class="animate-bounce-2 absolute bottom-[15%] right-[20%]">
			<div class="card bg-base-100/80 w-64 backdrop-blur-lg">
				<div class="card-body p-5">
					<div class="flex flex-col items-center justify-center">
						<div class="mask mask-squircle overflow-hidden">
							<img
								src="/images/landing/testimonial-avatar-1.jpg"
								class="bg-base-200 size-14"
								alt=""
							/>
						</div>
						<div class="mt-3 flex items-center justify-center gap-0.5">
							<span class="iconify lucide--star size-4 text-orange-600" />
							<span class="iconify lucide--star size-4 text-orange-600" />
							<span class="iconify lucide--star size-4 text-orange-600" />
							<span class="iconify lucide--star size-4 text-orange-600" />
							<span class="iconify lucide--star size-4 text-orange-600" />
						</div>
						<p class="mt-1 text-lg font-medium">Pouya Saadeghi</p>
						<p class="text-base-content/60 text-sm">Creator of daisyUI</p>
					</div>
					<p class="mt-2 text-center text-sm">
						This is the ultimate admin dashboard for any React project
					</p>
				</div>
			</div>
		</div>
	</div>
	<div class="col-span-12 lg:col-span-5 xl:col-span-4 2xl:col-span-3">{@render children()}</div>
</div>
