<script>
    import { onMount } from 'svelte';
  
    let username = '';
    let recentReports = [];
    let isLoading = true;
  
    onMount(async () => {
      // Fetch user data and recent reports
      try {
        const userData = await fetchUserData();
        username = userData.username;
        recentReports = await fetchRecentReports();
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        isLoading = false;
      }
    });
  
    async function fetchUserData() {
      // Implement API call to fetch user data
      // For now, we'll return mock data
      return { username: 'John Doe' };
    }
  
    async function fetchRecentReports() {
      // Implement API call to fetch recent reports
      // For now, we'll return mock data
      return [
        { id: 1, name: 'Report 1', date: '2023-08-15' },
        { id: 2, name: 'Report 2', date: '2023-08-14' },
        { id: 3, name: 'Report 3', date: '2023-08-13' },
      ];
    }
  </script>
  
  <svelte:head>
    <title>Dashboard</title>
  </svelte:head>
  
  <h1>Welcome to your Dashboard, {username}!</h1>
  
  {#if isLoading}
    <p>Loading dashboard data...</p>
  {:else}
    <section>
      <h2>Recent Reports</h2>
      {#if recentReports.length > 0}
        <ul>
          {#each recentReports as report}
            <li>
              <a href="/reports/{report.id}">{report.name}</a> - {report.date}
            </li>
          {/each}
        </ul>
      {:else}
        <p>No recent reports found.</p>
      {/if}
    </section>
  
    <section>
      <h2>Quick Actions</h2>
      <a href="/new-report" class="button">Create New Report</a>
      <a href="/setup" class="button">Update API Keys</a>
    </section>
  {/if}
  
  <!-- <style>
    h1, h2 {
      color: #333;
    }
  
    section {
      margin-top: 2rem;
    }
  
    ul {
      list-style-type: none;
      padding: 0;
    }
  
    li {
      margin-bottom: 0.5rem;
    }
  
    .button {
      display: inline-block;
      padding: 0.5rem 1rem;
      background-color: #007bff;
      color: white;
      text-decoration: none;
      border-radius: 4px;
      margin-right: 1rem;
    }
  </style> -->