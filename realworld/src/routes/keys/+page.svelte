<script>
	import NewKeys from './NewKeys.svelte';

	/** @type {import('./$types').ActionData} */
	export let form;

	export let data;
</script>

<div>
	<div class="editor-page">
        <div class="container page">
            <h1>Add new Environment</h1>
        </div>
    </div>
	<NewKeys
		authkeys={{
			role_id: '',
			external_id: ''
		}}
		errors={form?.errors}
	/>

	<div class="container">
		<div>
			<h2>Existing Environments</h2>
		</div>
		{#each data.user_keys as user_key (user_key.id)}
			<div class="row">
				<div class="col-xs-12 col-md-10 offset-md-1">
					<a href='keys/{user_key.id}' class="preview-link">{user_key.role_id}</a>
				</div>
			</div>
		{/each}
	</div>
</div>