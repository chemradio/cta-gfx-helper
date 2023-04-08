<script>
  import { onMount } from "svelte";
  import { dispatcherLoginURL } from "../../config";

  const logout = async () => {
    const res = await fetch(`${dispatcherLoginURL}`, {
      method: "delete",
      credentials: "include",
    });
    if (res.status === 200) window.location.href = "/";
  };
  onMount(async () => {
    await logout();
  });
</script>
