import * as api from '$lib/api.js';
import { error, fail } from '@sveltejs/kit';

// /** @type {import('./$types').PageServerLoad} */
// export async function load(event) {
// 	const { reports } = await get_reports(event, 'author');
// 	return { reports };
// }

/** @type {import('./$types').Actions} */
export const actions = {
	toggleFollow: async ({ locals, params, request }) => {
		if (!locals.user) error(401);

		const data = await request.formData();
		const following = data.get('following') !== 'on';

		// const result = following
		// 	? await api.post(`profiles/${params.user}/follow`, null, locals.user.token)
		// 	: await api.del(`profiles/${params.user}/follow`, locals.user.token);

		// if (result.errors) {
		// 	return fail(422, result);
		// }
	}
};
