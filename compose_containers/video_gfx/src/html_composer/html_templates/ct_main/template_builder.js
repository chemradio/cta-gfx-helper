fetch("./config.json")
    .then((response) => response.json())
    .then((json) => buildHTML(json));

function buildHTML(config) {
    // let mainContainer = document.getElementsByName('capture')[0];
    let mainContainer = document.createElement("div");
    mainContainer.setAttribute("class", "main-container");
    let targetHeight = config.verticalResolution || 1080;
    let targetWidth = (targetHeight / 9) * 16;
    mainContainer.style.width = targetWidth + "px";
    mainContainer.style.height = targetHeight + "px";
    document.body.append(mainContainer);

    // create midnight bg
    let midnightBackground = document.createElement("div");
    midnightBackground.setAttribute("class", "layer midnightBG");
    mainContainer.append(midnightBackground);

    // create background image
    let backgroundLayer = document.createElement("div");
    backgroundLayer.setAttribute("class", "layer");

    let backgroundContainer = document.createElement("div");
    backgroundContainer.setAttribute("class", "background-container");

    let backgroundImage = document.createElement("img");
    //   backgroundImage.setAttribute("class", config.backgroundClass);
    backgroundImage.setAttribute("src", config.backgroundPath);

    let bgImage = new Image();
    bgImage.src = config.backgroundPath;
    bgImage.onload = function () {
        // get bg orientation
        let bgImageOrientation =
            bgImage.width / bgImage.height > 12 / 9
                ? "horizontal-background"
                : "vertical-background";

        // console.log(bgImage.width, bgImage.height);
        // console.log(bgImage.width / bgImage.height);
        // console.log(bgImageOrientation);
        // set bg main animation class
        if (config.singleLayer) {
            config.backgroundClass = "bgOnly";
        } else {
            if (bgImageOrientation == "horizontal-background") {
                config.backgroundClass = "bgZoom";
            } else if (bgImageOrientation == "vertical-background") {
                config.backgroundClass = "bgScroll";
            }
        }
        backgroundImage.setAttribute("class", config.backgroundClass);

        // resize background image
        if (config.backgroundClass == "bgZoom") {
            backgroundImage.setAttribute(
                "class",
                backgroundImage.getAttribute("class") +
                    " " +
                    bgImageOrientation +
                    "-zoom"
            );
        } else if (config.backgroundClass == "bgOnly") {
            backgroundImage.setAttribute(
                "class",
                backgroundImage.getAttribute("class") +
                    " " +
                    bgImageOrientation +
                    "-scroll"
            );
        }
    };

    backgroundLayer.append(backgroundContainer);
    backgroundContainer.append(backgroundImage);
    mainContainer.append(backgroundLayer);

    // if not single layer
    if (!config.singleLayer) {
        // create midnight foil
        let foilLayer = document.createElement("div");
        foilLayer.setAttribute("class", "layer");

        let foilContainer = document.createElement("div");
        foilContainer.setAttribute("class", "midnightFoil");

        foilLayer.append(foilContainer);
        mainContainer.append(foilLayer);

        // create foreground
        let foregroundLayer = document.createElement("div");
        foregroundLayer.setAttribute("class", "layer");

        let foregroundContainer = document.createElement("div");
        foregroundContainer.setAttribute("class", "foreground-container");

        let foregroundImage = document.createElement("img");
        foregroundImage.setAttribute("src", config.foregroundPath);

        //
        let fgImage = new Image();
        fgImage.src = config.foregroundPath;
        fgImage.onload = function () {
            let fgImageOrientationPrimary =
                fgImage.height / fgImage.width > 1.6
                    ? "vertical-foreground"
                    : "horizontal-foreground";

            // set fg main animation class
            if (fgImageOrientationPrimary == "horizontal-foreground") {
                config.foregroundClass = "fgZoom";
            } else if (fgImageOrientationPrimary == "vertical-foreground") {
                config.foregroundClass = "fgScroll";
            }
            foregroundImage.setAttribute(
                "class",
                config.foregroundClass + " round-corners"
            );

            if (config.foregroundClass == "fgZoom") {
                let fgImageOrientationZoom =
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

        foregroundLayer.append(foregroundContainer);
        foregroundContainer.append(foregroundImage);
        mainContainer.append(foregroundLayer);
    }

    // create vignette overlay
    let vignetteContainer = document.createElement("div");
    vignetteContainer.setAttribute("class", "layer");

    let vignetteImage = document.createElement("img");
    vignetteImage.setAttribute("src", "./vignette-overlay.png");
    vignetteImage.setAttribute("class", "vignette-image");

    vignetteContainer.append(vignetteImage);
    mainContainer.append(vignetteContainer);

    // create quote box
    if (config.quoteEnabled) {
        let quoteTextLength = config.quoteTextText.length;
        let quoteAuthorLength = config.quoteTextText.length;

        let targetLength =
            quoteTextLength > quoteAuthorLength
                ? quoteTextLength
                : quoteAuthorLength;
        let width;

        let quoteLayer = document.createElement("div");
        quoteLayer.setAttribute("class", "layer");

        let quoteContainer = document.createElement("div");
        quoteContainer.setAttribute("class", "quote-container");

        let quoteBox = document.createElement("div");
        quoteBox.setAttribute("class", "quote-box");

        let fontRatio = 0.037;
        quoteBox.style.fontSize = targetHeight * fontRatio + "px";

        let paddingRatio = 0.0277;
        quoteBox.style.padding = targetHeight * paddingRatio + "px";

        console.log(config.quoteTextText);
        console.log(config.quoteAuthorText);

        const quoteTextText = insertUnbreakableSpaces(
            preprocessString(config.quoteTextText)
        );
        const quoteAuthorText = insertUnbreakableSpaces(
            preprocessString(config.quoteAuthorText || "")
        );

        let quoteTextEl = document.createElement("p");
        quoteTextEl.setAttribute("class", "quote-text-text");
        quoteTextEl.innerHTML = quoteTextText;
        quoteBox.append(quoteTextEl);

        if (config.quoteAuthorText) {
            let quoteBreakEl = document.createElement("br");
            quoteBox.append(quoteBreakEl);
            let quoteAuthorEl = document.createElement("div");
            quoteAuthorEl.setAttribute("class", "quote-author-text");
            quoteAuthorEl.innerHTML = quoteAuthorText;
            quoteAuthorEl.style.fontSize = "40px";
            quoteBox.append(quoteAuthorEl);
        }

        quoteContainer.append(quoteBox);
        quoteLayer.append(quoteContainer);
        mainContainer.append(quoteLayer);
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
