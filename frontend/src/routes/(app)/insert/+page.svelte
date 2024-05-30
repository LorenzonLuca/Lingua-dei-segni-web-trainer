<script lang="ts">
    import CameraPhoto from "$lib/components/Cameras/CameraPhoto.svelte";
    import FileUploader from "$lib/components/FileUploader.svelte";
    import Icon from '@iconify/svelte';
	import type { PageData } from "./$types";
    import { goto } from "$app/navigation";
    import { onMount } from 'svelte';
    import {insertStore} from '$lib/stores'
	import ConfirmButton from "$lib/components/ConfirmButton.svelte";
	import PageTemplate from "$lib/components/PageTemplate.svelte";

    export let data: PageData

	let img: string | undefined = undefined;
    let startWebcam: boolean = false;

    onMount(() => {
        if(data.user?.admin != 1){
            goto('/')
        }
    })

    function insertData(){
        insertStore.set(img);
        goto('/insert/data');
    }
</script>

<PageTemplate title="Inserisci">
    <div slot="desc">
        {#if !startWebcam && img == undefined}
            Per poter riconoscere i gesti bisogna registrarli. I gesti con i rispettivi significati si possono trovare sul seguente sito:
            <a href="https://www.sgb-fss.ch/signsuisse/it/assistente-di-ricerca-dal-segno" target="_blank" class="text-tertiary-500">https://www.sgb-fss.ch/signsuisse/it/assistente-di-ricerca-dal-segno</a>
        {/if}
    </div>
    <div class="space-y-12 text-center flex flex-col items-center w-full md:w-2/3">
        {#if img === undefined}
            {#if startWebcam}
                <CameraPhoto bind:startWebcam bind:img/>
            {:else}
                <button class="btn btn-lg variant-filled-secondary text-base md:text-lg w-full md:w-auto" on:click={() => startWebcam=true}>
                    <Icon icon="mdi:camera" class="mr-2" width="30"/>
                    Scatta una foto
                </button>
                <p class="text-xl">oppure</p>
                <FileUploader bind:img />
            {/if}
        {:else}
            <div class="flex flex-wrap flex-row justify-center w-full md:w-4/5">
                <div class="w-full space-y-3">
                    <img src={img} alt="uploaded">
                    <div class="flex flex-wrap flex-row w-full space-y-5 md:space-y-0">
                        <ConfirmButton func={() => img = undefined} buttonText="Cambia immagine" icon="mdi:trash" modalBody="Sei sicuro di voler cambiare l'immagine?" style="w-full md:w-1/2"/>
                        <button class="btn btn-lg variant-filled-success w-full md:w-1/2" on:click={insertData}>
                            <Icon icon="mdi:check" class="mr-2" width="30"/>
                            Procedi
                        </button> 
                    </div>
                </div>
            </div>
        {/if}
    </div>
</PageTemplate>