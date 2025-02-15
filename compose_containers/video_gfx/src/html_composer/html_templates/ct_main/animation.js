const checkElementsReady = setInterval(() => {
    if (window.elementsReady) {
        console.log("elements ready");
        clearInterval(checkElementsReady);
        fetch("./config.json")
            .then((response) => response.json())
            .then((json) => create_animation(json));
    }
}, 100);

function create_animation(config) {
    document.querySelector("body").addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            // animation
            const TAIL = 2;
            const SCROLLDURATION = config.animationDuration + TAIL;
            const ZOOMDURATION_BGONLY = 2;
            const ONLYBGOVERLAP = 1;
            const BG_SCROLLSPEED_PX = 50;
            const BG_SCROLLAMOUNT = BG_SCROLLSPEED_PX * SCROLLDURATION;

            timeline = gsap.timeline({ defaults: { duration: 1 } });

            timeline.pause();
            timeline
                // background scroll
                .to(
                    ".bgScroll",
                    {
                        duration: SCROLLDURATION,
                        y: `${-1 * (BG_SCROLLAMOUNT / 2)}px`,
                    },
                    0
                )
                // background zoom
                .from(".bgZoom", { duration: SCROLLDURATION, scale: 1.2 }, 0)

                // background only
                .to(
                    ".bgOnly",
                    {
                        duration: ZOOMDURATION_BGONLY,
                        scale: 1.1,
                        ease: "power4.out",
                    },
                    0
                )
                .to(
                    ".bgOnly",
                    {
                        duration: SCROLLDURATION - ONLYBGOVERLAP,
                        y: `${-1 * BG_SCROLLAMOUNT * 0.6}px`,
                        ease: CustomEase.create(
                            "custom",
                            "M0,0,C0.142,0,1,1,1,1"
                        ),
                    },
                    ZOOMDURATION_BGONLY - ONLYBGOVERLAP
                )

                // foil wipe
                .from(".midnightFoil", { y: "1080px", ease: "power3.out" }, 0)

                // foreground wipe
                .from(
                    ".foreground-container",
                    {
                        duration: 1.2,
                        "clip-path": "inset(0% 0% 100% 0%)",
                        ease: "power3.out",
                    },
                    0.2
                )

                // foreground scroll
                .to(".fgScroll", { duration: SCROLLDURATION, y: "-200px" }, 0.2)
                // foreground zoom
                .to(".fgZoom", { duration: SCROLLDURATION, scale: 1.1 }, 0.2)

                // quote box wipe
                .from(
                    ".quote-box",
                    { "clip-path": "inset(0% 0% 100% 0%)", ease: "power1.out" },
                    0.5
                )

                // quote box wipe off
                .to(
                    ".quote-box",
                    { "clip-path": "inset(100% 0% 0% 0%)", ease: "power1.out" },
                    SCROLLDURATION - TAIL - 1
                );

            // tail
            // .to('tail-nonexistent', {duration: TAIL, y:'1100px'}, SCROLLDURATION);
        }
    });
    document.querySelector("body").addEventListener("click", () => {
        timeline.progress(0);
        timeline.resume();
    });
}
