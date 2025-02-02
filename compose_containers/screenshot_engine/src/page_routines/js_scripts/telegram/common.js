const getPageType = () => {
    const postDetectors = [
        "iframe",
        '[class="tgme_page_widget_actions_wrap"]',
        '[class="tgme_page_widget_actions"]',
        '[class="tgme_page_widget_wrap"]',
        '[class="tgme_page tgme_page_post"]',
    ];
    const profileDetectors = [
        '[class="tgme_channel_info"]',
        '[class="tgme_header_search"]',
        '[class="tgme_header search_collapsed"]',
        '[class="tgme_header_right_column"]',
        '[class="tgme_header_info"]',
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

const parsePost = async () => {
    const pageType = getPageType();
    if (pageType !== "post") return null;

    // get the iframe which contains the telegram post
    iframe = document.querySelector("iframe");
    iframe.style.padding = "0px";

    avatar = iframe.contentWindow.document.querySelector(
        ".tgme_widget_message_user"
    );
    if (avatar) avatar.remove();
    element = iframe.contentWindow.document.querySelector(
        ".tgme_widget_message_bubble"
    );
    element.style.border = "0";
    element.style.borderRadius = "0px";
    element.style.margin = "0px";

    iframe.style.padding = "0px";
    iframe.style.margin = "0px";
    iframe.style.border = "0px";
    // remove the small tail leading to author profile picture
    bubbleTail = iframe.contentWindow.document.querySelector(
        ".tgme_widget_message_bubble_tail"
    );
    if (bubbleTail) bubbleTail.parentNode.removeChild(bubbleTail);

    // remove the inner padding of the message bubble to iframe
    messageWidget =
        iframe.contentWindow.document.querySelector(".js-widget_message");
    messageWidget.style.padding = "0px";

    const parent1 = iframe.parentElement;
    const parent2 = parent1.parentElement;

    [parent1, parent2].forEach((element) => {
        if (element) {
            element.style.padding = "0px";
            element.style.margin = "0px";
            element.style.border = "0px";
        }
    });

    return iframe;
};

const parseProfile = async () => {
    if (getPageType() !== "profile") return null;
    document.body.style.zoom = "130%";
    return document.body;
};

const extractProfileURL = async () => {
    console.log("extracting profile URL");
    const pageType = getPageType();
    if (pageType === "profile") return window.location.href;
    if (pageType === "post") {
        const profileLink = document.querySelector(
            'a[class="tgme_action_button_new"]'
        ).href;
        return profileLink;
    }
};
