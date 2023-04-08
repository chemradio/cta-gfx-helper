<script>
  export let formData;
</script>

<div class="mb-1">
  <label class="form-label w-100">
    Основной документ
    <input
      class="form-control"
      type="file"
      accept="image/*,.pdf"
      on:change={(event) => {
        formData.foreground_file = event.target.files[0];
      }}
      required
    />
  </label>
</div>
<div class="mb-3">
  <label class="form-label w-100">
    Задний план (необязательно)
    <input
      class="form-control"
      type="file"
      accept="image/*,.pdf"
      on:change={(event) => {
        formData.background_file = event.target.files[0];
      }}
    />
  </label>
</div>
