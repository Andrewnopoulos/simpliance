<script>
	import { page } from '$app/stores';
</script>

<nav class="navbar navbar-light">
	<div class="container">
		<a class="navbar-brand" href="/">Simple Compliance</a>
		<ul class="nav navbar-nav pull-xs-right">
			<li class="nav-item">
				<a class="nav-link" class:active={$page.url.pathname === '/'} href="/">Home</a>
			</li>

			{#if $page.data.user}
				<li class="nav-item">
					<a href="/reports" class="nav-link" class:active={$page.url.pathname === '/reports'}>
						<i class="ion-compose" />&nbsp;New Report
					</a>
				</li>

				<li class="nav-item">
					<a href="/keys" class="nav-link" class:active={$page.url.pathname === '/keys'}>
						<i class="ion-compose" />&nbsp;New Keys
					</a>
				</li>

				<li class="nav-item">
					<a href="/settings" class="nav-link" class:active={$page.url.pathname === '/settings'}>
						<i class="ion-gear-a" />&nbsp;Settings
					</a>
				</li>

				<li class="nav-item">
					<a href="/profile/{$page.data.user.user_id}" class="nav-link">
						{$page.data.user.user_id}
					</a>
				</li>
			{:else}
				<li class="nav-item">
					<a href="/login" class="nav-link" class:active={$page.url.pathname === '/login'}>
						Sign in
					</a>
				</li>

				<li class="nav-item">
					<a href="/register" class="nav-link" class:active={$page.url.pathname === '/register'}>
						Sign up
					</a>
				</li>
			{/if}
		</ul>
	</div>
</nav>
