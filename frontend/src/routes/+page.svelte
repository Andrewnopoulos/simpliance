<script>
  import { onMount } from 'svelte';

  let username = '';
  let password = '';
  let isLoggedIn = false;
  let protectedData = null;
  let errorMessage = '';

  const apiUrl = process.env.API_URL || 'http://localhost:8000';

  onMount(() => {
    isLoggedIn = !!getAuthToken();
    if (isLoggedIn) {
      fetchProtectedData();
    }
  });

  async function handleLogin(event) {
    event.preventDefault();
    try {
      const token = await login(username, password);
      setAuthCookie(token);
      isLoggedIn = true;
      errorMessage = '';
      fetchProtectedData();
    } catch (error) {
      console.error('Login failed:', error);
      errorMessage = 'Login failed. Please try again.';
    }
  }

  function handleLogout() {
    logout();
    isLoggedIn = false;
    protectedData = null;
  }

  async function login(username, password) {

    const formData = new URLSearchParams();
    formData.append('grant_type', 'password');
    formData.append('username', username);
    formData.append('password', password);
    formData.append('scope', '');
    formData.append('client_id', 'string');
    formData.append('client_secret', 'string');

    console.log("username: ")
    console.log(username)
    console.log("password:")
    console.log(password)

    const response = await fetch(`${apiUrl}/api/security/token`, {
      method: 'POST',
      headers: {            
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    console.log(data)
    return data.access_token;
  }

  function setAuthCookie(token) {
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 7);
    document.cookie = `auth_token=${token}; expires=${expirationDate.toUTCString()}; path=/; SameSite=Strict; Secure`;
  }

  function getAuthToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'auth_token') {
        return value;
      }
    }
    return null;
  }

  function logout() {
    document.cookie = 'auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  }

  async function fetchProtectedData() {
    const token = getAuthToken();
    if (!token) {
      throw new Error('No auth token found');
    }

    try {
      const response = await fetch(`${apiUrl}/api/security/users/me/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      protectedData = await response.json();
      console.log(protectedData);
    } catch (error) {
      console.error('Failed to fetch protected data:', error);
      errorMessage = 'Failed to fetch protected data.';
    }
  }
</script>

<main>
  {#if !isLoggedIn}
    <h1>Login</h1>
    <form on:submit={handleLogin}>
      <div>
        <label for="username">Username:</label>
        <input id="username" bind:value={username} type="text" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input id="password" bind:value={password} type="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  {:else}
    <h1>Welcome, {username}!</h1>
    <button on:click={handleLogout}>Logout</button>
    
    {#if protectedData}
      <h2>Protected Data:</h2>
      <pre>{JSON.stringify(protectedData, null, 2)}</pre>
    {:else}
      <p>Loading protected data...</p>
    {/if}
  {/if}

  {#if errorMessage}
    <p class="error">{errorMessage}</p>
  {/if}
</main>

<style>
  main {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  form div {
    margin-bottom: 10px;
  }
  label {
    display: block;
    margin-bottom: 5px;
  }
  input {
    width: 100%;
    padding: 5px;
  }
  button {
    margin-top: 10px;
  }
  .error {
    color: red;
  }
</style>