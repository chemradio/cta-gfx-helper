const getPageType = () => {
    const postDetectors = [
        '[class="xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1iyjqo2 xy5w88m"]',
        '[data-ad-preview="message"]',
        '[data-ad-comet-preview="message"]',
        '[data-ad-rendering-role="story_message"]',
        '[data-pagelet="WatchPermalinkVideo"]',
        // '[role="dialog"]',
    ];

    const storyDetectors = [
        // some containers
        'div[class="x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k xh8yej3"]',
        '[data-pagelet="StoriesContentPane"]',
        '[data-pagelet="StoriesCardMedia"]',
        // press to view story
        // '[class="x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k xh8yej3"]',
        // play button
        // '[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1n2onr6 x87ps6o x1lku1pv x1a2a7pz"]',
    ];

    const profileDetectors = [
        '[data-pagelet="ProfileTilesFeed_{n}"]',
        '[data-pagelet="ProfileTilesFeed_1"]',
        '[data-pagelet="ProfileTabs"]',
        '[data-pagelet="ProfileActions"]',
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

    if (isInCategory(profileDetectors)) {
        console.log("Page type: PROFILE");
        return "profile";
    }
    if (isInCategory(storyDetectors)) {
        console.log("Page type: STORY");
        return "story";
    }
    if (isInCategory(postDetectors)) {
        console.log("Page type: POST");
        return "post";
    }
    console.log("Page type: UNKNOWN");
    return "unknown";
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

// POST
const fallbackSingleLayerError = () => {
    throw new Error("Fallback to single layer");
};

const parsePost = async () => {
    document.body.style.fontFamily = "'Roboto', sans-serif";
    const getGroupPost = () => {};
    const getDialogPost = () => {
        let dialogs = document.querySelectorAll('[role="dialog"]');
        if (dialogs.length < 1) {
            return null;
        }

        let target;
        dialogs.forEach((dialog) => {
            let article = dialog.querySelector('[role="article"]');
            if (article) {
                target = article;
            }
        });
        target.querySelector("div").scrollIntoView();
        return target;
    };
    const getStory = async () => {
        console.log("Extracting STORY");
        function delay(ms) {
            return new Promise((resolve) => setTimeout(resolve, ms));
        }

        const viewStoryButton = document
            .querySelector('[data-pagelet="StoriesContentPane"]')
            .querySelector(
                '[class="x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k xh8yej3"]'
            );
        if (viewStoryButton) viewStoryButton.click();

        // wait until story is loaded. it's about half a second. but it WILL load
        await delay(1000);

        let storyPause = document
            .querySelector('[data-pagelet="StoriesContentPane"]')
            .querySelector(
                '[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1n2onr6 x87ps6o x1lku1pv x1a2a7pz"]'
            );
        if (storyPause) storyPause.click();

        const storySelectors = ['[data-pagelet="StoriesCardMedia"]'];

        for (const selector of storySelectors) {
            const story = document.querySelector(selector);
            if (story) {
                console.log("STORY: ", story);
                return story;
            }
        }
    };

    const getVideoPost = () => {
        let watchPerm = document.querySelector(
            '[data-pagelet="WatchPermalinkVideo"]'
        );
        return watchPerm.parentElement.parentElement;
    };

    const pageType = getPageType();
    if (pageType === "profile" || pageType === "unknown") {
        return fallbackSingleLayerError();
    }

    if (pageType === "story") {
        const story = await getStory();
        return story;
    }
    if (pageType === "post") {
        removeCommentAs();
        // try to get dialog post
        const dialogPost = getDialogPost();
        if (dialogPost) return dialogPost;

        // try to get video post
        const videoPost = getVideoPost();
        if (videoPost) return videoPost;

        // try to get group post
        const groupPost = getGroupPost();
        if (groupPost) return groupPost;

        return null;
    }

    let profileNavTabs = document.querySelector('[data-pagelet="ProfileTabs"]');
    if (profileNavTabs) {
        return fallbackSingleLayerError();
    }

    return fallbackSingleLayerError();
};

const parseProfile = async () => {
    document.body.style.fontFamily = "'Roboto', sans-serif";
    if (getPageType() !== "profile") return null;

    const removeBanner = () => {
        let banner = document.querySelector('[role="banner"]');
        if (banner) banner.remove();
        let main = document.querySelector('[role="main"]');
        let secondary =
            main.parentElement.parentElement.parentElement.parentElement;
        secondary.style.position = "relative";
        secondary.style.top = "0px";
    };

    removeBanner();
    removeCommentAs();
    document.body.style.zoom = "120%";
    return document.body;
};

// EXTRACT PROFILE URL
const extractProfileURL = async () => {
    console.log("extracting profile URL");
    const pageType = getPageType();
    if (pageType === "profile") return window.location.href;
    if (pageType === "post") {
        const post = await parsePost();
        const anchorTags = post.querySelectorAll("a");
        return anchorTags[1].href;
    }
    if (pageType === "story") {
        const story = await parsePost();
        // const anchorTag = story.querySelector("a");
        let aTag = document.querySelector(
            '[class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1rg5ohu x1a2a7pz x193iq5w"]'
        );
        return aTag.href;
    }
};
