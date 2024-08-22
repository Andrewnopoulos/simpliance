import * as api from '$lib/api.js';

export async function load({ locals, params }) {
	// const { profile } = await api.get(`users/${params.user}`, locals.user?.token);
	const profile = await api.get(`users/${params.user}`, locals.user?.token);

	// console.log(profile)

	return {
		profile
	};
}
