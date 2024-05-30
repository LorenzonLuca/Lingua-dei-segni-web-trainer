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


<AuthTemplate title={'Registrati'}>
    <form method="post">
        <label class="label mt-3">
            <span>Nome utente:</span>
            <input class="input" type="text" placeholder="Nome utente..." name="username"/>
        </label>
        <label class="label mt-3">
            <span>Password:</span>
            <input class="input" type="password" placeholder="Password..." name="password"/>
        </label>
        <label class="label mt-3">
            <span>Conferma Password:</span>
            <input class="input" type="password" placeholder="Conferma password..." name="password2"/>
        </label>
        <button type="submit" class="btn variant-filled-primary mt-6">Registrati</button>
    </form>
    <div class="pt-5">
        <a href="/login" class="text-tertiary-500">Hai già un account? Esegui l'accesso qua</a>
        <br>
        <a href="/" class="text-tertiary-500">Continua senza registrarti</a>
    </div>
</AuthTemplate>