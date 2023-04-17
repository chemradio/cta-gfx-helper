<script>
    let quote_enabled = false;
</script>

<div>
    <div class="mb-2">
        <input type="hidden" name="quote_enabled" bind:value={quote_enabled} />
        <input
            autocomplete="off"
            id="quote_enabled"
            class="btn-check"
            name="quote_enabled"
            type="checkbox"
            value="on"
            bind:checked={quote_enabled}
        />
        <label
            class="btn btn-outline-primary w-100 rounded-0"
            id="quote_enabled_label"
            for="quote_enabled"
        >
            Цитата
        </label>
    </div>
    <div hidden={!quote_enabled} class=" rounded-0 bg-secondary mb-3">
        <div class="form-floating mb-3">
            <textarea
                style="height: 150px"
                id="quote_text"
                type="textarea"
                value=""
                class="form-control rounded-0"
                name="quote_text"
                required={quote_enabled}
            />
            <label for="quote_text">Текст Цитаты</label>
        </div>

        <div class="form-floating">
            <input
                id="quote_author_text"
                name="quote_author_text"
                type="text"
                value=""
                class="form-control rounded-0"
                required={quote_enabled}
            />
            <label for="quote_author_text">Автор цитаты</label>
        </div>
    </div>
</div>
