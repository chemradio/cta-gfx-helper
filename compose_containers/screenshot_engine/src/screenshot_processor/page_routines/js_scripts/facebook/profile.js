// remove banner from the top

// role="banner"
let banner = document.querySelector('[role="banner"]');
if (banner) banner.remove();

// role="main"
let main = document.querySelector('[role="main"]');
let mainContainer =
  main.parentElement.parentElement.parentElement.parentElement;
if (mainContainer) mainContainer.style.position = "0px";
