<script lang="ts">
	import { goto } from '$app/navigation';
    import {insertStore, basePosStore, wordsStore} from '$lib/stores'
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
    import Icon from '@iconify/svelte';
	import  { type ModalSettings, getModalStore, type ToastSettings } from '@skeletonlabs/skeleton';
	import axios, { type AxiosRequestConfig } from 'axios';
    import { getSignImage } from '$lib/utils';
	import ConfirmButton from '$lib/components/ConfirmButton.svelte';
	import PageTemplate from '$lib/components/PageTemplate.svelte';
    import { getToastStore } from '@skeletonlabs/skeleton';

    const toastStore = getToastStore();

    const modalStore = getModalStore();
    let insertImg: string | undefined;
    insertStore.subscribe((value) =>{
        insertImg = value;
    })

    export let data: PageData

    onMount(() =>{
        if(data.user?.admin != 1){
            goto('/')
        }
        if (insertImg === "") {
            goto('/insert')
        }
    })

    let basePos: any = undefined;
    let signPos: any = undefined;
    let words: Array<Word> | undefined = undefined;

    function basePositionModal(){
        new Promise<any>((resolve) => {
            const modal: ModalSettings = {
                type: 'component',
                component: 'basePosModal',
                response: (r: any) => {
                    resolve(r);
                }
            };
            modalStore.trigger(modal);
        }).then((r: any) => {
            if(r == undefined){
                return;
            }
            basePos = r;
            signPos = undefined;
        });
    }

    function signPositionModal(){
        new Promise<any>((resolve) => {
            const modal: ModalSettings = {
                type: 'component',
                component: 'signModal',
                response: (r: any) => {
                    resolve(r);
                }
            };
            modalStore.trigger(modal);
        }).then((r: any) => {
            if(r == undefined){
                return;
            }
            signPos = r;
        });
    }

    function wordsFormModal(){
        new Promise<any>((resolve) => {
            const modal: ModalSettings = {
                type: 'component',
                component: 'wordsForm',
                response: (r: any) => {
                    resolve(r);
                }
            };
            modalStore.trigger(modal);
        }).then((r: any) => {
            words = r;
        });
    }

    async function insertSign(){

        if(signPos == undefined || basePos == undefined || words == undefined){
            const t: ToastSettings = {
                message: 'Seleziona una posizione base, un segno e inserisci almeno un termine',
                timeout: 5000,
                background: 'variant-filled-error',
            };
            toastStore.trigger(t);
            return;
        }

        if(words.length < 1){
            const t: ToastSettings = {
                message: 'Seleziona una posizione base, un segno e inserisci almeno un termine',
                timeout: 5000,
                background: 'variant-filled-error',
            };
            toastStore.trigger(t);
            return;
        }

        let config: AxiosRequestConfig = {
            method: 'post',
            url: "?/insert",
            data: {
                "img": insertImg,
                "sign_position": signPos,
                "base_position": basePos.id,
                "words": JSON.stringify(words)
            },
            headers: { "Content-Type": "multipart/form-data" },
            }
    
        await axios(config).then((res) => {
            let m = JSON.parse(JSON.parse(res.data.data)[0])
            let isOk = m.status == 'OK';
            let bg = isOk ? 'variant-filled-success' : 'variant-filled-error';
            const t: ToastSettings = {
                message: m.msg,
                timeout: 5000,
                background: bg,
            };
            toastStore.trigger(t);
            if(isOk) resetDatas();        
        })
    }

    function resetDatas(){
        basePosStore.set(0);
        wordsStore.set([])
        basePos = undefined;
        signPos = undefined;
        words = [];
        goto('/insert');    
    }
</script>

<PageTemplate containerExtraStyle="space-y-5">
    <ConfirmButton style="w-full md:w-3/5 h-fit" buttonText="Annulla" icon="mdi:close" func={resetDatas} modalBody="Sei sicuro di voler annullare l'inserimento?"/>
    <div class="w-full md:w-3/5">
        <img src={insertImg} alt="foto selezionata"/>
    </div>
    <div class="w-full md:w-3/5 space-y-5">
        <div class="flex flex-wrap flex-col space-y-2 xl:space-y-0 xl:flex-row xl:space-x-5 xl:justify-between">
            <div class="flex flex-wrap flex-row justify-between xl:flex-col xl:justify-center items-center space-y-2 h-fit">
                <button class="btn btn-lg variant-filled-secondary text-base xl:text-lg flex w-1/2 xl:w-auto h-min" on:click={basePositionModal}>
                    <Icon icon="mdi:hand-back-left-outline" class="mr-2 hidden md:block" width="30" />
                    Posizione base
                </button>
                {#if basePos !== undefined}
                    <div class="hidden xl:block">
                        <img src={basePos.img} alt="posizione base selezionata" width="100" class="flex"/>
                    </div>
                    <div class="block xl:hidden">
                        <img src={basePos.img} alt="posizione base selezionata" width="65" class="flex"/>
                    </div>
                {/if}
            </div>
            <div class="flex flex-wrap flex-row justify-between xl:flex-col xl:justify-center items-center space-y-2 h-fit">
                <button class="btn btn-lg variant-filled-secondary text-base xl:text-lg flex w-1/2 xl:w-auto h-min" on:click={signPositionModal} disabled={!basePos}>
                    <Icon icon="mdi:hand-wave-outline" class="mr-2 hidden md:block" width="30"/>
                    Segno
                </button>
                {#if signPos !== undefined}
                    <div class="hidden xl:block">
                        <img src={getSignImage(basePos.id, signPos)} alt="posizione base selezionata" width="100" class="flex"/>
                    </div>
                    <div class="block xl:hidden">
                        <img src={getSignImage(basePos.id, signPos)} alt="posizione base selezionata" width="65" class="flex"/>
                    </div>
                {/if}
            </div>
            <div class="flex flex-wrap flex-row justify-center space-y-3 h-fit">
                <button class="btn btn-lg variant-filled-secondary text-base xl:text-lg w-full xl:w-auto" on:click={wordsFormModal}>
                    <Icon icon="mdi:text" class="mr-2" width="30" />
                    Termini
                </button>
            </div>
        </div>
        {#if words}
            <div class="flex flex-wrap flex-row justify-between xl:justify-normal w-4/5 text-base xl:text-lg">
                <p><b>Termini inseriti:</b></p>
                {#each words as w}
                    <p>{w.word}, </p>
                {/each}
            </div>
        {/if}
        <button class="btn btn-lg variant-filled-primary w-full" on:click={insertSign}>
            <Icon icon="mdi:add-circle-outline" class="mr-2" width="30" />
            Inserisci gesto
        </button>
    </div>
</PageTemplate>