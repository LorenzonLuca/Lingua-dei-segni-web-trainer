<script lang="ts">
	import AuthTemplate from "$lib/components/AuthTemplate.svelte";
	import { getToastStore, type ToastSettings } from "@skeletonlabs/skeleton";
	import type { ActionData } from "./$types";
    
    const toastStore = getToastStore();

    export let form: ActionData;
    $: showError(form)

    function showError(form: ActionData){
        if(form?.msg){
            const t: ToastSettings = {
                message: form.msg,
                timeout: 3000,
                background: 'variant-filled-error',
            }
            toastStore.trigger(t);
        }
    }
</script>


<AuthTemplate title={'Accedi'}>
    <form method="post">
        <label class="label mt-3">
            <span>Nome utente:</span>
            <input class="input" type="text" placeholder="Nome utente..." name="username"/>
        </label>
        <label class="label mt-3">
            <span>Password:</span>
            <input class="input" type="password" placeholder="Password..." name="password"/>
        </label>
        <button type="submit" class="btn variant-filled-primary mt-6">Accedi</button>
    </form>
    <div class="pt-5">
        <a href="/register" class="text-tertiary-500">Non hai un account? Registrati qua</a>
        <br>
        <a href="/" class="text-tertiary-500">Continua senza registrarti</a>
    </div>
</AuthTemplate>