<script>
    import ListErrors from '$lib/ListErrors.svelte';

    export let report;
    export let errors;

    const progressStates = {
        queued: { label: 'Queued', value: 33 },
        progress: { label: 'In Progress', value: 66 },
        done: { label: 'Completed', value: 100 }
    };
</script>

<style>
    .progress-bar {
        height: 20px;
        background-color: #f3f3f3;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 15px;
    }
    .progress-bar-inner {
        height: 100%;
        background-color: #4caf50;
        text-align: center;
        color: white;
        line-height: 20px;
        transition: width 0.3s ease-in-out;
    }
    .status {
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>

<div class="container page">
    <div class="row">
        <div class="col-md-10 offset-md-1 col-xs-12">
            <ListErrors {errors} />
            <h4>{report.benchmark}</h4>
            
            <div class="status">Status: {progressStates[report.process_state].label}</div>
            <div class="progress-bar">
                <div 
                    class="progress-bar-inner" 
                    style="width: {progressStates[report.process_state].value}%;"
                >
                    {progressStates[report.process_state].label}
                </div>
            </div>
            
            <p>Started: {report.datetime_started}</p>
            {#if report.datetime_completed}
                <p>Completed: {report.datetime_completed}</p>
            {/if}
            <p>Started by: <a href="/profile/{report.user_id}">{report.user_id}</a></p>
            <p>Using auth keys: <a href="/keys/{report.auth_key_id}">{report.auth_key_id}</a></p>
        </div>
    </div>
</div>