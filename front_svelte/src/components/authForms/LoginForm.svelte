<script>
    import { enhance } from "$app/forms";
    import toast from "svelte-french-toast";
    export let form;
    let loading = false;
    const submitLoginUser = async ({ form, data, action, cancel }) => {
        // const { email, password } = Object.fromEntries(data.entries());
        return async ({ result, update }) => {
            loading = true;
            switch (result.data?.status) {
                case "error":
                    toast.error(result.data.message);
                    await update();
                    break;
                default:
                    toast.success("Successfully logged in");
                    break;
            }
            loading = false;
            window.location.href = "/";
            // await update();
        };
    };
</script>

<div class="card bg-secondary rounded-0">
    <form
        method="POST"
        action="/login?/login"
        id="loginForm"
        use:enhance={submitLoginUser}
    >
        <div class="card-header">
            <h5>Вход</h5>
            <small>Если ты уже зарегистрирован</small>
        </div>
        <div class="card-body">
            <div class="row mb-3">
                <label for="login_email">
                    Email
                    <input
                        name="login_email"
                        type="text"
                        class="form-control rounded-0 {form?.errors?.login_email
                            ? 'border-danger'
                            : ''}"
                        value={form?.data?.login_email ?? ""}
                        disabled={loading}
                    />
                    {#if form?.errors?.login_email}
                        <small class="text-danger"
                            >{form.errors.login_email[0]}</small
                        >
                    {/if}
                </label>
            </div>

            <div class="row mb-3">
                <label for="login_password"
                    >Пароль
                    <input
                        name="login_password"
                        type="password"
                        disabled={loading}
                        class="form-control rounded-0 {form?.errors
                            ?.login_password
                            ? 'border-danger'
                            : ''}"
                    />
                    {#if form?.errors?.login_password}
                        <small class="text-danger"
                            >{form.errors.login_password[0]}</small
                        >
                    {/if}
                </label>
            </div>
            <button
                disabled={loading}
                class="btn btn-primary w-100 rounded-0"
                type="submit">Отправить</button
            >
        </div>
    </form>
</div>
