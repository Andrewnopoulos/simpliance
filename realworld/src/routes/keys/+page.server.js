import { error, fail, redirect } from '@sveltejs/kit';
import * as api from '$lib/api.js';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals }) {
	if (!locals.user) redirect(302, `/login`);

    const user_keys = await api.get(`auth-keys`, locals.user.token);

	return { user_keys };
}

/** @type {import('./$types').Actions} */
export const actions = {
    default: async ({ locals, request }) => {
        if (!locals.user) error(401);

        const data = await request.formData();

        const result = await api.post(
            'auth-keys',
            {
                role_id: data.get('role_id'),
                external_id: data.get('external_id')
            },
            locals.user.token
        );

        if (result.errors) return fail(400, result);

        redirect(303, `keys/${result.id}`)
    }
}