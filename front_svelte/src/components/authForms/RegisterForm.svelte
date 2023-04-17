<script>
    import { enhance } from "$app/forms";
    import toast from "svelte-french-toast";
    export let form;

    let loading = false;
    const submitRegisterUser = async ({}) => {
        return async ({ result, update }) => {
            loading = true;
            switch (result.data?.status) {
                case "error":
                    toast.error(result.data.message);
                    await update();
                    break;
                default:
                    toast.success("Successfully registered");
                    break;
            }
            loading = false;
            await update();
        };
    };
</script>

<div class="card bg-secondary rounded-0">
    <form method="POST" action="/login?/register" id="registerForm" use:enhance>
        <div class="card-header">
            <h5>Регистрация</h5>
            <small>Получи кодовое слово у администратора</small>
        </div>
        <div class="card-body">
            <div class="row mb-2">
                <label for="register_email">
                    Email
                    <input
                        name="register_email"
                        type="text"
                        disabled={loading}
                        class="form-control rounded-0 {form?.errors
                            ?.register_email
                            ? 'border-danger'
                            : ''}"
                    />
                    {#if form?.errors?.register_email}
                        <small class="text-danger"
                            >{form.errors.register_email[0]}</small
                        >
                    {/if}
                </label>
            </div>
            <div class="row mb-2">
                <label for="register_password">
                    Пароль
                    <input
                        name="register_password"
                        type="password"
                        disabled={loading}
                        class="form-control rounded-0 {form?.errors
                            ?.register_password
                            ? 'border-danger'
                            : ''}"
                    />
                    {#if form?.errors?.register_password}
                        <small class="text-danger"
                            >{form.errors.register_password[0]}</small
                        >
                    {/if}
                </label>
            </div>
            <div class="row mb-2">
                <label for="register_passphrase">
                    Кодовое слово
                    <input
                        name="register_passphrase"
                        type="password"
                        disabled={loading}
                        class="form-control rounded-0 {form?.errors
                            ?.register_passphrase
                            ? 'border-danger'
                            : ''}"
                    />
                    {#if form?.errors?.register_passphrase}
                        <small class="text-danger"
                            >{form.errors.register_passphrase[0]}</small
                        >
                    {/if}
                </label>
            </div>

            <button
                disabled={loading}
                class="btn btn-primary rounded-0 mb-2 w-100"
                type="submit">Отправить</button
            >
        </div>
    </form>
</div>
