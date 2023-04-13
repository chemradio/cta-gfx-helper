<!-- <script context="module"> -->
<script>
    import { Toaster } from "svelte-french-toast";
    import "./styles.css";
    export let data;
    let loggedIn = data.user ? true : false;
</script>

<Toaster />

<div class="body-main">
    <header class="sticky-top">
        <nav class="navbar navbar-expand-lg">
            <div class="container d-flex justify-content-end">
                {#if loggedIn}
                    <a
                        data-sveltekit-preload-data="tap"
                        class="navbar-brand text-white"
                        href="/logout">Logout</a
                    >
                {:else}
                    <a
                        data-sveltekit-preload-data="tap"
                        class="navbar-brand text-white"
                        href="/login">Log In</a
                    >
                {/if}
            </div>
        </nav>
    </header>

    <main>
        <div class="container mt-5 mx-auto col-md-6">
            <slot />
        </div>
    </main>

    <footer>
        <div class="footer-main">something</div>
        <!-- <p>visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to learn SvelteKit</p> -->
    </footer>
</div>
