<script>
	import { enhance } from '$app/forms';
	import ListErrors from '$lib/ListErrors.svelte';

	export let authkeys;
	export let errors;

	let isEditing = false;

	// Add this function
	function toggleEditing() {
		isEditing = !isEditing;
	}
</script>

<div class="editor-page">
	<div class="container page">
		<div class="row">
			<div class="col-md-10 offset-md-1 col-xs-12">
				<ListErrors {errors} />
				{#if isEditing}
				<form use:enhance method="POST">
					<fieldset class="form-group">
						<p>
							Role ID
						</p>
						<input
							name="role_id"
							class="form-control"
							placeholder="AWS Role ID"
							value={authkeys.role_id}
						/>
					</fieldset>

					<fieldset class="form-group">
						<p>
							External ID
						</p>
						<input
							name="external_id"
							class="form-control"
							placeholder="External ID"
							value={authkeys.external_id}
						/>
					</fieldset>

					<button class="btn btn-lg pull-xs-right btn-primary"
					>Add Authkeys</button>
				</form>
				{:else}
				<fieldset class="form-group">
					<p>
						Role ID
					</p>
					<input
						disabled
						class="form-control"
						value={authkeys.role_id}
					/>
				</fieldset>

				<fieldset class="form-group">
					<p>
						External ID
					</p>
					<input
						disabled
						class="form-control"
						value={authkeys.external_id}
					/>
				</fieldset>
				<button
					class="btn btn-lg pull-xs-right btn-primary"
					on:click={toggleEditing}
					>
					Edit Authkeys
				</button>
				{/if}
			</div>
		</div>
	</div>
</div>

<style>
</style>
