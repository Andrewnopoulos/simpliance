<script>
	import { page } from '$app/stores';
	import ReportList from '$lib/ReportList/index.svelte';

	/** @type {import('./$types').PageData} */
	export let data;
</script>

<svelte:head>
	<title>CloudGuard Compliance | AWS Security Compliance Made Simple</title>
</svelte:head>

<div class="home-page">
	{#if !data.user}
		<div class="banner">
			<div class="container">
				<h1 class="logo-font">Simplified AWS Compliance</h1>
				<p>Continuous security compliance monitoring for your cloud infrastructure</p>
				<div class="text-center mt-4">
					<a href="/register" class="btn btn-lg btn-primary mr-3">Start Free Trial</a>
					<a href="/login" class="btn btn-lg btn-primary mr-3">Sign In</a>
				</div>
			</div>
		</div>

		<div class="container page">
			<div class="row">
				<div class="col-md-12 text-center mb-5">
					<h2>Comprehensive Framework Coverage</h2>
					<p class="text-muted">Supporting all major security and compliance standards</p>
				</div>
			</div>

			<div class="row mb-5">
				<div class="col-md-4">
					<div class="card h-100">
						<div class="card-body">
							<h3 class="card-title">Security Standards</h3>
							<ul class="list-unstyled">
								<li>✓ AWS Foundational Security</li>
								<li>✓ CIS Benchmarks</li>
								<li>✓ NIST Frameworks</li>
								<li>✓ FedRAMP</li>
							</ul>
						</div>
					</div>
				</div>
				<div class="col-md-4">
					<div class="card h-100">
						<div class="card-body">
							<h3 class="card-title">Industry Regulations</h3>
							<ul class="list-unstyled">
								<li>✓ HIPAA</li>
								<li>✓ PCI DSS</li>
								<li>✓ SOC 2</li>
								<li>✓ GDPR</li>
							</ul>
						</div>
					</div>
				</div>
				<div class="col-md-4">
					<div class="card h-100">
						<div class="card-body">
							<h3 class="card-title">Regional Standards</h3>
							<ul class="list-unstyled">
								<li>✓ ACSC Essential Eight</li>
								<li>✓ RBI Cyber Security</li>
								<li>✓ CISA Cyber Essentials</li>
								<li>✓ And more...</li>
							</ul>
						</div>
					</div>
				</div>
			</div>

			<div class="row features-section">
				<div class="col-md-12 text-center mb-4">
					<h2>Why Choose Us?</h2>
				</div>
				<div class="col-md-4 text-center">
					<i class="ion-clock" style="font-size: 3rem;"></i>
					<h3>Real-Time Monitoring</h3>
					<p>Continuous scanning of your AWS infrastructure against security benchmarks</p>
				</div>
				<div class="col-md-4 text-center">
					<i class="ion-arrow-graph-up-right" style="font-size: 3rem;"></i>
					<h3>Instant Insights</h3>
					<p>Clear visibility into your compliance status with actionable recommendations</p>
				</div>
				<div class="col-md-4 text-center">
					<i class="ion-checkmark-circled" style="font-size: 3rem;"></i>
					<h3>Easy Setup</h3>
					<p>Quick integration with your AWS environment - be compliant in minutes</p>
				</div>
			</div>
		</div>
	{:else}
		<div class="container page">
			<div class="row">
				<div class="col-md-12">
					<h2>Your Compliance Reports</h2>
					<ReportList reports={data.reports} />
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.banner {
		background: #5cb85c;
		color: #fff;
		padding: 2rem;
		margin-bottom: 2rem;
	}

	.banner h1 {
		text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
		font-weight: 700;
		text-align: center;
		font-size: 3.5rem;
		padding-bottom: 0.5rem;
	}

	.banner p {
		text-align: center;
		font-size: 1.5rem;
		font-weight: 300;
	}

	.features-section {
		margin-top: 3rem;
		padding-top: 3rem;
		border-top: 1px solid #e5e5e5;
	}

	.card {
		border-radius: 4px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		transition: transform 0.2s;
	}

	.card:hover {
		transform: translateY(-5px);
	}

	.card-title {
		color: #373a3c;
		font-size: 1.25rem;
		margin-bottom: 1rem;
	}

	.list-unstyled li {
		padding: 0.5rem 0;
		color: #55595c;
	}
</style>