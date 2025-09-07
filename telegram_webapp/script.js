document.addEventListener("DOMContentLoaded", () => {
    // Elements
    const audioCheckbox = document.getElementById("audio_enabled");
    const audioSection = document.getElementById("audio_section");
    audioCheckbox.addEventListener("change", () => {
        audioSection.style.display = audioCheckbox.checked ? "block" : "none";
    });

    const quoteCheckbox = document.getElementById("quote_enabled");
    const quoteSection = document.getElementById("quote_section");
    quoteCheckbox.addEventListener("change", () => {
        quoteSection.style.display = quoteCheckbox.checked ? "block" : "none";
    });

    const videoAutoRadio = document.getElementById("request_video_auto");
    const videoFilesRadio = document.getElementById("request_video_files");

    const linkField = document.getElementById("linkInput").closest(".mb-3"); // wrapper div
    const foregroundField = document
        .querySelector('input[name="foreground_file"]')
        .closest(".mb-3");
    const backgroundField = document
        .querySelector('input[name="background_file"]')
        .closest(".mb-3");

    // Update visibility based on selection
    const updateVideoFields = () => {
        if (videoAutoRadio.checked) {
            linkField.style.display = "block";
            linkField.querySelector("input").required = true;

            foregroundField.style.display = "none";
            backgroundField.style.display = "none";
            foregroundField.querySelector("input").required = false;
            backgroundField.querySelector("input").required = false;
        } else if (videoFilesRadio.checked) {
            linkField.style.display = "none";
            linkField.querySelector("input").required = false;

            foregroundField.style.display = "block";
            backgroundField.style.display = "block";
            foregroundField.querySelector("input").required = true;
            backgroundField.querySelector("input").required = false; // optional
        }
    };

    // Event listeners
    videoAutoRadio.addEventListener("change", updateVideoFields);
    videoFilesRadio.addEventListener("change", updateVideoFields);

    // Initialize visibility
    videoAutoRadio.checked = true;
    updateVideoFields();
});
