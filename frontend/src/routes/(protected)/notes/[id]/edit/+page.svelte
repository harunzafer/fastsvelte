<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { updateNote, organizeNote } from '$lib/api/gen/notes';
	import type { NoteResponse, UpdateNoteRequest } from '$lib/api/gen/model';
	import Alert from '$lib/components/Alert.svelte';

	// Get note data from page data
	let { data }: { data: { note: NoteResponse } } = $props();

	let note = $state<NoteResponse>(data.note);
	let editForm = $state({ title: note.title, content: note.content });
	let formErrors = $state<Record<string, string>>({});
	let submitting = $state(false);
	let organizing = $state(false);
	let hasUnsavedChanges = $state(false);
	let errorMessage = $state('');
	let showError = $state(false);
	let successMessage = $state('');
	let showSuccess = $state(false);

	// Track changes for unsaved warning
	$effect(() => {
		hasUnsavedChanges = editForm.title !== note.title || editForm.content !== note.content;
	});

	// Warn before leaving with unsaved changes
	onMount(() => {
		const handleBeforeUnload = (e: BeforeUnloadEvent) => {
			if (hasUnsavedChanges) {
				e.preventDefault();
				return '';
			}
		};

		window.addEventListener('beforeunload', handleBeforeUnload);
		return () => window.removeEventListener('beforeunload', handleBeforeUnload);
	});

	async function handleSave() {
		if (!validateForm()) return;

		submitting = true;
		try {
			const response = await updateNote(note.id, editForm as UpdateNoteRequest);
			note = response.data;
			successMessage = 'Note updated successfully';
			showSuccess = true;
		} catch (error) {
			console.error('Failed to update note:', error);
			formErrors.submit = 'Failed to update note. Please try again.';
		} finally {
			submitting = false;
		}
	}

	async function handleOrganize() {
		organizing = true;
		try {
			const response = await organizeNote(note.id);
			note = response.data;
			editForm = { title: note.title, content: note.content };
			successMessage = 'Note organized successfully with AI';
			showSuccess = true;
		} catch (error) {
			// Handle specific error types
			if (
				(error as any).response?.status === 403 &&
				(error as any).response?.data?.code === 'QUOTA_EXCEEDED'
			) {
				const feature = (error as any).response.data.details?.feature_key;
				if (feature === 'token_limit') {
					errorMessage =
						'Your current plan has reached the AI processing limit. Please upgrade your plan to continue using AI organization features.';
				} else {
					errorMessage =
						'Your current plan does not support this feature. Please upgrade your plan to continue.';
				}
			} else {
				errorMessage = 'Failed to organize note. Please try again later.';
			}
			showError = true;
		} finally {
			organizing = false;
		}
	}

	function validateForm(): boolean {
		formErrors = {};

		if (!editForm.title.trim()) {
			formErrors.title = 'Title is required';
		}
		if (!editForm.content.trim()) {
			formErrors.content = 'Content is required';
		}

		return Object.keys(formErrors).length === 0;
	}

	function handleBack() {
		if (hasUnsavedChanges) {
			if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
				goto('/notes');
			}
		} else {
			goto('/notes');
		}
	}

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString();
	}
</script>

<svelte:head>
	<title>Edit Note - {note.title} - FastSvelte</title>
</svelte:head>

<!-- Breadcrumb -->
<div class="breadcrumbs mb-6 text-sm">
	<ul>
		<li><a href="/notes" class="link">Notes</a></li>
		<li>Edit Note</li>
	</ul>
</div>

