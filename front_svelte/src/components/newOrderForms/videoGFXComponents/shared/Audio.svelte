<script>
    let audio_enabled = false;
</script>

<div class="mb-2">
    <input type="hidden" name="audio_enabled" bind:value={audio_enabled} />
    <input
        id="audio_enabled"
        class="btn-check"
        type="checkbox"
        name="audio_enabled"
        bind:checked={audio_enabled}
    />
    <label
        class="btn btn-outline-primary rounded-0 w-100"
        for="audio_enabled"
        id="audio_enabled_label">Аудио-файл</label
    >
</div>

<div hidden={!audio_enabled} class="rounded-0 mb-3">
    <label class="w-100 rounded-0">
        Аудио-файл (mp3 или wav):
        <input
            name="audio_file"
            class="form-control rounded-0"
            type="file"
            accept="audio/*"
            required={audio_enabled}
        />
    </label>
</div>
