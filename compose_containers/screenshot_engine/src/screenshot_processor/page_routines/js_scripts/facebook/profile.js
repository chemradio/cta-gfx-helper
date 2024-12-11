// remove the top banner completely
let banner = document.querySelector('[role="banner"]');
if (banner) banner.remove();
let main = document.querySelector('[role="main"]');
let secondary = main.parentElement.parentElement.parentElement.parentElement;
secondary.style.position = "relative";
secondary.style.top = "0px";
return document.body;
