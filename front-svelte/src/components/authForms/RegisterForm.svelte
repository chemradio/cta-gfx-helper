<script>
  const handleSubmit = () => {};
</script>

<div class="card border-warning">
  <form id="registerForm" on:submit={handleSubmit}>
    <div class="card-header">
      <h5>Регистрация</h5>
      <small>Получи кодовое слово у администратора</small>
    </div>
    <div class="card-body">
      <div class="row mb-2">
        <label for="email">
          Email
          <input type="text" class="form-control" />
        </label>
      </div>
      <div class="row mb-2">
        <label for="email">
          Пароль
          <input type="password" class="form-control" />
        </label>
      </div>
      <div class="row mb-2">
        <label for="passphrase">
          Кодовое слово
          <input type="password" class="form-control" />
        </label>
      </div>
      <button class="btn btn-primary mb-2 w-100" type="submit">Отправить</button
      >
    </div>
  </form>
</div>
