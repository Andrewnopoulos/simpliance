<script>
    import { goto } from '$app/navigation';
    import { isLoggedIn } from '../authStore.js'; // Create this file to export the store

  
    let email = '';
    let password = '';
    let confirmPassword = '';
    let isRegistering = false;
    let errorMessage = '';

    const apiUrl = process.env.API_URL || 'http://localhost:8000';

    async function login(email, password) {

        const formData = new URLSearchParams();
        formData.append('grant_type', 'password');
        formData.append('username', email);
        formData.append('password', password);
        formData.append('scope', '');
        formData.append('client_id', 'string');
        formData.append('client_secret', 'string');

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
        isLoggedIn.set(true);
        return data.access_token;
    }

    async function register(email, password) {
        const response = await fetch(`${apiUrl}/api/security/users/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        return data.access_token;
    }
  
    async function handleSubmit(event) {
      event.preventDefault();
      errorMessage = '';
  
      if (isRegistering && password !== confirmPassword) {
        errorMessage = 'Passwords do not match.';
        return;
      }

      try {
        if (isRegistering) {
            await register(email, password);
        }

        let access_token = await login(email, password);
        setAuthCookie(access_token);
        goto('/dashboard');

      } catch (error) {
        console.error('Authentication error:', error);
        errorMessage = isRegistering ? 'Registration failed.' : 'Login failed.';
      }
    }
  
    function setAuthCookie(token) {
      const expirationDate = new Date();
      expirationDate.setDate(expirationDate.getDate() + 7);
      document.cookie = `auth_token=${token}; expires=${expirationDate.toUTCString()}; path=/; SameSite=Strict; Secure`;
    }
  
    function toggleMode() {
      isRegistering = !isRegistering;
      errorMessage = '';
    }
  </script>
  
  <svelte:head>
    <title>{isRegistering ? 'Register' : 'Login'}</title>
  </svelte:head>
  
  <main>
    <h1>{isRegistering ? 'Register' : 'Login'}</h1>
  
    <form on:submit={handleSubmit}>
      <div>
        <label for="email">Email:</label>
        <input id="email" bind:value={email} type="text" required>
      </div>
  
      <div>
        <label for="password">Password:</label>
        <input id="password" bind:value={password} type="password" required>
      </div>
  
      {#if isRegistering}
        <div>
          <label for="confirmPassword">Confirm Password:</label>
          <input id="confirmPassword" bind:value={confirmPassword} type="password" required>
        </div>
      {/if}
  
      <button type="submit">{isRegistering ? 'Register' : 'Login'}</button>
    </form>
  
    <p>
      {isRegistering ? 'Already have an account?' : "Don't have an account?"}
      <button on:click={toggleMode}>{isRegistering ? 'Login' : 'Register'}</button>
    </p>
  
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
  </main>
<!--   
  <style>
    main {
      max-width: 300px;
      margin: 0 auto;
      padding: 20px;
    }
  
    form {
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
  
    label {
      display: block;
      margin-bottom: 5px;
    }
  
    input {
      width: 100%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  
    button {
      padding: 10px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #0056b3;
    }
  
    .error {
      color: red;
      margin-top: 10px;
    }
  </style> -->