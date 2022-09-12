
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

        const prepText = preprocessString(config.quoteTextText)
        const lines = splitStringParagraph(prepText);
        for (let i = 0; i < lines.length; i++) {
            let quoteTextText = document.createElement('div');
            quoteTextText.setAttribute('class', 'quote-text-text');
            quoteTextText.innerHTML = lines[i];
            quoteBox.append(quoteTextText);
        }


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


function splitStringParagraph(longString) {
    const maxCharsPerLineL0 = 50;
    const maxCharsPerLineL1 = 60;
    const maxCharsPerLineL2 = 70;
    const maxCharsPerLineL3 = 75;
    const maxCharsPerLineL4 = 80;


    const textLength = longString.length;
    let splitIndex;
    
    console.log(Math.floor(textLength/maxCharsPerLineL4));
    switch (Math.floor(textLength/maxCharsPerLineL4)) {
        case 0:
            splitIndex = maxCharsPerLineL0;
            break;
        case 1:
            splitIndex = maxCharsPerLineL1;
            break;
        case 2:
            splitIndex = maxCharsPerLineL2;
            break;
        case 3:
            splitIndex = maxCharsPerLineL3;
            break;
        default:
            splitIndex = maxCharsPerLineL4;
            break;
    }

    let procString = longString;
    let output = '';
    
    while (true) {
        if (procString.length >= splitIndex) {
            let targetIndex = procString.slice(0, splitIndex).lastIndexOf(' ');
            let firstString = procString.slice(0,targetIndex);
            let secondString = procString.slice(targetIndex);
    
            while (true) {
                let lastWhite = firstString.lastIndexOf(' ');
                if ( (targetIndex - lastWhite) <= 4) {
                    let chunk = firstString.slice(lastWhite);
                    firstString = firstString.slice(0, lastWhite);
                    secondString = chunk + ' ' + secondString;    
                } else {
                    break;
                }
            }

            output += (firstString + '\n');
            procString = secondString;
        } else {
            output += procString;
            break
        }
    }
    return output.split('\n');
}


function preprocessString(text) {
    while (
        text.indexOf("ё") > -1 ||
        text.indexOf("Ё") > -1 ||
        text.indexOf("«") > -1 ||
        text.indexOf("»") > -1 ||
        text.indexOf(" - ") > -1
    ) {
        text = text.replace('ё', 'е')
        text = text.replace('Ё', 'Е')
        text = text.replace('«', '"')
        text = text.replace('»', '"')
        text = text.replace(' - ', ' – ')
    }
    text = text.replace(/^\s+|\s+$/g, '')
    while (text.indexOf('  ') > -1) {
        text = text.replace('  ', ' ')
    }
    return text
}
