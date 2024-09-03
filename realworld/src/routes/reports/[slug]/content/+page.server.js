import * as api from '$lib/api.js';


/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, params }) {
    if (!locals.user) redirect(302, `/login`);

	const report_content = await api.getHTML(`reports/${params.slug}/content`, locals.user?.token);

	return {
		report_content
	};
}
