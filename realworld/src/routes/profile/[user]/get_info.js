import * as api from '$lib/api.js';
import { page_size } from '$lib/constants.js';

export async function get_reports({ params, locals }) {

	const reports = await api.get( 'reports', locals.user.token);

	return {
		reports
	};
}

/*export async function get_user_details({ locals }) {
	const user_data = await api.get( `users/${locals.user.user_id}`, locals.user.token);

	return { user_data };
}*/