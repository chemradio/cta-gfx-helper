<script>
  // import logo from '$lib/images/svelte-logo.svg';
  // import github from '$lib/images/github.svg';
  export let loggedIn;
  console.log("header reports user is logged in: ", loggedIn);
</script>

<header class="sticky-top">
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container d-flex justify-content-end">
      {#if loggedIn}
        <a class="navbar-brand" href="/logout">Logout</a>
      {:else}
        <a class="navbar-brand" href="/login">Log In</a>
      {/if}
    </div>
  </nav>
</header>
