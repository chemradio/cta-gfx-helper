<script>
  import { onMount } from "svelte";
  import VideoGfxForm from "../../components/newOrderForms/VideoGFXForm.svelte";
  import PreviousOrderList from "../../components/previousOrders/PreviousOrderList.svelte";
  import { dispatcherOrdersURL } from "../../config";
  export let data;
  let orders = [];
  console.log(data);

  const fetchUserOrders = async () => {
    console.log("entered fetchOrders");
    const res = await fetch(dispatcherOrdersURL, {
      method: "get",
      credentials: "include",
    });
    console.log("response from the getOrders");
    console.log(res);
    const data = await res.json();
    console.log("data: ", data);
    return data;
  };

  onMount(async () => {
    orders = await fetchUserOrders();
    orders = orders.reverse();
  });
</script>

<svelte:head>
  <title>My Orders</title>
  <meta name="description" content="Svelte demo app" />
</svelte:head>

<div class="col">
  <div class="row">
    <VideoGfxForm />
  </div>

  <hr />
  {#if data}
    <PreviousOrderList {orders} />
  {/if}
</div>
