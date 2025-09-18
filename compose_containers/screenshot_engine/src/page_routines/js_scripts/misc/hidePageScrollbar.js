function hidePageScrollbarGeneric() {
    const html = document.documentElement;
    const body = document.body;
    html.style.setProperty("overflow", "hidden", "important");
    body.style.setProperty("overflow", "hidden", "important");
}

function hidePageScrollbarMetaFacebookInstagram() {
    document.body.querySelector("div").style.overflow = "hidden";
}

function hidePageScrollbar() {
    hidePageScrollbarGeneric();
    if (
        window.location.hostname.includes("facebook.com") ||
        window.location.hostname.includes("instagram.com") ||
        window.location.hostname.includes("threads.com")
    ) {
        hidePageScrollbarMetaFacebookInstagram();
    }
}

hidePageScrollbar();
