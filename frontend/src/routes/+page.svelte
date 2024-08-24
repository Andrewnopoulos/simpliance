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
      // console.log(data)
      // return data.access_token;
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
        // console.log(protectedData);
      } catch (error) {
        console.error('Failed to fetch protected data:', error);
        errorMessage = 'Failed to fetch protected data.';
      }
    }
  </script>
  
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form on:submit={handleLogin}>
        <input 
            type="username" 
            bind:value={username}
            class="input-field" 
            placeholder="Email" 
            required 
        />
        <input 
            type="password" 
            bind:value={password} 
            class="input-field" 
            placeholder="Password" 
            required 
        />
      
      <button class="login-button" type="submit">
        Login
      </button>
      
    </form>
      <a href="/" class="forgot-password">Forgot your password?</a>
    </div>
    {#if errorMessage}
        <p class="error">{errorMessage}</p>
    {/if}
  </div>
  
  
  <style>
    .login-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: var(--background-color);
    }
  
    .login-box {
      background-color: var(--box-background-color);
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      max-width: 350px;
      width: 100%;
    }
  
    h2 {
      margin-bottom: 1.5rem;
      color: var(--text-color);
      font-size: 1.75rem;
      text-align: center;
    }
  
    .input-field {
      width: 100%;
      padding: 0.5rem;
      margin: 0.75rem 0;
      border-radius: 4px;
      border: 1px solid var(--input-border-color);
      font-size: 0.95rem;
      background-color: var(--input-background-color);
      color: var(--input-text-color);
    }
  
    .input-field:focus {
      border-color: var(--input-border-focus-color);
      outline: none;
      background-color: var(--input-background-focus-color);
    }
  
    .login-button {
      width: 100%;
      padding: 0.6rem;
      margin-top: 1rem;
      background-color: var(--button-background-color);
      color: var(--button-text-color);
      border: none;
      border-radius: 4px;
      font-size: 1rem;
      cursor: pointer;
    }
  
    .login-button:hover {
      background-color: var(--button-hover-background-color);
    }
  
    .forgot-password {
      display: block;
      margin-top: 1rem;
      color: var(--forgot-password-color);
      font-size: 0.85rem;
      text-decoration: none;
      text-align: center;
    }
  
    .forgot-password:hover {
      color: var(--forgot-password-hover-color);
    }
  
    /* Light mode variables */
    :root {
      --background-color: #f4f4f4;
      --box-background-color: #ffffff;
      --text-color: #333333;
      --input-background-color: #f9f9f9;
      --input-border-color: #ccc;
      --input-text-color: #333333;
      --input-border-focus-color: #666;
      --input-background-focus-color: #ffffff;
      --button-background-color: #333333;
      --button-text-color: white;
      --button-hover-background-color: #555555;
      --forgot-password-color: #777;
      --forgot-password-hover-color: #333333;
    }
  
    /* Dark mode variables */
    @media (prefers-color-scheme: dark) {
      :root {
        --background-color: #121212;
        --box-background-color: #1e1e1e;
        --text-color: #f0f0f0;
        --input-background-color: #2c2c2c;
        --input-border-color: #444444;
        --input-text-color: #f0f0f0;
        --input-border-focus-color: #888888;
        --input-background-focus-color: #333333;
        --button-background-color: #444444;
        --button-text-color: white;
        --button-hover-background-color: #666666;
        --forgot-password-color: #999;
        --forgot-password-hover-color: #f0f0f0;
      }
    }
  </style>