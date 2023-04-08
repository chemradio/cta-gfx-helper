<script>
  import { dispatcherOrdersURL } from "../../config";
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

  const submitNewOrder = async (event) => {
    console.log("post new order");
    event.preventDefault();
    const submitForm = new FormData();
    Object.entries(formData).forEach((e, i) => submitForm.append(...e));
    for (var pair of submitForm.entries()) {
      console.log(pair[0] + ": " + pair[1]);
    }

    try {
      const res = await fetch(dispatcherOrdersURL, {
        method: "post",
        credentials: "include",
        body: submitForm,
        // headers: {
        //   "Content-Type": "multipart/form-data",
        // },
      });
      console.log(res.status);
    } catch (error) {
      console.error(error);
      alert("Something went wrong. Please try again later.");
    }
  };
</script>

<h5>Новый заказ</h5>
<div class="container">
  <form
    id="videoGFXForm"
    class="card border-warning"
    on:submit={submitNewOrder}
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
        <label class="btn btn-outline-info px-5 w-50" for="request_video_auto"
          >Из ссылки
        </label>

        <input
          class="btn-check"
          type="radio"
          bind:group={formData.request_type}
          name="request_type"
          id="request_video_files"
          value={"video_files"}
        />
        <label
          class="btn btn-outline-warning px-5 w-50"
          for="request_video_files">Из файлов</label
        >
      </div>

      {#if formData.request_type === "video_auto"}
        <VideoAuto bind:formData />
      {:else}
        <VideoFiles bind:formData />
      {/if}
      <Quote bind:formData />
      <Audio bind:formData />
      <button class="btn btn-primary w-100" type="submit">Заказать</button>
    </div>
  </form>
</div>
