<script>
  export let formData;

  const checkboxChange = (event) => {
    let checkboxId = event.srcElement.id;
    formData[checkboxId] = event.srcElement.checked;
    if (event.srcElement.checked) {
      document.getElementById("audio_enabled_label").innerHTML = "Убрать аудио";
    } else {
      document.getElementById("audio_enabled_label").innerHTML =
        "Добавить аудио";
    }
  };
  const textChange = (event) => {
    let textId = event.srcElement.id;
    formData[textId] = event.srcElement.value;
  };
</script>

<div class="mb-3">
  <input
    id="audio_enabled"
    class="btn-check"
    type="checkbox"
    on:change={checkboxChange}
  />
  <label
    class="btn btn-outline-secondary w-100"
    for="audio_enabled"
    id="audio_enabled_label">Добавить аудио</label
  >
</div>

{#if formData.audio_enabled}
  <div class="mb-3">
    <label class="w-100">
      Аудио-файл (mp3 или wav):
      <input
        class="form-control"
        type="file"
        accept="audio/*"
        on:change={(event) => {
          formData.audio_file = event.target.files[0];
        }}
        required
      />
    </label>
  </div>
{/if}
