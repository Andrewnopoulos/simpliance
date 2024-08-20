<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { isLoggedIn } from './authStore';

    let isLoading = true;
  
    onMount(async () => {
      await checkAuthStatus();
    });
  
    async function checkAuthStatus() {
      isLoading = true;
      const token = getAuthToken();
      if (token) {
        // Optionally, validate the token with your backend
        isLoggedIn.set(true);
      } else {
        isLoggedIn.set(false);
        if (window.location.pathname !== '/login') {
          console.log("token is missing?")
          console.log("going to login screen")
          // goto('/login');
        }
      }
      isLoading = false;
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
  
    function handleLogout() {
      // Implementation of logout function
      document.cookie = 'auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      isLoggedIn.set(false);
      goto('/login');
    }
  </script>
  
  {#if isLoading}
    <p>Loading...</p>
  {:else}
    {#if $isLoggedIn}
      <nav>
        <ul>
          <li><a href="/dashboard">Dashboard</a></li>
          <li><a href="/reports">Reports</a></li>
          <li><a href="/reports/new">New Report</a></li>
          <li><a href="/setup">Setup</a></li>
          <li><button on:click={handleLogout}>Logout</button></li>
        </ul>
      </nav>
    {/if}
  
    <main>
      <slot />
    </main>
  {/if}
  
  <style>
    nav {
      background-color: #f8f9fa;
      padding: 1rem;
    }
  
    ul {
      list-style-type: none;
      padding: 0;
      margin: 0;
      display: flex;
      justify-content: space-around;
    }
  
    li {
      display: inline;
    }
  
    a {
      text-decoration: none;
      color: #333;
      font-weight: bold;
    }
  
    button {
      background: none;
      border: none;
      cursor: pointer;
      font-weight: bold;
      color: #333;
    }
  
    main {
      padding: 2rem;
    }
  </style>