<!-- Page Header -->
<div class="mb-8 flex items-center justify-between">
	<div>
		<h1 class="text-3xl font-bold">Edit Note</h1>
		<p class="text-base-content/60 mt-2">
			Last updated {formatDate(note.updated_at)}
			{#if hasUnsavedChanges}
				<span class="text-warning"> • Unsaved changes</span>
			{/if}
		</p>
	</div>
	<div class="flex gap-2">
		<button class="btn btn-ghost" onclick={handleBack}>
			<span class="iconify lucide--arrow-left size-4"></span>
			Back to Notes
		</button>
	</div>
</div>

<!-- Alerts -->
<Alert type="error" message={errorMessage} bind:show={showError} autoDismiss={true} />
<Alert type="success" message={successMessage} bind:show={showSuccess} autoDismiss={true} />

<!-- Edit Form -->
<div class="grid gap-8 lg:grid-cols-3">
	<!-- Main Editor -->
	<div class="lg:col-span-2">
		<div class="card bg-base-100 shadow-sm">
			<div class="card-body">
				<div class="space-y-6">
					<div class="form-control w-full">
						<label class="label" for="title">
							<span class="label-text text-lg font-medium">Title</span>
						</label>
						<input
							id="title"
							type="text"
							class="input input-bordered input-lg w-full"
							class:input-error={formErrors.title}
							bind:value={editForm.title}
							placeholder="Enter note title"
						/>
						{#if formErrors.title}
							<div class="label">
								<span class="label-text-alt text-error">{formErrors.title}</span>
							</div>
						{/if}
					</div>

					<div class="form-control w-full">
						<label class="label" for="content">
							<span class="label-text text-lg font-medium">Content</span>
						</label>
						<textarea
							id="content"
							class="textarea textarea-bordered min-h-96 w-full"
							class:textarea-error={formErrors.content}
							bind:value={editForm.content}
							placeholder="Enter note content"
						></textarea>
						{#if formErrors.content}
							<div class="label">
								<span class="label-text-alt text-error">{formErrors.content}</span>
							</div>
						{/if}
					</div>

					{#if formErrors.submit}
						<div class="alert alert-error">
							<span>{formErrors.submit}</span>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>

	<!-- Sidebar -->
	<div class="lg:col-span-1">
		<div class="card bg-base-100 shadow-sm">
			<div class="card-body">
				<h3 class="card-title mb-4 text-lg">Actions</h3>

				<!-- Save Button -->
				<button
					class="btn btn-primary mb-4"
					class:loading={submitting}
					disabled={submitting || !hasUnsavedChanges}
					onclick={handleSave}
				>
					{#if submitting}
						Saving...
					{:else if hasUnsavedChanges}
						<span class="iconify lucide--save size-4"></span>
						Save Changes
					{:else}
						<span class="iconify lucide--check size-4"></span>
						Saved
					{/if}
				</button>

				<div class="divider my-4"></div>

				<!-- AI Organize Section -->
				<div class="space-y-4">
					<h4 class="font-medium">AI Organization</h4>
					<p class="text-base-content/70 text-sm">
						Use AI to automatically organize, improve, and structure your note content.
					</p>

					<button
						class="btn btn-outline w-full"
						class:loading={organizing}
						disabled={organizing || hasUnsavedChanges}
						onclick={handleOrganize}
						title={hasUnsavedChanges
							? 'Save changes first before organizing'
							: 'AI Organize & Improve'}
					>
						{#if organizing}
							Organizing...
						{:else}
							<span class="iconify lucide--sparkles size-4"></span>
							AI Organize & Improve
						{/if}
					</button>

					{#if hasUnsavedChanges}
						<p class="text-warning text-xs">Save your changes first before using AI organization</p>
					{/if}
				</div>

				<div class="divider my-4"></div>

				<!-- Note Info -->
				<div class="space-y-2 text-sm">
					<div class="flex justify-between">
						<span class="text-base-content/60">Created:</span>
						<span>{formatDate(note.created_at)}</span>
					</div>
					<div class="flex justify-between">
						<span class="text-base-content/60">Updated:</span>
						<span>{formatDate(note.updated_at)}</span>
					</div>
					<div class="flex justify-between">
						<span class="text-base-content/60">ID:</span>
						<span class="font-mono text-xs">{note.id}</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
