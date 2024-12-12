// POST
const fallbackSingleLayerError = () => {
  throw new Error("Fallback to single layer");
};

const getDialogPost = () => {
  let dialogs = document.querySelectorAll('[role="dialog"]');

  let target;
  dialogs.forEach((dialog) => {
    let article = dialog.querySelector('[role="article"]');
    if (article) {
      target = article;
    }
  });

  return target;
};

const getVideoPost = () => {
  let watchPerm = document.querySelector(
    '[data-pagelet="WatchPermalinkVideo"]'
  );
  return watchPerm.parentElement.parentElement;
};

const parsePost = () => {
  removeCommentAs();

  let dialogs = document.querySelectorAll('[role="dialog"]');
  if (dialogs.length > 0) {
    return getDialogPost();
  }

  let permalinkVideo = document.querySelector(
    '[data-pagelet="WatchPermalinkVideo"]'
  );
  if (permalinkVideo) {
    return getVideoPost();
  }

  let profileNavTabs = document.querySelector('[data-pagelet="ProfileTabs"]');
  if (profileNavTabs) {
    return fallbackSingleLayerError();
  }

  return fallbackSingleLayerError();
};

// PROFILE
const removeBanner = () => {
  let banner = document.querySelector('[role="banner"]');
  if (banner) banner.remove();
  let main = document.querySelector('[role="main"]');
  let secondary = main.parentElement.parentElement.parentElement.parentElement;
  secondary.style.position = "relative";
  secondary.style.top = "0px";
};

const parseProfile = () => {
  removeBanner();
  removeCommentAs();
  return document.body;
};

// EXTRACT PROFILE URL
const extractProfileURL = () => {
  let post = parsePost();
  let profileURL = post.parentElement.parentElement.getAttribute("href");
  return profileURL;
};

// HELPERS
const removeCommentAs = () => {
  let myImages = document.querySelectorAll('[aria-label="Available Voices"]');
  if (myImages.length > 0) {
    myImages.forEach((image) => {
      image.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.remove();
    });
  }
};
