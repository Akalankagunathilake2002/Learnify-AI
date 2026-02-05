<script lang="ts">
  import { goto } from "$app/navigation";
  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";
  let msg: string | null = null;

  async function upgrade() {
    msg = null;
    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    const res = await fetch(`${API_URL}/billing/create-checkout-session`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      msg = "❌ Failed to start checkout";
      return;
    }

    const data = await res.json();
    window.location.href = data.url; // ✅ redirect to Stripe Checkout
  }
</script>

<h1>Upgrade to Premium</h1>
<button on:click={upgrade}>Upgrade</button>
{#if msg}<p>{msg}</p>{/if}
