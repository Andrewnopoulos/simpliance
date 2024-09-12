<script>
	import Benchmark from './Benchmark.svelte';

	/** @type {import('./$types').ActionData} */
	export let form;

	export let data;
</script>

<Benchmark
	user_keys={data.user_keys}
	benchmark_list={data.benchmark_list}
	errors={form?.errors}
/>
