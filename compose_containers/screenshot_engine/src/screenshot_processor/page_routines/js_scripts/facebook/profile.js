// remove banner from the top

// role="banner"
let banner = document.querySelector('[role="banner"]');
if (banner) banner.remove();

// role="main"
let main = document.querySelector('[role="main"]');

// in chrome dev tools i see padding 0, border 0, margin 0, but position is 56 on the top side
// i will try to remove it
main.style.position = "relative";
main.style.top = "0px";
