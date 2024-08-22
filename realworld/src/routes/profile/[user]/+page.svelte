<script>
	import ReportList from '$lib/ReportList/index.svelte';

	/** @type {import('./$types').PageData} */
	export let data;
</script>

<ReportList reports={data.reports} />
