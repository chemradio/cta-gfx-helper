const getPageType = () => {
    const postDetectors = ['[id="wk_summary"]', '[id="wk_content"]'];
    const profileDetectors = [
        '[class="ProfileInfo"]',
        '[class="ProfileHeader__actions"]',
        '[id="profile_skeleton"]',
    ];
    const secondaryPostDetectors = [
        '[class="post_content"]',
        '[class="post_info"]',
        '[class="_post_content"]',
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
        console.log("Page type: POST");
        return "post";
    }
    if (isInCategory(profileDetectors)) {
        console.log("Page type: PROFILE");
        return "profile";
    }
    if (isInCategory(secondaryPostDetectors)) {
        console.log("Page type: POST");
        return "post";
    }
    return "unknown";
};

const removeBanners = () => {
    const banners = [
        '[id="page_bottom_banners_root"]',
        '[class="PageBottomBanner__in"]',
        '[id="box_layer_bg"]',
        '[id="box_layer_wrap"]',
    ];
    for (const banner of banners) {
        const element = document.querySelector(banner);
        if (element) element.remove();
    }
};

const parsePost = async () => {
    const pageType = getPageType();
    if (pageType !== "post") return null;

    const postSelectors = [
        '[id="wl_post"]',
        '[id="wk_content"]',
        '[class="_post_content"]',
    ];

    let post;
    for (const selector of postSelectors) {
        post = document.querySelector(selector);
        if (post) break;
    }

    removeBanners();
    return post;
};

const parseProfile = async () => {
    if (getPageType() !== "profile") return null;
    removeBanners();
    document.body.style.zoom = "120%";
    return document.body;
};

const extractProfileURL = async () => {
    console.log("extracting profile URL");
    const pageType = getPageType();
    if (pageType === "profile") return window.location.href;
    if (pageType === "post") {
        const linkSelectors = [
            '[data-task-click="Post/ownerLinkClick"]',
            '[class="PostHeaderTitle__authorLink"]',
        ];
        for (const selector of linkSelectors) {
            const link = document.querySelector(selector);
            if (link) return link.href;
        }
    }
};
