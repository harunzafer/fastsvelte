import { getNote, listNotes } from '$lib/api/gen/notes';
import { getPing } from '$lib/api/gen/ping';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ url }) => {
	await listNotes();
};
