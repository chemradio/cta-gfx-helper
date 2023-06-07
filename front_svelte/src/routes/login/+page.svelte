<script>
    import { onMount } from "svelte";
    import toast from "svelte-french-toast";
    import LoginForm from "../../components/authForms/LoginForm.svelte";
    import RegisterForm from "../../components/authForms/RegisterForm.svelte";
    export let form;
    export let data;

    onMount(() => {
        toast.success(data?.message, { icon: "🔐" });
    });
</script>

<a
    href={`/downloads?filename=temp.mp4`}
    class="btn btn-primary rounded-0 align-self-center">test</a
>
<div class="row d-flex justify-content-center">
    <div class="col col-s-12 col-md-10">
        <div class="mb-3"><LoginForm {form} /></div>
        <br />
        <h3>Или</h3>
        <br />
        <div class=""><RegisterForm {form} /></div>
    </div>
</div>
