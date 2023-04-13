<script>
    import { enhance } from "$app/forms";
    import Icon from "@iconify/svelte";
    import toast from "svelte-french-toast";
    import VideoAuto from "./videoGFXComponents/VideoAuto.svelte";
    import VideoFiles from "./videoGFXComponents/VideoFiles.svelte";
    import Audio from "./videoGFXComponents/shared/Audio.svelte";
    import Quote from "./videoGFXComponents/shared/Quote.svelte";
    let formData = {
        request_type: "video_auto",
        quote_enabled: false,
        quote_text: "",
        quote_author_text: "",
        audio_enabled: false,
        audio_file: "",
        link: "",
        foreground_file: "",
        background_file: "",
    };

    let loading = false;
    const submitVideoGFXOrder = async ({}) => {
        return async ({ result, update }) => {
            loading = true;
            console.log(result);
            switch (result.data?.status) {
                case "error":
                    toast.error(result.data.message);
                    await update();
                    break;
                default:
                    toast.success("Successfully registered");
                    break;
            }
            loading = false;
            await update();
        };
    };
</script>

<h5>Новый заказ</h5>
<div class="container">
    <form
        method="POST"
        action="/orders?/submitVideoGFXOrder"
        id="videoGFXForm"
        class="card rounded-0"
        use:enhance={submitVideoGFXOrder}
    >
        <div class="card-header">
            <h5 class="form-label">Видео-графика</h5>
            <small>Укажи ссылку или пришли файлы, получи MP4-видео</small>
        </div>

        <div class="card-body">
            <div class="mb-3 d-flex justify-content-between">
                <input
                    class="btn-check"
                    type="radio"
                    bind:group={formData.request_type}
                    name="request_type"
                    id="request_video_auto"
                    value={"video_auto"}
                />

                <label
                    class="btn btn-outline-primary px-5 w-50"
                    for="request_video_auto"
                >
                    <Icon icon="material-symbols:link" /> Из ссылки
                </label>
                <div
                    class="m-2"
                    style="border-left:1px solid #000;height:20px"
                />
                <input
                    class="btn-check"
                    type="radio"
                    bind:group={formData.request_type}
                    name="request_type"
                    id="request_video_files"
                    value={"video_files"}
                />
                <label
                    class="btn btn-outline-primary px-5 w-50"
                    for="request_video_files"
                    ><Icon icon="material-symbols:file-copy-rounded" /> Из файлов</label
                >
            </div>
            <hr />

            {#if formData.request_type === "video_auto"}
                <VideoAuto bind:formData />
            {:else}
                <VideoFiles bind:formData />
            {/if}
            <Quote bind:formData />
            <Audio bind:formData />
            <button
                disabled={loading}
                class="btn btn-primary w-100"
                type="submit">Заказать</button
            >
        </div>
    </form>
</div>
