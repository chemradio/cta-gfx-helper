<script>
    export let request_type;
</script>

<div class="mb-3">
    <label for="linkInput" class="form-label"><p>Ссылка</p></label>
    <div class="input-group">
        <input
            name="link"
            value="https://meduza.io/"
            type="text"
            class="form-control"
            aria-describedby="basic-addon1"
            id="linkInput"
            required={request_type === "video_auto"}
        />
    </div>
</div>
