<script>
    // export let formData;

    const checkboxChange = (event) => {
        let checkboxId = event.srcElement.id;
        formData[checkboxId] = event.srcElement.checked;
        if (event.srcElement.checked) {
            document.getElementById("quote_enabled_label").innerHTML =
                "Убрать цитату";
        } else {
            document.getElementById("quote_enabled_label").innerHTML =
                "Добавить цитату";
        }
    };
    const textChange = (event) => {
        let textId = event.srcElement.id;
        formData[textId] = event.srcElement.value;
    };
</script>

<div>
    <div class="mb-2">
        <input
            autocomplete="off"
            id="quote_enabled"
            class="btn-check"
            name="quote_enabled"
            type="checkbox"
            on:change={checkboxChange}
        />
        <label
            class="btn btn-outline-secondary w-100"
            id="quote_enabled_label"
            for="quote_enabled"
        >
            Добавить цитату
        </label>
    </div>
    {#if formData.quote_enabled}
        <div
            class="p-2 border border-secondary border-1 rounded-3 bg-light mb-3"
        >
            <div class="form-floating mb-3">
                <textarea
                    style="height: 150px"
                    id="quote_text"
                    type="textarea"
                    value=""
                    placeholder="Lorem ipsum"
                    class="form-control"
                    name="quote_text"
                    on:change={textChange}
                    required
                />
                <label for="quote_text">Текст Цитаты</label>
            </div>

            <div class="form-floating">
                <input
                    id="quote_author_text"
                    name="quote_author_text"
                    type="text"
                    class="form-control"
                    on:change={textChange}
                    required
                />
                <label for="quote_author_text">Автор цитаты</label>
            </div>
        </div>
        <hr />
    {/if}
</div>
