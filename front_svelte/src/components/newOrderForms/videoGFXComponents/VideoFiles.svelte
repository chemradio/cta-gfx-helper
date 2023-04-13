<script>
    export let formData;
</script>

<div class="mb-1">
    <label class="form-label w-100">
        <p>Основной документ</p>
        <input
            name="foreground_file"
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
        <p>Задний план (необязательно)</p>
        <input
            name="background_file"
            class="form-control"
            type="file"
            accept="image/*,.pdf"
            on:change={(event) => {
                formData.background_file = event.target.files[0];
            }}
        />
    </label>
</div>
