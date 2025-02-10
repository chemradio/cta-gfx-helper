fetch("./config.json")
    .then((response) => response.json())
    .then((json) => buildHTML(json));

function buildHTML(config) {
    // create background image
    const backgroundContainer = document.querySelector(".background-container");
    const backgroundImage = document.createElement("img");
    backgroundImage.setAttribute("src", config.backgroundPath);

    const bgImage = new Image();
    bgImage.src = config.backgroundPath;
    bgImage.onload = function () {
        // get bg orientation
        const bgImageOrientation =
            bgImage.width / bgImage.height > 12 / 9
                ? "horizontal-background"
                : "vertical-background";

        let targetClass;

        if (config.singleLayer) {
            targetClass = "bgOnly";
        } else {
            if (bgImageOrientation == "horizontal-background") {
                targetClass = "bgZoom";
            } else if (bgImageOrientation == "vertical-background") {
                targetClass = "bgScroll";
            }
        }
        backgroundImage.setAttribute("class", targetClass);

        // resize background image
        if (targetClass == "bgZoom") {
            backgroundImage.setAttribute(
                "class",
                backgroundImage.getAttribute("class") +
                    " " +
                    bgImageOrientation +
                    "-zoom"
            );
        } else if (targetClass == "bgOnly") {
            backgroundImage.setAttribute(
                "class",
                backgroundImage.getAttribute("class") +
                    " " +
                    bgImageOrientation +
                    "-scroll"
            );
        }
    };
    backgroundContainer.append(backgroundImage);

    // if not single layer
    if (!config.singleLayer) {
        const foregroundContainer = document.querySelector(
            ".foreground-container"
        );
        const foregroundImage = document.createElement("img");
        foregroundImage.setAttribute("src", config.foregroundPath);

        const fgImage = new Image();
        fgImage.src = config.foregroundPath;
        fgImage.onload = function () {
            let fgImageOrientationPrimary =
                fgImage.height / fgImage.width > 1.6
                    ? "vertical-foreground"
                    : "horizontal-foreground";

            let targetClass;
            // set fg main animation class
            if (fgImageOrientationPrimary == "horizontal-foreground") {
                targetClass = "fgZoom";
            } else if (fgImageOrientationPrimary == "vertical-foreground") {
                targetClass = "fgScroll";
            }
            foregroundImage.setAttribute(
                "class",
                targetClass + " round-corners"
            );

            if (targetClass == "fgZoom") {
                const fgImageOrientationZoom =
                    fgImage.width / fgImage.height > 4 / 3
                        ? "horizontal-foreground-zoom"
                        : "vertical-foreground-zoom";
                foregroundImage.setAttribute(
                    "class",
                    foregroundImage.getAttribute("class") +
                        " " +
                        fgImageOrientationZoom
                );
            }
        };
        foregroundContainer.append(foregroundImage);
    } else {
        document.querySelector(".midnightFoil").style.display = "none";
    }

    // create quote box
    const quoteContainer = document.querySelector(".quote-container");
    if (config.quoteEnabled) {
        window.quoteEnabled = true;
        const quoteTextLength = config.quoteTextText.length;
        const quoteAuthorLength = config.quoteTextText.length;

        const targetLength =
            quoteTextLength > quoteAuthorLength
                ? quoteTextLength
                : quoteAuthorLength;

        const quoteBox = document.createElement("div");
        quoteBox.setAttribute("class", "quote-box");

        const fontRatio = 0.037;
        quoteBox.style.fontSize = config.verticalResolution * fontRatio + "px";

        const paddingRatio = 0.0277;
        quoteBox.style.padding =
            config.verticalResolution * paddingRatio + "px";

        const quoteTextText = insertUnbreakableSpaces(
            preprocessString(config.quoteTextText)
        );
        const quoteAuthorText = insertUnbreakableSpaces(
            preprocessString(config.quoteAuthorText || "")
        );

        const quoteTextEl = document.createElement("p");
        quoteTextEl.setAttribute("class", "quote-text-text");
        quoteTextEl.innerHTML = quoteTextText;
        quoteBox.append(quoteTextEl);

        if (config.quoteAuthorText) {
            const quoteBreakEl = document.createElement("br");
            quoteBox.append(quoteBreakEl);
            const quoteAuthorEl = document.createElement("div");
            quoteAuthorEl.setAttribute("class", "quote-author-text");
            quoteAuthorEl.innerHTML = quoteAuthorText;
            quoteAuthorEl.style.fontSize = "40px";
            quoteBox.append(quoteAuthorEl);
        }

        quoteContainer.append(quoteBox);
    } else {
        window.quoteEnabled = false;
        quoteContainer.remove();
    }
    window.quoteBoxReady = true;
    window.elementsReady = true;
}

function insertUnbreakableSpaces(text) {
    //   find all words that are shorter than 4 characters or included in a special list [] and replace the space after it with and unbreakable space
    const list = [
        "и",
        "в",
        "на",
        "с",
        "по",
        "к",
        "о",
        "за",
        "из",
        "от",
        "до",
        "у",
        "а",
        "не",
        "но",
        "или",
        "что",
        "как",
        "где",
        "кто",
        "чей",
        "тот",
        "этот",
        "сей",
    ];

    const words = text.split(" ");
    console.log(words);
    let result = "";
    for (let word of words) {
        if (
            // word.length < 4 ||
            list.includes(word)
        ) {
            result += word + "&nbsp;";
        } else {
            result += word + " ";
        }
    }
    return result;
}

function preprocessString(text) {
    console.log("preprocessString");
    console.log(text);
    while (
        text.indexOf("ё") > -1 ||
        text.indexOf("Ё") > -1 ||
        text.indexOf("«") > -1 ||
        text.indexOf("»") > -1 ||
        text.indexOf(" - ") > -1
    ) {
        text = text.replace("ё", "е");
        text = text.replace("Ё", "Е");
        text = text.replace("«", '"');
        text = text.replace("»", '"');
        text = text.replace(" - ", " – ");
    }
    text = text.replace(/^\s+|\s+$/g, "");
    while (text.indexOf("  ") > -1) {
        text = text.replace("  ", " ");
    }
    return text;
}
