<script>
    import { onMount } from 'svelte';

    const apiUrl = process.env.API_URL || 'http://localhost:8000';
    
    let data = [];
  
    onMount(async () => {
      const response = await fetch(`${apiUrl}/api/users`);
      data = await response.json();
    });
  </script>
  
  <h1>My Data</h1>
  <ul>
    {#each data as item}
      <li>{item.name}</li>
    {/each}
  </ul>