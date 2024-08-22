import * as api from '$lib/api.js';
import { page_size } from '$lib/constants.js';

export async function get_reports({ params, locals }) {

	const reports = await api.get( 'reports', locals.user.token);

	return {
		reports
	};
}
