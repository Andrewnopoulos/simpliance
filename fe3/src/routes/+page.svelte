<script>
    import { goto } from '$app/navigation';

    let username = '';
    let password = '';
    let error = '';
  
    async function handleLogin() {

      const formData = new URLSearchParams();
      formData.append('grant_type', 'password');
      formData.append('username', username);
      formData.append('password', password);
      formData.append('scope', '');
      formData.append('client_id', 'string');
      formData.append('client_secret', 'string');

      try {
        const response = await fetch('/api/security/token', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
            },
            body: formData
        });
  
        if (response.ok) {
          // Successful login
          console.log("success!!")
          goto('/dashboard'); // Redirect to dashboard or any other page
        } else {
          // Failed login
          const data = await response.json();
          error = data.detail || 'Login failed';
        }
      } catch (err) {
        console.error('Login error:', err);
        error = 'An error occurred. Please try again.';
      }
    }
</script>
  
<main>
    <h1>Login</h1>
    <form on:submit|preventDefault={handleLogin}>
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" bind:value={username} required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" bind:value={password} required>
      </div>
      <button type="submit">Login</button>
    </form>
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
    form {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .error {
      color: red;
    }
</style>