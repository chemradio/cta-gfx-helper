export const getPageType = () => {
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
                // console.log(element);
                return true;
            }
        }
        return false;
    };

    if (isInCategory(postDetectors)) {
        console.log("Page type: POST");
        return "post";
    }
    if (isInCategory(storyDetectors)) {
        console.log("Page type: STORY");
        return "story";
    }
    if (isInCategory(profileDetectors)) {
        console.log("Page type: PROFILE");
        return "profile";
    }
    console.log("Page type: UNKNOWN");
    return "unknown";
};

export const removeObscuringElements = () => {
    targetSelectors = ["[class='x1n2onr6 xzkaem6']"];
    for (const selector of targetSelectors) {
        const element = document.querySelector(selector);
        if (element) {
            element.remove();
        }
    }
};
export const parsePost = async () => {
    document.body.style.fontFamily = "'Roboto', sans-serif";
    const getPost = () => {
        console.log("Extracting POST");
        const postDetectors = [
            "article",
            ".x6s0dn4.x78zum5.xdt5ytf.xdj266r.xkrivgy.xat24cr.x1gryazu.x1n2onr6.xh8yej3",
            ".x1yvgwvq .x1dqoszc .x1ixjvfu .xhk4uv .x13fuv20 .xu3j5b3 .x1q0q8m5 .x26u7qi .x178xt8z .xm81vs4 .xso031l .xy80clv .x78zum5 .x1q0g3np .xh8yej3",
        ];
        let postElement;
        for (const selector of postDetectors) {
            const post = document.querySelector(selector);
            if (post) {
                console.log("POST: ", post);
                postElement = post;
            }
        }
        postElement.style.border = "0px";

        // remove comment as
        // element is a section with class="x5ur3kl x178xt8z x1roi4f4 x2lah0s xvs91rp xl56j7k x17ydfre x1n2onr6 x1qiirwl xh8yej3 x1ejq31n xd10rxx x1sy0etr x17r0tee x3hdcf8 x180j4jr x18dplov x1ub4b5r"
        const commentAs = postElement.querySelector(
            'section[class="x5ur3kl x178xt8z x1roi4f4 x2lah0s xvs91rp xl56j7k x17ydfre x1n2onr6 x1qiirwl xh8yej3 x1ejq31n xd10rxx x1sy0etr x17r0tee x3hdcf8 x180j4jr x18dplov x1ub4b5r"]'
        );
        commentAs?.remove();
        postElement.firstElementChild.style.border = "0px";
        return postElement;
    };
    async function getStory() {
        console.log("Extracting STORY");
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
        // may not exist.
        let storyPause = document.querySelector(
            '[aria-label="Pause"]'
        )?.parentElement;
        if (storyPause) {
            console.log("pause button found");

            storyPause.click();
        }

        const storySelectors = [
            ".x5yr21d .x1n2onr6 .xh8yej3",
            '[referrerpolicy="origin-when-cross-origin"]',
        ];

        for (const selector of storySelectors) {
            const story = document.querySelector(selector);
            if (story) {
                console.log("STORY: ", story);
                return story;
            }
        }
    }
    removeObscuringElements();

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

export const parseProfile = async () => {
    document.body.style.fontFamily = "'Roboto', sans-serif";
    if (getPageType() !== "profile") return null;

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

export const extractProfileURL = async () => {
    console.log("extracting profile URL");
    const pageType = getPageType();
    if (pageType === "profile") return window.location.href;
    if (pageType === "post") {
        const post = await parsePost();
        const anchorTag = post.querySelector("a");
        return anchorTag.href;
    }
    if (pageType === "story") {
        const story = await parsePost();
        const anchorTag = story.querySelector("a");
        return anchorTag.href;
    }
};
