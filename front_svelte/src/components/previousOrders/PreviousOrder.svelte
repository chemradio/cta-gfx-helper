<script>
    import { onMount } from "svelte";

    export let order;

    let requestTypeHuman = "Графика из ссылки";
    switch (order.request_type) {
        case "video_auto":
            requestTypeHuman = "Графика из ссылки";
            break;
        case "video_files":
            requestTypeHuman = "Графика из файлов";
        default:
            requestTypeHuman = "...";
    }

    let currentStageMap = {
        ready_for_screenshots: "Подготовка к захвату скриншотов",
        screenshots_pending: "Захват скриншотов",
        ready_for_video_gfx: "Подготовка к анимации",
        video_gfx_pending: "Обработка анимации",
        ready_for_send: "Готов",
    };

    const orderEpoch =
        new Date(order.order_creation_end_timestamp).valueOf() / 1000;

    let time = new Date().valueOf() / 1000 - orderEpoch;

    $: hours = Math.floor(time / 3600);
    $: minutes = Math.floor((time % 3600) / 60);
    $: seconds = Math.trunc(time % 60);
    $: formattedTimeString =
        "" +
        hours +
        ":" +
        (minutes < 10 ? "0" : "") +
        "" +
        minutes +
        ":" +
        (seconds < 10 ? "0" : "") +
        "" +
        seconds;

    onMount(() => {
        const interval = setInterval(() => {
            time = new Date().valueOf() / 1000 - orderEpoch;
        }, 1000);

        return () => {
            clearInterval(interval);
        };
    });
</script>

<div class="card bg-secondary rounded-0 mt-1 mb-1">
    <div class="card-header d-flex justify-content-between w-100">
        <div>
            <strong>Заказ № {order.id}</strong><br />
            <small>Стадия: {currentStageMap[order.current_stage]}</small>
        </div>
        <div class="spinner-border align-self-center" role="status" />
    </div>
    <div class="card-body">
        {#if order.error}
            <p><strong>Ошибка:</strong> <span>{order.error_type}</span></p>
        {/if}
        <p><strong>Тип заказа:</strong> <span>{requestTypeHuman}</span></p>

        {#if order.request_type === "video_auto"}
            <p><strong>Ссылка:</strong> <span>{order.link}</span></p>
        {/if}
        <p><strong>В обработке:</strong> <span>{formattedTimeString}</span></p>

        <!-- quote part -->
        {#if order.quote_enabled}
            <p>
                <strong>Текст цитаты:</strong> <span>{order.quote_text}</span>
            </p>
            <p>
                <strong>Автор цитаты:</strong>
                <span>{order.quote_author_text}</span>
            </p>
        {/if}
        {#if order.audio_enabled}
            <p><strong>Аудио:</strong> <span>Да</span></p>
        {/if}
    </div>
</div>

<style>
    p {
        margin: 0;
    }
</style>
