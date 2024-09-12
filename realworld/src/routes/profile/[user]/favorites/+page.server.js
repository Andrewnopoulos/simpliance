import { get_reports } from '../get_info';

/** @type {import('./$types').PageServerLoad} */
export async function load(event) {
	const { reports } = await get_reports(event);
	return { reports };
}
