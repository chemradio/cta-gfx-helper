console.log("quoteboxResizer.js loaded");
// constants
const maxTextLength = 600;
const minTextLength = 10;

const maxWidth = 1650;
const minWidth = 700;

// linear interoplation magic
const lerp = (x, y, a) => x * (1 - a) + y * a;
const clamp = (a, min = 0, max = 1) => Math.min(max, Math.max(min, a));
const invlerp = (x, y, a) => clamp((a - x) / (y - x));
const range = (x1, y1, x2, y2, a) => lerp(x2, y2, invlerp(x1, y1, a));

function resizeQuoteBox() {
  // get text length
  const quoteText = document.querySelector(".quote-text-text");
  const textLength = quoteText.textContent.length;

  // calc target div maxwidth and apply it
  const targetWidth = range(
    minTextLength,
    maxTextLength,
    minWidth,
    maxWidth,
    textLength
  );

  const quoteBox = document.querySelector(".quote-box");
  quoteBox.style.maxWidth = `${targetWidth}px`;

  // remove the line-break caused oversizing of the quote-box div by the p tag
  const docRange = document.createRange();
  docRange.selectNodeContents(quoteText);
  const { width: actualTextWidth } = docRange.getBoundingClientRect();
  quoteText.style.width = `${actualTextWidth}px`;
}

resizeQuoteBox();
