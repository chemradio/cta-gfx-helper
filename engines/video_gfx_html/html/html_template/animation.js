fetch('./config.json')
    .then(response => response.json())
    .then(json => create_animation(json));


function create_animation(config) {
    // animation
    const SCROLLDURATION = config.animationDuration;
    const ZOOMDURATION_BGONLY = 2;
    timeline = gsap.timeline({defaults: {duration:1}});
    
    timeline.pause()
    timeline
        // background scroll
        .to('.bgScroll', {duration: SCROLLDURATION, y: '-500px'}, 0)
        // background zoom
        .to('.bgZoom', {duration: SCROLLDURATION, scale: .9}, 0)
        // background only
        .to('.bgOnly', {duration: ZOOMDURATION_BGONLY, scale: 1.1,ease:"power4.out"}, 0)
        .to('.bgOnly', {duration: SCROLLDURATION, y: '-500px'}, ZOOMDURATION_BGONLY)
    
    
        // foil wipe
        .from('.midnightFoil', {y: '1080px', ease: "power3.out"}, 0)
    
        // foreground wipe
        .from('.foreground-container', {duration: 1.2, "clip-path": "inset(0% 0% 100% 0%)", ease: "power3.out"}, .2)
    
        // foreground scroll
        .to('.facebook', {duration: SCROLLDURATION, y: '-200px'}, .2)
        // foreground zoom
        .to('.twitter, .document, .instagram, .photo', {duration: SCROLLDURATION, scale: 1.2}, .2)
    
    
        // quote box wipe
        .from('.quote-box', {"clip-path": "inset(0% 0% 100% 0%)", ease:"power1.out"}, .5)
    
        // quote box wipe off
        .to('.quote-box', {"clip-path": "inset(100% 0% 0% 0%)", ease:"power1.out"}, "<5");
}