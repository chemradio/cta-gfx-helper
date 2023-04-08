<script>
  import { handleUserSubmit } from "../../tools/login";

  let email = "";
  let password = "";
  let error = "";

  const handleSubmit = async () => {
    console.log("before fetch");
    const user = await handleUserSubmit(email, password);
    console.log("after fetch");
    console.log(user);
    if (user) {
      error = "Successfully logged in.";
      window.location.href = "/";
    } else {
      error = "Invalid credentials.";
      password = "";
    }
    return;
  };
</script>

<div class="card border-primary">
  <form id="registerForm" on:submit={handleSubmit}>
    <div class="card-header">
      <h5>Вход</h5>
      <small>Если ты уже зарегистрирован</small>
    </div>
    <div class="card-body">
      <div class="row mb-3">
        <label for="email">
          Email
          <input type="text" class="form-control" bind:value={email} />
        </label>
      </div>
      <div class="row mb-3">
        <label for="email"
          >Пароль
          <input type="password" class="form-control" bind:value={password} />
        </label>
      </div>
      <button class="btn btn-primary w-100" type="submit">Отправить</button>
      <small>{error}</small>
    </div>
  </form>
</div>
