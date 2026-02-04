<script lang="ts">
  import { clearToken } from "$lib/authStore";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  onMount(() => {
    clearToken();
    goto("/login");
  });
</script>

<p>Logging out...</p>
