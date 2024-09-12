import { fail, redirect } from '@sveltejs/kit';
import * as api from '$lib/api.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ parent }) {
	const { user } = await parent();
	if (user) redirect(307, '/');
}

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();

		const user = {
			name: data.get('username'),
			email: data.get('email'),
			password: data.get('password')
		};

		const body = await api.post('users/register', user);

		if (body.errors) {
			return fail(401, body);
		}

		cookies.set('jwt', body.access_token, { path: '/' });

		redirect(307, '/');
	}
};
