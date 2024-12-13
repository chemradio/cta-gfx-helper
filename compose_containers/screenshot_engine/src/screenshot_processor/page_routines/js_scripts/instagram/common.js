const getPageType = () => {
  const postDetectors = [
    "article",
    ".x6s0dn4.x78zum5.xdt5ytf.xdj266r.xkrivgy.xat24cr.x1gryazu.x1n2onr6.xh8yej3",
    ".x1yvgwvq .x1dqoszc .x1ixjvfu .xhk4uv .x13fuv20 .xu3j5b3 .x1q0q8m5 .x26u7qi .x178xt8z .xm81vs4 .xso031l .xy80clv .x78zum5 .x1q0g3np .xh8yej3",
  ];

  const storyDetectors = [
    ".xyzq4qe .xgqcy7u .x1lq5wgf .x5yr21d .x6ikm8r .x10wlt62 .x1n2onr6 .x87ps6o .xh8yej3 .x1ja2u2z",
    '[aria-label="Pause"]',
    '[aria-label="Play"]',
  ];

  const profileDetectors = [
    'canvas[class="xnz67gz x14yjl9h xudhj91 x18nykt9 xww2gxu x9f619 x1lliihq x2lah0s x6ikm8r x10wlt62 x1n2onr6 xzfakq x7imw91 x1j8hi7x x5aw536 x194ut8o x1vzenxt xd7ygy7 xt298gk xynf4tj xdspwft x1r9ni5o x1d52zm6 xoiy6we x15xhmf9 x1qj619r x15tem40 x1xrz1ek x1s928wv x1n449xj x2q1x1w x1j6awrg x162n7g1 x1m1drc7"]',
    '[role="tablist"]',
    '[aria-label="Link icon"]',
  ];

  const isInCategory = (category) => {
    for (const selector of category) {
      const element = document.querySelector(selector);
      if (element) {
        console.log(element);
        return true;
      }
    }
    return false;
  };

  if (isInCategory(postDetectors)) {
    return "post";
  }
  if (isInCategory(storyDetectors)) {
    return "story";
  }
  if (isInCategory(profileDetectors)) {
    return "profile";
  }
  return "unknown";
};

const parsePost = async () => {
  const getPost = () => {
    return document.querySelector("article");
  };
  async function getStory() {
    function delay(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }

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
    let storyPause = document.querySelector(
      '[aria-label="Pause"]'
    ).parentElement;
    if (storyPause) {
      console.log("pause button found");

      storyPause.click();
    }

    return document.querySelector(
      '[referrerpolicy="origin-when-cross-origin"]'
    );
  }

  const pageType = getPageType();
  if (pageType === "unknown") {
    return null;
  } else if (pageType === "post") {
    return await getPost();
  } else if (pageType === "story") {
    return await getStory();
  } else if (pageType === "profile") {
    throw new Error("Page is a profile, not a post or story");
  } else {
    throw new Error("Unknown page type");
  }
};

const parseProfile = async () => {
  if (getPageType() != "profile") throw new Error("Page is not a profile.");
  // remove the side panel
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

  // center the main content area
  const main = document.querySelector('[role="main"]');
  main.parentElement.parentElement.style.margin = "0px";
  main.parentElement.parentElement.parentElement.style.justifyContent =
    "center";
  return document.body;
};

const extractProfileURL = async () => {
  // const post = await parsePost();
};
