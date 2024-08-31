import * as api from '$lib/api.js';


/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, params }) {
    if (!locals.user) redirect(302, `/login`);

	const report = await api.get(`reports/${params.slug}`, locals.user?.token);

	return {
		report
	};
}
