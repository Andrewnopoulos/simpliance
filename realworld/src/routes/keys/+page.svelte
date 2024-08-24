<script>
	import NewKeys from './NewKeys.svelte';

	/** @type {import('./$types').ActionData} */
	export let form;
</script>

<NewKeys
	authkeys={{
		role_id: '',
		external_id: ''
	}}
	errors={form?.errors}
/>
