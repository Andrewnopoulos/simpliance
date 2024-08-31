<script>
    import Report from './Report.svelte';
    /** @type {import('./$types').PageData} */
	export let data;
</script>

<div>

    <div class="editor-page">
        <div class="container page">
            <h1>Report Detail</h1>
        </div>
    </div>
    <Report
        report={data.report}
    />
</div>