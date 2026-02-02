<script lang="ts">
  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let data: any = null;

  async function loadHealth() {
    try {
      loading = true;
      const res = await fetch(`${API_URL}/health`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      data = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to connect";
    } finally {
      loading = false;
    }
  }

  loadHealth();
</script>

<h1>Backend Status</h1>

{#if loading}
  <p>Checking backend...</p>
{:else if error}
  <p style="color:red">Error: {error}</p>
{:else}
  <p>✅ Connected!</p>
  <pre>{JSON.stringify(data, null, 2)}</pre>
{/if}
