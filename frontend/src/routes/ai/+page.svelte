<script lang="ts">
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let question = "";
  let answer = "";
  let error: string | null = null;
  let loading = false;

  async function askAI() {
    error = null;
    loading = true;
    answer = "";

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    const res = await fetch(`${API_URL}/ai/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ question })
    });

    if (!res.ok) {
      error = res.status === 403
        ? "Upgrade to Premium to use AI"
        : "AI request failed";
      loading = false;
      return;
    }

    const data = await res.json();
    answer = data.answer;
    loading = false;
  }
</script>

<h1>🤖 AI Tutor</h1>

<textarea
  rows="4"
  placeholder="Ask something about your course..."
  bind:value={question}
/>

<br />
<button on:click={askAI} disabled={loading || !question}>
  {loading ? "Thinking..." : "Ask AI"}
</button>

{#if error}
  <p style="color:red">{error}</p>
{/if}

{#if answer}
  <h3>Answer</h3>
  <pre>{answer}</pre>
{/if}
