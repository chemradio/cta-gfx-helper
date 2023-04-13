<script>
    import { invalidate } from "$app/navigation";
    import { onMount } from "svelte";
    onMount(async () => {
        await invalidate("/logout");
        await invalidate("/login");
    });
    export let form;
    if (form) console.log(form);
</script>
