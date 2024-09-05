<script>
    import ListErrors from '$lib/ListErrors.svelte';

    import { fade } from 'svelte/transition';
    import { cubicOut } from 'svelte/easing';
  
    export let report;
    export let errors;
  
    $: progress = report.process_state === 'queued' ? 0 : 
                  report.process_state === 'progress' ? 50 :
                  100;
  </script>
  
  <style>
    .container {
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem;
    }
  
    .report-card {
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      padding: 2rem;
      margin-bottom: 2rem;
    }
  
    .report-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
  
    h4 {
      margin: 0;
    }
  
    .progress-bar {
      height: 20px;
      background-color: #f0f0f0;
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 1rem;
    }
  
    .progress {
      height: 100%;
      background-color: #007bff;
      transition: width 0.5s ease-in-out;
    }
  
    .report-details {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-gap: 1rem;
    }
  
    .report-details p {
      margin: 0;
    }
  
    .report-details a {
      color: #007bff;
      text-decoration: none;
    }
  
    .report-details a:hover {
      text-decoration: underline;
    }
  </style>
  
  <div class="container">
    <div class="report-card" in:fade={{ duration: 300, easing: cubicOut }}>
      <div class="report-header">
        <h4>{report.benchmark}</h4>
        <p>{report.process_state}</p>
      </div>
      <div class="progress-bar">
        <div class="progress" style="width: {progress}%;"></div>
      </div>
      <div class="report-details">
        <p>Started: {report.datetime_started}</p>
        {#if report.datetime_completed}
          <p>Completed: {report.datetime_completed} - <a href="/reports/{report.id}/content">View Report</a></p>
        {/if}
        <p>Started by: <a href="/profile/{report.user_id}">{report.user_id}</a></p>
        <p>Using auth keys: <a href="/keys/{report.auth_key_id}">{report.auth_key_id}</a></p>
      </div>
      <ListErrors {errors} />
    </div>
  </div>