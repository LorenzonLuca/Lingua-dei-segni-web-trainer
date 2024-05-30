<script lang="ts">
	import Icon from '@iconify/svelte';
	import { onMount } from 'svelte';
	import { ioStore } from "$lib/stores";
	import FileUploader from '$lib/components/FileUploader.svelte';
	import CameraStream from '$lib/components/Cameras/CameraStream.svelte';
	import axios, { type AxiosRequestConfig } from 'axios';
	import { getLanguageImage, getSignImage } from '$lib/utils';
	import ConfirmButton from '$lib/components/ConfirmButton.svelte';
	import PageTemplate from '$lib/components/PageTemplate.svelte';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();
	
	let io: any;
	ioStore.subscribe((value) =>{
		io = value;
	})


	let startWebcam: boolean = false;
	let img: string | undefined = undefined;
	let result: Array<any> = [];
	let resultDatas: any[] = []
	let confirmedImage: boolean = false;

	onMount(() =>{
		io.off();
		io.on('real_time_recognization', (res: any) => {
			result = res.data;
		}) 
	})

	$: if(startWebcam){
		io.emit('start_recognization');
	}

	async function recognizeImage(){
		if(img == undefined){
			return;
		}
		confirmedImage = true;
		
		let config: AxiosRequestConfig = {
            method: 'post',
            url: "?/recognize",
            data: {
                "img": img,
            },
            headers: { "Content-Type": "multipart/form-data" },
        }
    
        await axios(config).then((res) => {	
			let tmp = JSON.parse(JSON.parse(res.data.data)[0])
			if(tmp.status){
				if(tmp.status == 'NOK'){
					const t: ToastSettings = {
						message: tmp.msg,
						timeout: 5000,
						background: 'variant-filled-error',
					};
					toastStore.trigger(t);
					backPage()
					return;
				}
			}
			resultDatas = tmp.data;
		})
	}

	function backPage(){
		confirmedImage = false;
		img = undefined;
		resultDatas = []
	}
</script>

<PageTemplate title="Riconosci">
	<div slot="desc">
		{#if !startWebcam && img == undefined}
			Avvia il riconoscimento in tempo reale e esegui dei gesti. Se i gesti eseguiti sono stati registrati, verranno mostrati tutti i termini legati al gesto.
			È possibile anche eseguire il riconoscimento su una singola immagine.
		{/if}	
	</div>
	<div class="space-y-6 text-center flex flex-col items-center w-full md:w-2/3">
		{#if startWebcam}
			<CameraStream io={io} bind:startWebcam/>
			{#if result.length > 0}
				{#each result as r}
					<div class=" card w-full flex flex-col flex-row p-3 space-y-3">
						<div class="w-full flex flex-wrap flex-row justify-between items-center">
							<div class="block md:hidden">
								<img src={getSignImage(r.base_position, r.sign_position)} alt="img segno" width="50" height="50" class="rounded-lg">
							</div>
							<div class="hidden md:block">
								<img src={getSignImage(r.base_position, r.sign_position)} alt="img segno" width="75" height="75" class="rounded-lg">
							</div>
							<h2 class="text-xl md:text-2xl">Posizione base: {r.base_position + 1}</h2>
						</div>
						<div class="w-full flex flex-col flex-wrap space-y-3">
							{#each r.words as w}
								<div class="flex flex-row flex-wrap items-center">
									<img src={getLanguageImage(w.language)} alt="lingua" height="50" width="50" class="rounded-lg">
									<div class="flex flex-row flex-wrap w-4/5 md:w-5/6 pl-5 text-left md:text-lg">
										<p class="w-full md:w-1/2 flex flex-col flex-wrap md:flex-row"><b>Categoria: </b>{w.category}</p>
										<p class="w-full md:w-1/2 flex flex-col flex-wrap md:flex-row"><b>Termine: </b>{w.word}</p>
									</div>
								</div>
								<hr class="block md:hidden"/>
							{/each}
						</div>
					</div>
				{/each}
			{/if}
		{:else}
			{#if img == undefined}
				<button class="btn btn-lg variant-filled-secondary text-base md:text-lg" on:click={()=>startWebcam=true}>
					<Icon icon="mdi:video-outline" class="mr-2" width="30"/>
					Avvia riconoscimento real-time
				</button>
				<p class="text-xl">oppure</p>
				<FileUploader bind:img />
			{:else}
				<div class="flex flex-wrap flex-row justify-center w-full md:w-4/5">
					<div class="w-full space-y-3">
						{#if confirmedImage}
							<button class="btn btn-lg variant-filled-error w-full" on:click={backPage}>
								<Icon icon="mdi:arrow-back" class="mr-2" width="30"/>
								Torna indietro
							</button>
						{/if}
						<img src={img} alt="uploaded">
						{#if confirmedImage}
							{#if resultDatas.length > 0}
								{#each resultDatas as r}
								<div class=" card w-full flex flex-col flex-row p-3 space-y-3">
									<div class="w-full flex flex-wrap flex-row justify-between items-center">
										<div class="block md:hidden">
											<img src={getSignImage(r.base_position, r.sign_position)} alt="img segno" width="50" height="50" class="rounded-lg">
										</div>
										<div class="hidden md:block">
											<img src={getSignImage(r.base_position, r.sign_position)} alt="img segno" width="75" height="75" class="rounded-lg">
										</div>
										<h2 class="text-xl md:text-2xl">Posizione base: {r.base_position + 1}</h2>
									</div>
									<div class="w-full flex flex-col flex-wrap space-y-3">
										{#each r.words as w}
											<div class="flex flex-row flex-wrap items-center">
												<img src={getLanguageImage(w.language)} alt="lingua" height="50" width="50" class="rounded-lg">
												<div class="flex flex-row flex-wrap w-4/5 md:w-5/6 pl-5 text-left md:text-lg">
													<p class="w-full md:w-1/2 flex flex-col flex-wrap md:flex-row"><b>Categoria: </b>{w.category}</p>
													<p class="w-full md:w-1/2 flex flex-col flex-wrap md:flex-row"><b>Termine: </b>{w.word}</p>
												</div>
											</div>
											<hr class="block md:hidden"/>
										{/each}
									</div>
								</div>
								{/each}
							{/if}
						{:else}
							<div class="flex flex-wrap flex-row w-full space-y-5 md:space-y-0">
								<ConfirmButton func={() => img = undefined} buttonText="Cambia immagine" icon="mdi:trash" modalBody="Sei sicuro di voler cambiare l'immagine?" style="w-full md:w-1/2"/>
								<button class="btn btn-lg variant-filled-success w-full md:w-1/2" on:click={recognizeImage}>
									<Icon icon="mdi:check" class="mr-2" width="30"/>
									Conferma
								</button> 
							</div>
						{/if}
					</div>
				</div>
			{/if}
		{/if}
	</div>
</PageTemplate>
