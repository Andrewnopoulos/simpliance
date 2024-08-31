<script>
    import ListErrors from '$lib/ListErrors.svelte';

    export let report;
    console.log(report);
    export let errors;
</script>

<div class="container page">
    <div class="row">
        <div class="col-md-10 offset-md-1 col-xs-12">
            <ListErrors {errors} />
            <h4>{report.benchmark}</h4>
            <p>{report.process_state}</p>
            <p>Started: {report.datetime_started}</p>
            {#if report.datetime_completed}
              <p>Completed: {report.datetime_completed}</p>
            {/if}
            <p>Started by: <a href="/profile/{report.user_id}">{report.user_id}</a></p>
            <p>Using auth keys: <a href="/keys/{report.auth_key_id}">{report.auth_key_id}</a></p>
        </div>
    </div>
</div>