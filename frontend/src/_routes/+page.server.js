const apiUrl = process.env.API_URL || 'http://app-host:8000';

export function load({ fetch }) {
    return {
      streamed: {
        serverData: fetch(`${apiUrl}/api/users`).then(r => r.json())
      }
    };
  }