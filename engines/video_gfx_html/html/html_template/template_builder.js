fetch('./config.json')
    .then(response => response.json())
    .then(json => buildHTML(json));

function buildHTML(config) {
    // let mainContainer = document.getElementsByName('capture')[0];
    let mainContainer = document.createElement('div');
    mainContainer.setAttribute('class', 'main-container');
    document.body.append(mainContainer)

    // create midnight bg
    let midnightBackground = document.createElement('div');
    midnightBackground.setAttribute('class', 'layer midnightBG');
    mainContainer.append(midnightBackground);

    // create background image
    let backgroundLayer = document.createElement('div');
    backgroundLayer.setAttribute('class', 'layer');

    let backgroundContainer = document.createElement('div');
    backgroundContainer.setAttribute('class', 'background-container');
    
    let backgroundImage = document.createElement('img');
    backgroundImage.setAttribute('class', config.backgroundClass);
    backgroundImage.setAttribute('src', config.backgroundPath);

    backgroundLayer.append(backgroundContainer);
    backgroundContainer.append(backgroundImage);
    mainContainer.append(backgroundLayer);

    // if not single layer
    if (!config.singleLayer) {
        // create midnight foil
        let foilLayer = document.createElement('div');
        foilLayer.setAttribute('class', 'layer')

        let foilContainer = document.createElement('div');
        foilContainer.setAttribute('class', 'midnightFoil');

        foilLayer.append(foilContainer);
        mainContainer.append(foilLayer);

        // create foreground
        let foregroundLayer = document.createElement('div');
        foregroundLayer.setAttribute('class', 'layer');

        let foregroundContainer = document.createElement('div');
        foregroundContainer.setAttribute('class', 'foreground-container');
        
        let foregroundImage = document.createElement('img');
        foregroundImage.setAttribute('src', config.foregroundPath);
        
        if (config.roundCorners) {
            foregroundImage.setAttribute('class', `${config.foregroundClass} round-corners`);
        } else {
            foregroundImage.setAttribute('class', config.foregroundClass);
        }

        foregroundLayer.append(foregroundContainer);
        foregroundContainer.append(foregroundImage);
        mainContainer.append(foregroundLayer);
    }

    // create vignette overlay
    let vignetteContainer = document.createElement('div');
    vignetteContainer.setAttribute('class', 'layer');

    let vignetteImage = document.createElement('img');
    vignetteImage.setAttribute('src', "./vignette-overlay.png");

    vignetteContainer.append(vignetteImage);
    mainContainer.append(vignetteContainer);

    // create quote box
    if (config.quoteEnabled) {
        let quoteTextLength = config.quoteTextText.length;
        let quoteAuthorLength = config.quoteTextText.length;

        let targetLength = (quoteTextLength > quoteAuthorLength) ? quoteTextLength : quoteAuthorLength;
        let width;

        let quoteLayer = document.createElement('div');
        quoteLayer.setAttribute('class', 'layer');

        let quoteContainer = document.createElement('div');
        quoteContainer.setAttribute('class', 'quote-container');

        let quoteBox = document.createElement('div');
        quoteBox.setAttribute('class', 'quote-box');

        let quoteTextText = document.createElement('div');
        quoteTextText.setAttribute('class', 'quote-text-text');
        quoteTextText.innerHTML = config.quoteTextText;

        quoteBox.append(quoteTextText);

        if (config.quoteAuthorText) {
            let quoteBreak = document.createElement('br');
            let quoteAuthorText = document.createElement('div');
            quoteAuthorText.setAttribute('class', 'quote-author-text');
            quoteAuthorText.innerHTML = config.quoteAuthorText;
            quoteBox.append(quoteBreak);
            quoteBox.append(quoteAuthorText);
        }

        mainContainer.append(quoteLayer);
        quoteLayer.append(quoteContainer);
        quoteContainer.append(quoteBox);
    }

    let tailPlaceholder = document.createElement('div');
    tailPlaceholder.setAttribute('class', 'tail-nonexistent layer');
    mainContainer.append(tailPlaceholder);
}