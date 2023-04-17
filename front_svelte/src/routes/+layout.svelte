<!-- <script context="module"> -->
<script>
    import { Toaster } from "svelte-french-toast";
    import "./styles.css";
    export let data;
    let loggedIn = data.user ? true : false;
</script>

<Toaster />

<div class="body-main">
    {#key data}
        <header class="sticky-top">
            <nav class="navbar bg-primary navbar-expand-lg">
                <div class="container d-flex justify-content-center">
                    {#if loggedIn}
                        <a
                            data-sveltekit-preload-data="tap"
                            class="navbar-brand text-white ml-5 mr-5"
                            href="/orders">Orders</a
                        >
                        <a
                            data-sveltekit-preload-data="tap"
                            class="navbar-brand text-white ml-5 mr-5"
                            href="/logout">Logout</a
                        >
                    {:else}
                        <a
                            data-sveltekit-preload-data="tap"
                            class="navbar-brand text-white ml-5 mr-5"
                            href="/login">Log In</a
                        >
                    {/if}
                </div>
            </nav>
        </header>
    {/key}

    <main>
        <div class="container mt-5 mx-auto col-md-6">
            <slot />
        </div>
    </main>

    <footer>
        <!-- <p>visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to learn SvelteKit</p> -->
    </footer>
</div>
