// remove "comment as ..."
let myImages = document.querySelectorAll('[aria-label="Available Voices"]');
if (myImages.length > 0) {
  myImages.forEach((image) => {
    image.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.remove();
  });
}

//
let topRightProfileImage = document.querySelector('[aria-label="Ваш профиль"]');
if (topRightProfileImage) {
  topRightProfileImage.remove();
}
