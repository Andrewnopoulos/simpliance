import * as api from '$lib/api.js';
import { get_reports } from './get_info';

export async function load({ locals, params }) {
	// const { profile } = await api.get(`users/${params.user}`, locals.user?.token);
	const profile = await api.get(`users/${params.user}`, locals.user?.token);
	const { reports } = await get_reports({locals});

	return {
		profile,
		reports
	};
}
