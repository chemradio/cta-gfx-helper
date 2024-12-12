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

  await delay(1000);
  // stop story playback - aria-label="Pause"
  let storyPause = document.querySelector('[aria-label="Pause"]').parentElement;
  if (storyPause) {
    storyPause.click();
  }

  //   return document.querySelectorAll('img[draggable="false"]')[1];
  return document.querySelector('[referrerpolicy="origin-when-cross-origin"]');
}

const parsePost = () => {
  // try get the post
  let post = getPost();
  if (post) {
    return post;
  }

  // try get the story
  let story = await getStory();
  return story
};

const parseProfile = () => {
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

  let main = document.querySelector('[role="main"]');
  main.parentElement.parentElement.style.margin = "0px";
  main.parentElement.parentElement.parentElement.style.justifyContent =
    "center";
  return document.body;
};
