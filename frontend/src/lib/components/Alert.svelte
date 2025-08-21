<script lang="ts">
	interface Props {
		type: 'error' | 'success' | 'warning' | 'info';
		message: string;
		show: boolean;
		dismissible?: boolean;
		onDismiss?: () => void;
		autoDismiss?: boolean;
		autoDismissDelay?: number;
	}

	let {
		type,
		message,
		show = $bindable(),
		dismissible = true,
		onDismiss,
		autoDismiss = false,
		autoDismissDelay = 5000
	}: Props = $props();

	// Auto-dismiss functionality
	$effect(() => {
		if (show && autoDismiss) {
			const timeout = setTimeout(() => {
				handleDismiss();
			}, autoDismissDelay);

			return () => clearTimeout(timeout);
		}
	});

	function handleDismiss() {
		show = false;
		onDismiss?.();
	}

	// Icon paths for each alert type
	const icons = {
		error: 'M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z',
		success: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
		warning:
			'M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z',
		info: 'M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853L14.25 14.25M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z'
	};
</script>

{#if show}
	<div class="alert alert-{type} mb-6">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			class="h-6 w-6 shrink-0 stroke-current"
		>
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={icons[type]}></path>
		</svg>
		<span>{message}</span>
		{#if dismissible}
			<button class="btn btn-sm btn-ghost" onclick={handleDismiss} aria-label="Close">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					class="h-4 w-4 stroke-current"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M6 18L18 6M6 6l12 12"
					></path>
				</svg>
			</button>
		{/if}
	</div>
{/if}
