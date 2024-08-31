<script>
	export let report;
</script>

<div class="report-preview">
	<div class="report-meta">
		<div class="info">
			<a class="author" href="/profile/{report.user_id}">{report.user_id}</a>
		</div>
	</div>

	<a href="/reports/{report.id}" class="preview-link">
		<h1>{report.benchmark}</h1>
		<p>{report.process_state}</p>
		<span class="date">{new Date(report.datetime_started).toDateString()}</span>
		<span class="date">{new Date(report.datetime_completed).toDateString()}</span>
		<p>{report.auth_key_id}</p>
	</a>
</div>
