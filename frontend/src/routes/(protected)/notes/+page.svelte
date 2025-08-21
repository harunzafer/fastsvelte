<script lang="ts">
	import { onMount } from 'svelte';
	import { listNotes, createNote, updateNote, deleteNote, organizeNote } from '$lib/api/gen/notes';
	import type { NoteResponse, CreateNoteRequest, UpdateNoteRequest } from '$lib/api/gen/model';
	import Alert from '$lib/components/Alert.svelte';

	let notes = $state<NoteResponse[]>([]);
	let filteredNotes = $state<NoteResponse[]>([]);
	let loading = $state(true);
	let searchQuery = $state('');
	let showCreateModal = $state(false);
	let editingNote = $state<NoteResponse | null>(null);
	let deletingNote = $state<NoteResponse | null>(null);
	let organizing = $state<Record<number, boolean>>({});
	let errorMessage = $state('');
	let showError = $state(false);

	// Form states
	let createForm = $state({ title: '', content: '' });
	let editForm = $state({ title: '', content: '' });
	let formErrors = $state<Record<string, string>>({});
	let submitting = $state(false);

	// Reactive filtering
	$effect(() => {
		if (searchQuery.trim() === '') {
			filteredNotes = notes;
		} else {
			const query = searchQuery.toLowerCase();
			filteredNotes = notes.filter(
				(note) =>
					note.title.toLowerCase().includes(query) || note.content.toLowerCase().includes(query)
			);
		}
	});

	// Check for action parameter to show create modal
	onMount(() => {
		const url = new URL(window.location.href);
		if (url.searchParams.get('action') === 'new') {
			showCreateModal = true;
		}
	});

	onMount(loadNotes);

	async function loadNotes() {
		loading = true;
		try {
			const response = await listNotes();
			notes = response.data || [];
		} catch (error) {
			console.error('Failed to load notes:', error);
		} finally {
			loading = false;
		}
	}

	function resetCreateForm() {
		createForm = { title: '', content: '' };
		formErrors = {};
	}

	function openCreateModal() {
		resetCreateForm();
		showCreateModal = true;
	}

	function closeCreateModal() {
		showCreateModal = false;
		resetCreateForm();
	}

	async function handleCreate() {
		if (!validateForm(createForm)) return;

		submitting = true;
		try {
			await createNote(createForm as CreateNoteRequest);
			closeCreateModal();
			await loadNotes();
		} catch (error) {
			console.error('Failed to create note:', error);
			formErrors.submit = 'Failed to create note. Please try again.';
		} finally {
			submitting = false;
		}
	}

	function openEditModal(note: NoteResponse) {
		editingNote = note;
		editForm = { title: note.title, content: note.content };
		formErrors = {};
	}

	function closeEditModal() {
		editingNote = null;
		editForm = { title: '', content: '' };
		formErrors = {};
	}

	async function handleEdit() {
		if (!editingNote || !validateForm(editForm)) return;

		submitting = true;
		try {
			await updateNote(editingNote.id, editForm as UpdateNoteRequest);
			closeEditModal();
			await loadNotes();
		} catch (error) {
			console.error('Failed to update note:', error);
			formErrors.submit = 'Failed to update note. Please try again.';
		} finally {
			submitting = false;
		}
	}

	function confirmDelete(note: NoteResponse) {
		deletingNote = note;
	}

	function cancelDelete() {
		deletingNote = null;
	}

	async function handleDelete() {
		if (!deletingNote) return;

		try {
			await deleteNote(deletingNote.id);
			cancelDelete();
			await loadNotes();
		} catch (error) {
			console.error('Failed to delete note:', error);
		}
	}

	async function handleOrganize(noteId: number) {
		organizing[noteId] = true;
		try {
			const response = await organizeNote(noteId);
			// Update the note in the notes array with the organized content
			const noteIndex = notes.findIndex((note) => note.id === noteId);
			if (noteIndex !== -1) {
				notes[noteIndex] = response.data;
			}
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
			organizing[noteId] = false;
		}
	}

	function validateForm(form: { title: string; content: string }): boolean {
		formErrors = {};

		if (!form.title.trim()) {
			formErrors.title = 'Title is required';
		}
		if (!form.content.trim()) {
			formErrors.content = 'Content is required';
		}

		return Object.keys(formErrors).length === 0;
	}

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString();
	}

	function truncateContent(content: string, maxLength: number = 150): string {
		return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
	}
