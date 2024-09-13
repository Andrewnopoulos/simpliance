import { error, fail, redirect } from '@sveltejs/kit';
import * as api from '$lib/api.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals }) {
	if (!locals.user) redirect(302, `/login`);

	const benchmark_list = await api.get('benchmark')
	const user_keys = await api.get(`auth-keys`, locals.user.token);

	return { benchmark_list, user_keys }
}

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ locals, request }) => {
		if (!locals.user) error(401);

		const data = await request.formData();

		const result = await api.post(
			'benchmark',
			{
				auth_key_id: data.get('selected_key'),
				type: data.get('selected_benchmark')
			},
			locals.user.token
		);

		if (result.errors) return fail(400, result);

		redirect(303, `/reports/${result.report_id}`);
	}
};
