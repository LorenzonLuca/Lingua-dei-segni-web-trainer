<script lang="ts">
    import Icon from '@iconify/svelte';
	import CameraLearn from "$lib/components/Cameras/CameraLearn.svelte";
    import { ioStore, deltasStore } from "$lib/stores";
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getLanguageImage } from '$lib/utils';
    import type { PageData } from './$types';
	import axios, { type AxiosRequestConfig } from 'axios';
	import PageTemplate from '$lib/components/PageTemplate.svelte';
	import ConfirmButton from '$lib/components/ConfirmButton.svelte';

    let io: any;
    export let data: PageData;

	ioStore.subscribe((value) =>{
		io = value;
	})

    let startWebcam: boolean = true;
    let stopTraining: any;
    let word: any = undefined;
    let signId: any = 0;
    let delta: number = 0.04;
    let qNumber: number = 0;
    let deltas: Array<WordDelta> = [];

    onMount(() =>{
		io.off();
		io.on('real_time_delta', (res: any) => {
            if(res.delta < delta){
                delta = res.delta
            }
		})
        io.on('new_word', (res: any) => {
            qNumber = res.qNumber;
            if(qNumber > 10){
                stopTraining();
                deltasStore.set(deltas);
                goto('/learn/quiz/results')
                return;
            }
			word = res;
            signId = res.sign_id
		})
		io.emit('start_recognization');
        io.emit('learn_next_word', {'wordId': -1, 'qNumber': qNumber});
	})

    function closeTraining(){
        stopTraining();
        goto('/learn');
    }

    function nextWord(){
        let config: AxiosRequestConfig = {
            method: 'post',
            url: "?/save",
            data: {
                "value": delta,
                "word": word.word_id
            },
            headers: { "Content-Type": "multipart/form-data" },
            }
    
        axios(config)
        deltas.push({word: {word: word.word, category: word.category, language: word.language, signPos: word.sign_pos, basePos: word.base_pos}, delta: delta});
        delta = 0.04;
        io.emit('learn_next_word', {'wordId': word ? word.word_id : -1, 'qNumber': qNumber});
    }
</script>

<PageTemplate>
    <div class="space-y-6 text-center flex flex-col items-center w-full md:w-2/3">
        {#if startWebcam}
            <ConfirmButton func={closeTraining} buttonText="Esci dalla modalità quiz" icon="mdi:close" style="w-full text-base md:text-lg" 
                modalBody="Sei sicuro di voler uscire dalla modalità quiz?"
            />
            {#if word}
                <div class="flex flex-wrap flex-col space-y-2 w-full hidden md:block">
                    <div class="flex flex-wrap flex-row space-x-5 h-fit items-center justify-between">
                        <img src={getLanguageImage(word.language)} alt="lingua" width="60" class="rounded-lg">
                        <p class="text-2xl"><b>Categoria: </b>{word.category}</p>
                        <p class="text-2xl"><b>Termine: </b>{word.word}</p>
                        <p class="text-2xl"><b>{qNumber}/10</b></p>
                    </div>
                </div>
                <div class="flex flex-wrap flex-col space-y-2 w-full block md:hidden">
                    <div class="flex flex-wrap flex-row h-fit w-full items-center justify-between">
                        <div class="text-left flex flex-wrap flex-col">
                            <p class="text-xl flex flex-col flex-wrap"><b>Categoria: </b>{word.category}</p>
                            <p class="text-xl flex flex-col flex-wrap"><b>Termine: </b>{word.word}</p>
                        </div>
                        <div class="flex flex-col justify-between h-full">
                            <img src={getLanguageImage(word.language)} alt="lingua" width="60" class="rounded-lg">
                            <p class="text-2xl"><b>{qNumber}/10</b></p>
                        </div>
                    </div>
                </div>
            {/if}
		    <CameraLearn io={io} bind:startWebcam bind:stopVideoCapture={stopTraining} bind:signId socketEvent={"stream_quiz"}/>
            <!-- <p class="text-2xl"><b>Precisione: </b>{(100 - (delta * 100)).toFixed(5)}%</p> -->
            <button class="btn btn-lg variant-filled-secondary w-full text-base md:text-lg" on:click={nextWord}>
                <Icon icon="mdi:arrow-right" class="mr-2" width="30"/>
                Prossimo
            </button>
        {/if}
    </div>
</PageTemplate>   