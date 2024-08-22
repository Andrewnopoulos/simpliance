<script>
	import { page } from '$app/stores';
	import ReportPreview from './ReportPreview.svelte';

	export let reports;
</script>

{#if reports.length === 0}
	<div class="report-preview">No reports are here... yet.</div>
{:else}
	<div>
		{#each reports as report (report.slug)}
			<ReportPreview {report} user={$page.data.user} />
		{/each}
	</div>
{/if}
