const getPageType = () => {
    const postDetectors = [
        ".x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6",
        ".x1a2a7pz.x1n2onr6",
        ".x1n2onr6.x1f9n5g.x17dsfyh.xzzag5r.x1losyl9.xsag5q8.x1iorvi4.x1sqbtui",
    ];

    const profileDetectors = [
        ".x1a8lsjc.xyamay9.x8tz501.x1rdv6da.xs4q6k7.xm3mpkm",
        ".x6s0dn4.x78zum5.x1c4vz4f.x1ws5yxj.x13fj5qh",
        // 'svg[aria-label="Instagram"]',
    ];

    const isInCategory = (category) => {
        for (const selector of category) {
            const element = document.querySelector(selector);
            if (element) {
                // console.log(selector);
                // console.log(element);
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

    console.log("Page type: UNKNOWN");
    return "unknown";
};

const parsePost = async () => {
    const getPost = () => {
        console.log("Extracting POST");
        const postDetectors = [
            ".x1n2onr6.x1f9n5g.x17dsfyh.xzzag5r.x1losyl9.xsag5q8.x1iorvi4.x1sqbtui",
            ".x1a2a7pz.x1n2onr6",
        ];
        let postElement;
        for (const selector of postDetectors) {
            const post = document.querySelector(selector);
            if (post) {
                console.log("POST: ", post);
                postElement = post;
                break;
            }
        }
        postElement.style.paddingTop = "24px";
        return postElement;
    };

    const pageType = getPageType();
    if (pageType === "post") {
        return await getPost();
    } else if (pageType === "profile") {
        throw new Error("Page is a profile, not a post or story");
    } else {
        throw new Error("Unknown page type");
    }
};

const parseProfile = async () => {
    if (getPageType() !== "profile") return null;
    // document.body.style.zoom = "210%";
    document.body.style.zoom = "150%";
    return document.body;
};

const extractProfileURL = async () => {
    console.log("extracting profile URL");
    const pageType = getPageType();
    if (pageType === "profile") return window.location.href;
    if (pageType === "post") {
        const post = await parsePost();
        const anchorTag = post.querySelector("a");
        return anchorTag.href;
    }
};
