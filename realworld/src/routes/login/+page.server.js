import { fail, redirect } from '@sveltejs/kit';
import * as api from '$lib/api.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals }) {
	if (locals.user) redirect(307, '/');
}

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();

		console.log(data)

		const formData = new URLSearchParams();
		formData.append('grant_type', 'password');
		formData.append('username', data.get('email'));
		formData.append('password', data.get('password'));
		formData.append('scope', '');
		formData.append('client_id', 'string');
		formData.append('client_secret', 'string');

		const body = await api.postForm('auth/login', formData);

		if (body.errors) {
			return fail(401, body);
		}

		cookies.set('jwt', body.access_token, { path: '/' });

		redirect(307, '/');
	}
};
