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
    <div class="d-flex">
        <div
            class="toast"
            role="alert"
            aria-live="assertive"
            aria-atomic="true"
            auto-hode="false"
        >
            <div class="toast-header">
                <img src="..." class="rounded me-2" alt="..." />
                <strong class="me-auto">Bootstrap</strong>
                <small>11 mins ago</small>
                <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="toast"
                    aria-label="Close"
                />
            </div>
            <div class="toast-body">Hello, world! This is a toast message.</div>
        </div>
    </div>

    <VideoGfxForm />

    <hr />
    {#if data}
        <PreviousOrderList {orders} />
    {/if}
</div>
