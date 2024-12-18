const profileDetectors = [
    '[aria-label="Home timeline"]',
    '[data-testid="UserDescription"]',
    '[aria-label="Profile timelines"]',
];

const allAria = document.querySelectorAll("[aria-label]");
for (const aria of allAria) {
    console.log(aria.getAttribute("aria-label"));
}
