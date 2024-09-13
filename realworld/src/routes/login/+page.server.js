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

		console.log("Login response body");
		console.log(body);

		cookies.set('jwt', body.access_token, { path: '/', secure: false }); // TODO Change to secure once https implemented

		// response.set_cookie(
		// 	key="jwt",
		// 	value=token,
		// 	httponly=True,
		// 	secure=True,  # Set to False if not using HTTPS
		// 	samesite="strict",
		// 	max_age=1800,  # 30 minutes
		// 	domain="your-domain.com"  # Set this to your domain
		// )

		redirect(307, '/');
	}
};
