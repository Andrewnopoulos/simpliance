<script>
	import NewKeys from '../NewKeys.svelte';

	/** @type {import('./$types').PageData} */
	export let data;

	/** @type {import('./$types').ActionData} */
	export let form;
</script>

<div>

    <div class="editor-page">
        <div class="container page">
            <h1>Edit Existing keys</h1>
        </div>
    </div>
    <NewKeys authkeys={data.keys} errors={form?.errors} />

</div>