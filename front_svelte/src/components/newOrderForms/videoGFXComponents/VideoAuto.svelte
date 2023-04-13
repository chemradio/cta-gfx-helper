<script>
    export let formData;
    let link_inside;

    const textChange = (event) => {
        let textId = event.srcElement.id;
        formData[textId] = event.srcElement.value;
    };

    const pasteClipboard = async () => {
        try {
            const text = await navigator.clipboard.readText();
            link_inside = text;
        } catch (error) {}
    };
</script>

<div class="mb-3">
    <label for="linkInput" class="form-label"><p>Ссылка</p></label>
    <div class="input-group">
        <input
            on:change={textChange}
            bind:value={link_inside}
            name="link"
            type="text"
            class="form-control"
            aria-describedby="basic-addon1"
            id="linkInput"
            required
        />
        <span on:click={pasteClipboard} class="input-group-text" id="paste-link"
            >📋</span
        >
    </div>
</div>

<!-- 
<div class="form-floating mb-3">
  <input
    on:change={textChange}
    id="linkInput"
    class="form-control"
    type="text"
    required
    placeholder="https://currenttime.tv"
  />
  <label for="linkInput">Ссылка</label>
</div> -->
