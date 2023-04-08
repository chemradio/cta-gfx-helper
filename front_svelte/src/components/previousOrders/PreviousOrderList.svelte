<script>
  import PreviousOrder from "./PreviousOrder.svelte";
  export let orders;
</script>

<h5>Предыдущие заказы</h5>
<small>Сперва последние</small>
{#each orders as order}
  <PreviousOrder {order} />
{/each}
