let dialogs = document.querySelectorAll('[role="dialog"]');

// find role="article" in the dialog
let target;
dialogs.forEach((dialog) => {
  let article = dialog.querySelector('[role="article"]');
  if (article) {
    target = article;
  }
});

target;

// of fail - switch to singleLayer workflow
