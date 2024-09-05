import { error, redirect } from '@sveltejs/kit';
import * as api from '$lib/api.js';

export async function load({ locals, params }) {
	if (!locals.user) redirect(302, `/login`);

	const keys = await api.get(`auth-keys/${params.slug}`, locals.user.token);

	return { keys };
}


/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ locals, params, request }) => {
		if (!locals.user) error(401);

		const data = await request.formData();

		const result = await api.put(
			`auth-keys/${params.slug}`,
            {
                role_id: data.get('role_id'),
                external_id: data.get('external_id')
            },
			locals.user.token
		);

		if (result.errors) error(400, result.errors);

		console.log(result);

		redirect(303, `${params.slug}`)
	}
};
