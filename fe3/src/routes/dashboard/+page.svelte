<script>
    import { goto } from '$app/navigation';
    import { setCookie, getCookie, eraseCookie } from '../../lib/cookiestore';
    import { onMount } from 'svelte';

    let user_data = '';
    let error = '';
    let savedValue = '';

    onMount(async () => {
      // Retrieve the cookie when the component mounts
      savedValue = getCookie('access_token') || '';
      console.log('saved value');
      console.log(savedValue)
      try {
        const response = await fetch('/api/security/users/me/', {
            method: 'GET',
            headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${savedValue}`
            }
        });

        if (response.ok) {
          // Successful login
          console.log("success!!")
          const data = await response.json();
          user_data = data;
          console.log(data)
        } else {
          // Failed login
          const data = await response.json();
          error = data || 'Login failed';
        }
      } catch (err) {
        console.error('Login error:', err);
        error = 'An error occurred. Please try again.';
      }
    });
</script>
  
<main>
    <h1>Logged In</h1>
    <div>
      ${user_data}
    </div>

    {#if error}
      <p class="error">{error}</p>
    {/if}
</main>
  
<style>
    main {
      max-width: 300px;
      margin: 0 auto;
      padding: 20px;
    }
    .error {
      color: red;
    }
</style>