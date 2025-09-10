function censorText(text) {
    // Simple word list - one regex per word type
    const patterns = [
        // English
        /fuck(ing|ed|er|s)?/gi,
        /shit(ty|s)?/gi,
        /bitch(es|y)?/gi,
        /ass(hole|es)?/gi,
        /damn(ed)?/gi,
        /hell/gi,
        /crap(py|s)?/gi,
        /bastard(s)?/gi,

        // Russian - individual words
        /хуй/gi,
        /хуйня/gi,
        /хуе/gi,
        /хуя/gi,
        /хуи/gi,
        /хуяф/gi,
        /блядь/gi,
        /блядский/gi,
        /бледь/gi,
        /бля/gi,
        /бляд/gi,
        /пизда/gi,
        /пиздец/gi,
        /пиздо/gi,
        /пизд/gi,
        /ебать/gi,
        /ебучий/gi,
        /ебля/gi,
        /ебал/gi,
        /ёб/gi,
        /ёбыв/gi,
        /ебн/gi,
        /сука/gi,
        /сучка/gi,
        /гавно/gi,
        /мудак/gi,
        /дерьмо/gi,
    ];

    return patterns.reduce((result, pattern) => {
        return result.replace(pattern, (match) => {
            if (match.length <= 2) return match;
            return (
                match[0] +
                "*".repeat(match.length - 2) +
                match[match.length - 1]
            );
        });
    }, text);
}
function censorWebpage() {
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );

    const textNodes = [];
    let node;

    // Collect all text nodes
    while ((node = walker.nextNode())) {
        textNodes.push(node);
    }

    // Process each text node
    textNodes.forEach((textNode) => {
        const originalText = textNode.textContent;
        const censoredText = censorText(originalText);
        if (originalText !== censoredText) {
            textNode.textContent = censoredText;
        }
    });
}

censorWebpage();
