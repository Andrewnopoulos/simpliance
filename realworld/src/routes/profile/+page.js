import { redirect } from '@sveltejs/kit';

export async function load({ parent }) {
	const { user } = await parent();
	console.log("user")
	console.log(user)
	redirect(307, user ? `/profile/@${user.username}` : '/login');
}
