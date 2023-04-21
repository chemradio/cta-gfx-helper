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

<div class="row d-flex justify-content-center">
    <div class="col col-s-12 col-md-10">
        <h5>{JSON.stringify(data)}</h5>
        <div class="mb-3"><LoginForm {form} /></div>
        <br />
        <h3>Или</h3>
        <br />
        <div class=""><RegisterForm {form} /></div>
        <h5>{JSON.stringify(form?.data)}</h5>
    </div>
</div>
