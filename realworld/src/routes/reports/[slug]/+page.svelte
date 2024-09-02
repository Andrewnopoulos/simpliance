<script>
    import Report from './Report.svelte';
    import Report2 from './Report2.svelte';

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
    <Report2
        report={data.report}
    />
</div>