import { getNote } from '$lib/api/gen/notes';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
	try {
		const response = await getNote(parseInt(params.id));
		return {
			note: response.data
		};
	} catch (err) {
		console.error('Failed to load note:', err);
		throw error(404, 'Note not found');
	}
};
