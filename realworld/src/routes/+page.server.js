import * as api from '$lib/api';
import { page_size } from '$lib/constants';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, url }) {
	const tab = url.searchParams.get('tab') || 'all';
	const tag = url.searchParams.get('tag');
	const page = +(url.searchParams.get('page') ?? '1');

	let reports = [];
	let keys = [];

	if (locals.user)
	{
		reports = await api.get( 'reports', locals.user?.token);
		keys = await api.get(`auth-keys`, locals.user?.token);	
	}

	return {
		reports,
		keys
	};
}
