/** @type {import('./$types').LayoutServerLoad} */
export function load({ locals }) {
	console.log('locals')
	console.log(locals)
	return {
		user: locals.user && {
			username: locals.user.sub,
			token: locals.user.token,
			expiration: locals.user.exp
		}
	};
}
