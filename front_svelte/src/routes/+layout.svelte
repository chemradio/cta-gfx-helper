<!-- <script context="module"> -->
<script>
  import Header from "./Header.svelte";
  import "./styles.css";
  export let data;
  let loggedIn = data.user ? true : false;
</script>

<div class="body-main">
  <Header {loggedIn} />

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
