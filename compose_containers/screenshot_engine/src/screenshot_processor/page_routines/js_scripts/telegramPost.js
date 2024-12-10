// get the iframe which contains the telegram post
iframe = document.querySelector("iframe");
iframe.style.padding = "0px";

element = iframe.contentWindow.document.querySelector(
  ".tgme_widget_message_bubble"
);
element.style.border = "0";
element.style.margin = "0px";

// remove the small tail leading to author profile picture
bubbleTail = iframe.contentWindow.document.querySelector(
  ".tgme_widget_message_bubble_tail"
);
if (bubbleTail) bubbleTail.parentNode.removeChild(bubbleTail);

// remove the inner padding of the message bubble to iframe
messageWidget =
  iframe.contentWindow.document.querySelector(".js-widget_message");
messageWidget.style.padding = "0px";

iframe;
