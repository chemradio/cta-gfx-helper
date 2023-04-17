<script>
    import { enhance } from "$app/forms";
    import Icon from "@iconify/svelte";
    // import { onMount } from "svelte";

    import toast from "svelte-french-toast";
    import VideoAuto from "./videoGFXComponents/VideoAuto.svelte";
    import VideoFiles from "./videoGFXComponents/VideoFiles.svelte";
    import Audio from "./videoGFXComponents/shared/Audio.svelte";
    import Quote from "./videoGFXComponents/shared/Quote.svelte";
    let request_type = "video_auto";
    export let data;
    let loading = false;
    const submitVideoGFXOrder = async ({}) => {
        return async ({ result }) => {
            console.log(result);
            switch (result.data?.status) {
                case "ok":
                    toast.success("Order submitted successfully");
                    break;
                case "error":
                    toast.error("A problem occured");
                    break;
                default:
                    toast.error("Something went wrong");
                    break;
            }
            window.location.href = "/";
        };
    };
</script>

<form
    method="POST"
    action="/orders?/submitVideoGFXOrder"
    id="videoGFXForm"
    class="card rounded-0 bg-secondary p-0"
    use:enhance={submitVideoGFXOrder}
>
    <div class="card-header">
        <h3 class="form-label fw-bold">Видео-графика</h3>
        <small>Укажи ссылку или пришли файлы, получи MP4-видео</small>
    </div>

    <div class="card-body">
        <div class="mb-3 d-flex justify-content-between">
            <input
                class="btn-check"
                type="radio"
                bind:group={request_type}
                name="request_type"
                id="request_video_auto"
                value="video_auto"
            />

            <label
                class="btn btn-outline-primary rounded-0 w-50"
                for="request_video_auto"
            >
                <Icon icon="material-symbols:link" /> Из ссылки
            </label>
            <div class="m-2" style="border-left:1px solid #000;height:20px" />
            <input
                class="btn-check"
                type="radio"
                bind:group={request_type}
                name="request_type"
                id="request_video_files"
                value="video_files"
            />
            <label
                class="btn btn-outline-primary rounded-0 w-50"
                for="request_video_files"
                ><Icon icon="material-symbols:file-copy-rounded" /> Из файлов</label
            >
        </div>
        <hr />

        <div hidden={request_type !== "video_auto"}>
            <VideoAuto {request_type} />
        </div>
        <div hidden={request_type !== "video_files"}>
            <VideoFiles {request_type} />
        </div>

        <div hidden={!["video_files", "video_auto"].includes(request_type)}>
            <Quote />
            <Audio />
            <button
                disabled={loading}
                class="btn btn-primary w-100 rounded-0"
                type="submit">Заказать</button
            >
        </div>
    </div>
</form>
