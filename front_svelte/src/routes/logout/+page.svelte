<script>
    import { onMount } from "svelte";
    export let data;
    onMount(() => {
        // const { email, password } = Object.fromEntries(data.entries());
        if (data.status === "ok") {
            window.location.href = "/";
        }
    });
</script>
