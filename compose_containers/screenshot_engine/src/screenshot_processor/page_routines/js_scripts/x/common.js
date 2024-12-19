const getPageType = () => {
    const profileDetectors = [
        // '[aria-label="Home timeline"]',
        '[data-testid="UserDescription"]',
        '[aria-label="Profile timelines"]',
    ];

    const postDetectors = [
        '[aria-label="Timeline: Conversation"]',
        'article[role="article"]',
        '[data-testid="tweet"]',
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
    if (isInCategory(postDetectors)) {
        console.log("Page type: POST");
        return "post";
    }
    return "unknown";
};

const removePersonal = () => {
    const selectors = [
        'a[href="/chemradio"]',
        '[aria-label="Trending"]',
        '[aria-label="Account menu"]',
        '[class="css-175oi2r r-1h8ys4a r-1mmae3n"]',
        '[class="css-175oi2r r-1bimlpy r-f8sm7e r-m5arl1 r-16y2uox r-14gqq1x"]',
        '[class="css-175oi2r r-1bimlpy r-f8sm7e r-m5arl1 r-1p0dtai r-1d2f490 r-u8s1d r-zchlnj r-ipm5af"]',
    ];

    for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        for (const element of elements) {
            if (element) element.remove();
        }
    }
};

const parsePost = async () => {
    const pageType = getPageType();
    if (pageType !== "post") return null;
    removePersonal();

    let post;
    const selectors = [
        "article[tabindex='-1']",
        'article[role="article"]',
        '[data-testid="tweet"]',
    ];
    for (const selector of selectors) {
        post = document.querySelector(selector);
        if (post) return post;
    }
};

const parseProfile = async () => {
    if (getPageType() !== "profile") return null;
    removePersonal();
    return document.body;
};

const extractProfileURL = async () => {
    console.log("extracting profile URL");
    const pageType = getPageType();
    if (pageType === "profile") return window.location.href;
    if (pageType === "post") {
        const linkSelectors = [
            '[class="css-175oi2r r-1pi2tsx r-13qz1uu r-o7ynqc r-6416eg r-1ny4l3l r-1loqt21"]',
            '[class="css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21"]',
        ];
        for (const selector of linkSelectors) {
            const link = document.querySelector(selector);
            if (link) return link.href;
        }
    }
};

await parsePost();
