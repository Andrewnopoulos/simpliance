<script>
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';

	/** @type {import('./$types').PageData} */
	export let data;
	$: ({ profile } = data);

	$: is_favorites = $page.route.id === '/profile/[user]/favorites';
</script>

<svelte:head>
	<title>{profile.name} • Conduit</title>
</svelte:head>

<div class="profile-page">
	<div class="user-info">
		<div class="container">
			<div class="row">
				<div class="col-xs-12 col-md-10 offset-md-1">
					<h4>{profile.name}</h4>
					{#if profile.email}
						<p>{profile.email}</p>
					{/if}

					{#if profile.name === data.user?.name}
						<a href="/settings" class="btn btn-sm btn-outline-secondary action-btn">
							<i class="ion-gear-a" />
							Edit Profile Settings
						</a>
					{:else if data.user}
						<form
							method="POST"
							action="/profile/@{data.name}?/toggleFollow"
							use:enhance={({ form }) => {
								// optimistic UI
								data.following = !data.following;

								const button = form.querySelector('button');
								button.disabled = true;

								return ({ result, update }) => {
									button.disabled = false;
									if (result.type === 'error') update();
								};
							}}
						>
							<input hidden type="checkbox" name="following" checked={data.following} />
							<button
								class="btn btn-sm action-btn"
								class:btn-secondary={data.following}
								class:btn-outline-secondary={!data.following}
							>
								<i class="ion-plus-round" />
								{data.following ? 'Unfollow' : 'Follow'}
								{data.name}
							</button>
						</form>
					{:else}
						<a href="/login">Sign in to follow</a>
					{/if}
				</div>
			</div>
		</div>
	</div>

	<div class="container">
		<div class="row">
			<div class="col-xs-12 col-md-10 offset-md-1">
				<div class="articles-toggle">
					<ul class="nav nav-pills outline-active">
						<li class="nav-item">
							<a
								href="/profile/@{data.name}"
								class="nav-link"
								class:active={!is_favorites}
							>
								Articles
							</a>
						</li>

						<li class="nav-item">
							<a
								href="/profile/@{data.name}/favorites"
								class="nav-link"
								class:active={is_favorites}
							>
								Favorites
							</a>
						</li>
					</ul>
				</div>

				<slot />
			</div>
		</div>
	</div>
</div>
