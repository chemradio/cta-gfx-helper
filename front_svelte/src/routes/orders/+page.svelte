<script>
    import VideoGfxForm from "../../components/newOrderForms/VideoGFXForm.svelte";
    import PreviousOrderList from "../../components/previousOrders/PreviousOrderList.svelte";
    export let data;
    let orders = data.orders;
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
