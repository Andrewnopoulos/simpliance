<script>
	import NewKeys from '../NewKeys.svelte';

	/** @type {import('./$types').PageData} */
	export let data;

	/** @type {import('./$types').ActionData} */
	export let form;
</script>

<NewKeys authkeys={data.keys} errors={form?.errors} />
