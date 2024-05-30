<script lang="ts">
    import Icon from '@iconify/svelte';
	import CameraLearn from "$lib/components/Cameras/CameraLearn.svelte";
    import { ioStore } from "$lib/stores";
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getLanguageImage, getSignImage } from '$lib/utils';
	import PageTemplate from '$lib/components/PageTemplate.svelte';

    let io: any;

	ioStore.subscribe((value) =>{
		io = value;
	})

    let startWebcam: boolean = true;
    let stopTraining: any;
    let word: any = undefined;
    let signId: any = 0;
    let unlockButton: boolean = false;
    let msg: string = "";

    $: msgColor = unlockButton ? 'text-success-500' : 'text-error-500';

    onMount(() =>{
		io.off();
		io.on('real_time_learn_msg', (res: any) => {
            if(unlockButton) return;
            switch(res.msg){
                case 'OK':
                    unlockButton = true;
                    msg = "Gesto corretto";
                    break;
                case 'NOK':
                    msg = "Gesto sbagliato";
                    break;
            }
		})
        io.on('new_word', (res: any) => {
			word = res;
            signId = res.sign_id
		})
		io.emit('start_recognization');
        nextWord();
	})

    function closeTraining(){
        stopTraining();
        goto('/learn');
    }

    function nextWord(){
        unlockButton = false;
        msg = "";
        io.emit('learn_next_word', {'wordId': word ? word.word_id : -1});
    }
</script>

<PageTemplate>
    <div class="space-y-6 text-center flex flex-col items-center w-full md:w-2/3">
        {#if startWebcam}
            <button class="btn btn-lg variant-filled-error w-full text-base md:text-lg" on:click={closeTraining}>
                <Icon icon="mdi:close" class="mr-2" width="30"/>
                Esci dalla modalità di allenamento
            </button>
            {#if word}
                <div class="flex flex-wrap flex-col space-y-2 w-4/5 hidden md:block">
                    <div class="flex flex-wrap flex-row space-x-5 h-fit items-center">
                        <img src={getLanguageImage(word.language)} alt="lingua" width="60" class="rounded-lg">
                        <p class="text-2xl"><b>Categoria: </b>{word.category}</p>
                        <p class="text-2xl"><b>Termine: </b>{word.word}</p>
                    </div>
                    <div class="flex flex-wrap flex-row space-x-5 items-center">
                        <p class="text-2xl"><b>Gesto da imitare: </b></p>
                        <img src={getSignImage(word.base_pos, word.sign_pos)} alt="img segno" width="85" height="85" class="rounded-lg">
                    </div>
                </div>
                <div class="flex flex-wrap flex-col space-y-2 w-full block md:hidden">
                    <div class="flex flex-wrap flex-row h-fit w-full items-center justify-between">
                        <div class="text-left flex flex-wrap flex-col">
                            <p class="text-xl flex flex-col flex-wrap"><b>Categoria: </b>{word.category}</p>
                            <p class="text-xl flex flex-col flex-wrap"><b>Termine: </b>{word.word}</p>
                        </div>
                        <div class="h-full">
                            <img src={getLanguageImage(word.language)} alt="lingua" width="60" class="rounded-lg">
                        </div>
                    </div>
                    <div class="flex flex-wrap flex-row w-full items-center justify-between">
                        <p class="text-xl"><b>Gesto da imitare: </b></p>
                        <img src={getSignImage(word.base_pos, word.sign_pos)} alt="img segno" width="55" height="5" class="rounded-lg">
                    </div>
                </div>
            {/if}
		    <CameraLearn io={io} bind:startWebcam bind:stopVideoCapture={stopTraining} bind:signId bind:pauseStream={unlockButton}/>
            <p class="text-lg md:text-2xl {msgColor}"><b>{msg}</b></p>
            <button class="btn btn-lg variant-filled-secondary w-full text-base md:text-lg" on:click={nextWord} disabled={!unlockButton}>
                <Icon icon="mdi:arrow-right" class="mr-2" width="30"/>
                Prossimo
            </button>
        {/if}
    </div>
</PageTemplate>