</script>

<svelte:head>
	<title>Notes - FastSvelte</title>
</svelte:head>

<!-- Page Header -->
<div class="mb-8 flex items-center justify-between">
	<div>
		<h1 class="text-3xl font-bold">Notes</h1>
		<p class="text-base-content/60 mt-2">Manage your notes with AI organization</p>
	</div>
	<button class="btn btn-primary" onclick={openCreateModal}>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			class="h-5 w-5 stroke-current"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 6v6m0 0v6m0-6h6m-6 0H6"
			></path>
		</svg>
		New Note
	</button>
</div>

<!-- Error Alert -->
<Alert type="error" message={errorMessage} bind:show={showError} autoDismiss={true} />

<!-- Search Bar -->
<div class="mb-6">
	<div class="relative">
		<input
			type="text"
			placeholder="Search notes..."
			class="input input-bordered w-full max-w-md pl-10"
			bind:value={searchQuery}
		/>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			class="absolute top-1/2 left-3 h-5 w-5 -translate-y-1/2 transform stroke-current opacity-60"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
			></path>
		</svg>
	</div>
</div>

<!-- Notes Grid -->
{#if loading}
	<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
		{#each Array(6) as _}
			<div class="card bg-base-100 shadow">
				<div class="card-body">
					<div class="skeleton mb-4 h-4 w-3/4"></div>
					<div class="skeleton mb-2 h-3 w-full"></div>
					<div class="skeleton mb-4 h-3 w-2/3"></div>
					<div class="skeleton h-8 w-full"></div>
				</div>
			</div>
		{/each}
	</div>
{:else if filteredNotes.length === 0}
	<div class="py-12 text-center">
		{#if searchQuery}
			<p class="text-base-content/60 mb-4">No notes found matching "{searchQuery}"</p>
			<button class="btn btn-ghost" onclick={() => (searchQuery = '')}>Clear search</button>
		{:else}
			<p class="text-base-content/60 mb-4">No notes yet. Create your first note to get started!</p>
			<button class="btn btn-primary" onclick={openCreateModal}>Create Note</button>
		{/if}
	</div>
{:else}
	<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
		{#each filteredNotes as note (note.id)}
			<div class="card bg-base-100 shadow transition-shadow hover:shadow-md">
				<div class="card-body">
					<h2 class="card-title text-lg">{note.title}</h2>
					<p class="text-base-content/70 text-sm leading-relaxed">
						{truncateContent(note.content)}
					</p>
					<p class="mt-2 text-xs opacity-60">Updated {formatDate(note.updated_at)}</p>

					<div class="card-actions mt-4 justify-end">
						<div class="flex gap-2">
							<button
								class="btn btn-sm btn-ghost"
								class:loading={organizing[note.id]}
								disabled={organizing[note.id]}
								onclick={() => handleOrganize(note.id)}
								title="AI Organize & Improve"
								aria-label="AI Organize & Improve"
							>
								{#if !organizing[note.id]}
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
											d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"
										></path>
									</svg>
								{/if}
							</button>
							<button
								class="btn btn-sm btn-ghost"
								onclick={() => openEditModal(note)}
								title="Edit"
								aria-label="Edit note"
							>
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
										d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
									></path>
								</svg>
							</button>
							<button
								class="btn btn-sm btn-ghost text-error"
								onclick={() => confirmDelete(note)}
								title="Delete"
								aria-label="Delete note"
							>
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
										d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
									></path>
								</svg>
							</button>
						</div>
					</div>
				</div>
			</div>
		{/each}
	</div>
{/if}

<!-- Create Note Modal -->
{#if showCreateModal}
	<div class="modal modal-open">
		<div class="modal-box">
			<h3 class="mb-4 text-lg font-bold">Create New Note</h3>

			<form
				onsubmit={(e) => {
					e.preventDefault();
					handleCreate();
				}}
			>
				<div class="form-control mb-4">
					<label class="label" for="create-title">
						<span class="label-text">Title</span>
					</label>
					<input
						id="create-title"
						type="text"
						class="input input-bordered"
						class:input-error={formErrors.title}
						bind:value={createForm.title}
						placeholder="Enter note title"
					/>
					{#if formErrors.title}
						<label class="label">
							<span class="label-text-alt text-error">{formErrors.title}</span>
						</label>
					{/if}
				</div>

				<div class="form-control mb-4">
					<label class="label" for="create-content">
						<span class="label-text">Content</span>
					</label>
					<textarea
						id="create-content"
						class="textarea textarea-bordered h-32"
						class:textarea-error={formErrors.content}
						bind:value={createForm.content}
						placeholder="Enter note content"
					></textarea>
					{#if formErrors.content}
						<label class="label">
							<span class="label-text-alt text-error">{formErrors.content}</span>
						</label>
					{/if}
				</div>

				{#if formErrors.submit}
					<div class="alert alert-error mb-4">
						<span>{formErrors.submit}</span>
					</div>
				{/if}

				<div class="modal-action">
					<button type="button" class="btn btn-ghost" onclick={closeCreateModal}>Cancel</button>
					<button
						type="submit"
						class="btn btn-primary"
						class:loading={submitting}
						disabled={submitting}
					>
						{submitting ? 'Creating...' : 'Create Note'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<!-- Edit Note Modal -->
{#if editingNote}
	<div class="modal modal-open">
		<div class="modal-box">
			<h3 class="mb-4 text-lg font-bold">Edit Note</h3>

			<form
				onsubmit={(e) => {
					e.preventDefault();
					handleEdit();
				}}
			>
				<div class="form-control mb-4">
					<label class="label" for="edit-title">
						<span class="label-text">Title</span>
					</label>
					<input
						id="edit-title"
						type="text"
						class="input input-bordered"
						class:input-error={formErrors.title}
						bind:value={editForm.title}
						placeholder="Enter note title"
					/>
					{#if formErrors.title}
						<label class="label">
							<span class="label-text-alt text-error">{formErrors.title}</span>
						</label>
					{/if}
				</div>

				<div class="form-control mb-4">
					<label class="label" for="edit-content">
						<span class="label-text">Content</span>
					</label>
					<textarea
						id="edit-content"
						class="textarea textarea-bordered h-32"
						class:textarea-error={formErrors.content}
						bind:value={editForm.content}
						placeholder="Enter note content"
					></textarea>
					{#if formErrors.content}
						<label class="label">
							<span class="label-text-alt text-error">{formErrors.content}</span>
						</label>
					{/if}
				</div>

				{#if formErrors.submit}
					<div class="alert alert-error mb-4">
						<span>{formErrors.submit}</span>
					</div>
				{/if}

				<div class="modal-action">
					<button type="button" class="btn btn-ghost" onclick={closeEditModal}>Cancel</button>
					<button
						type="submit"
						class="btn btn-primary"
						class:loading={submitting}
						disabled={submitting}
					>
						{submitting ? 'Updating...' : 'Update Note'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<!-- Delete Confirmation Modal -->
{#if deletingNote}
	<div class="modal modal-open">
		<div class="modal-box">
			<h3 class="mb-4 text-lg font-bold">Delete Note</h3>
			<p class="mb-4">
				Are you sure you want to delete "{deletingNote.title}"? This action cannot be undone.
			</p>

			<div class="modal-action">
				<button class="btn btn-ghost" onclick={cancelDelete}>Cancel</button>
				<button class="btn btn-error" onclick={handleDelete}>Delete</button>
			</div>
		</div>
	</div>
{/if}
