let dialogs = document.querySelectorAll('[role="dialog"]');

let target;
dialogs.forEach((dialog) => {
  let article = dialog.querySelector('[role="article"]');
  if (article) {
    target = article;
  }
});

return target;
