<script>
    export let request_type;
</script>

<div class="mb-1">
    <label class="form-label w-100">
        <p>Основной документ</p>
        <input
            name="foreground_file"
            class="form-control"
            type="file"
            value=""
            accept="image/*,.pdf"
            required={request_type === "video_files"}
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
            value=""
            accept="image/*,.pdf"
            required={request_type === "video_files"}
        />
    </label>
</div>
