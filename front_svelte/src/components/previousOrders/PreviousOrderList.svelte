<script>
    import PreviousOrder from "./PreviousOrder.svelte";
    export let orders;
</script>

<div class="mb-5">
    <h5>Предыдущие заказы</h5>
    {#each orders as order}
        <PreviousOrder {order} />
    {/each}
</div>
