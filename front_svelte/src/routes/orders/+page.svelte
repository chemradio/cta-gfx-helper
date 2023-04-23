<script>
    import { invalidate } from "$app/navigation";
    import { onMount } from "svelte";
    import VideoGfxForm from "../../components/newOrderForms/VideoGFXForm.svelte";
    import PreviousOrderList from "../../components/previousOrders/PreviousOrderList.svelte";
    export let data;
    let orders = data.orders;
    const reloadOrders = async () => {
        // any of these will cause the `load` function to re-run
        await invalidate("app:previousOrders");
        orders = data.orders;
    };

    onMount(() => {
        // Call `updateData()` every 2 seconds
        setInterval(reloadOrders, 2000);
    });
</script>

<svelte:head>
    <title>My Orders</title>
    <meta name="description" content="Svelte demo app" />
</svelte:head>

<div class="col">
    <div class="m-3">
        <h1>Новый заказ</h1>

        <VideoGfxForm {data} />

        <hr />
        <PreviousOrderList {orders} />
    </div>
</div>
