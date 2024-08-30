<script>
	import { enhance } from '$app/forms';
	import ListErrors from '$lib/ListErrors.svelte';

	export let user_keys;
	export let benchmark_list;
	export let errors;

	let selected_key;
	let selected_benchmark;

</script>

<div class="editor-page">
	<div class="container page">
		<div class="row">
			<div class="col-md-10 offset-md-1 col-xs-12">
				<ListErrors {errors} />

				<form use:enhance method="POST">
					<fieldset class="form-group">
						<p>
							Auth Keys
						</p>
						<select
							value={selected_key}
							>
							{#each user_keys as user_key}
							<option value={user_key.id}>
								{user_key.role_id}
							</option>
							{/each}
						</select>
					</fieldset>

					<fieldset class="form-group">
						<p>
							Benchmark
						</p>
						<select
							value={selected_benchmark}
							>
							{#each benchmark_list as benchmark}
							<option value={benchmark}>
								{benchmark}
							</option>
							{/each}
						</select>
					</fieldset>

					<button class="btn btn-lg pull-xs-right btn-primary">Run Benchmark</button>
				</form>
			</div>
		</div>
	</div>
</div>

<style>
</style>
