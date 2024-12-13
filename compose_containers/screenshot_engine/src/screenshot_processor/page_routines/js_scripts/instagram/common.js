const getPost = () => {
  return document.querySelector("article");
};

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getStory() {
  // accept "view as ..." dialog
  // find a div with role=button and with textContent = "View story"
  const viewStoryButton = Array.from(
    document.querySelectorAll('div[role="button"]')
  ).find((div) => div.innerHTML.trim() === "View story");
  if (viewStoryButton) {
    viewStoryButton.click();
  }

  // wait until story is loaded. it's about half a second. but it WILL load
  await delay(1000);

  // stop story playback - aria-label="Pause"
  let storyPause = document.querySelector('[aria-label="Pause"]').parentElement;
  if (storyPause) {
    console.log("pause button found");

    storyPause.click();
  }

  return document.querySelector('[referrerpolicy="origin-when-cross-origin"]');
}

const parsePost = async () => {
  const publicationType = checkPublicationType();
  if (publicationType === "error") {
    return null;
  } else if (publicationType === "post") {
    return await parsePost();
  } else if (publicationType === "story") {
    return await parseStory();
  }
};

const checkPublicationType = () => {
  if (document.querySelector("article")) return "post";
  if (
    document.querySelector('[referrerpolicy="origin-when-cross-origin"]') ||
    Array.from(document.querySelectorAll('div[role="button"]')).find(
      (div) => div.innerHTML.trim() === "View story"
    )
  )
    return "story";
  return "error";
};

const parseProfile = async () => {
  // find the first class
  let firstClass = document.querySelectorAll(".xvbhtw8");
  let target;
  for (const el of firstClass) {
    let secondClass = el.querySelector(".x1qughib");
    if (secondClass) {
      sidePanel = secondClass;
      break;
    }
  }
  sidePanel.remove();

  const main = document.querySelector('[role="main"]');
  main.parentElement.parentElement.style.margin = "0px";
  main.parentElement.parentElement.parentElement.style.justifyContent =
    "center";
  return document.body;
};

const extractProfileURL = async () => {
  const post = await parsePost();
};
