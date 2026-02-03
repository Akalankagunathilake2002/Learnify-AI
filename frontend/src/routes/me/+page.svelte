<script lang="ts">
  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let user: any = null;

  async function loadMe() {
    const token = localStorage.getItem("token");
    if (!token) {
      error = "No token found. Please login first.";
      loading = false;
      return;
    }

    try {
      const res = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      user = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed";
    } finally {
      loading = false;
    }
  }

  loadMe();
</script>

<h1>My Profile</h1>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
  <p><a href="/login">Go to Login</a></p>
{:else}
  <pre>{JSON.stringify(user, null, 2)}</pre>
{/if}
