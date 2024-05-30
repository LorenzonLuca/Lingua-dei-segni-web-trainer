<script lang="ts">
	import Icon from '@iconify/svelte';
	import Camera from './Camera.svelte';
	import CameraLoader from './CameraLoader.svelte';
	import { PUBLIC_WEBCAM_FRAMES } from '$env/static/public';
	import { RangeSlider } from '@skeletonlabs/skeleton';

    export let io: any;
    export let startWebcam: boolean;
    const fps:number = Number(PUBLIC_WEBCAM_FRAMES);
    let videoSource: any = null;
    let stopVideoCapture: any;
    let loading: boolean = true;
    let webcamError: boolean = false;

    let tValue = 0.04;
    let max = 0.1;

    let interval = setInterval(() => {
        const canvas = document.createElement("canvas");
        canvas.width = videoSource.videoWidth;
        canvas.height = videoSource.videoHeight;
        canvas.getContext("2d")!.drawImage(videoSource, 0, 0, canvas.width, canvas.height);
        let img = canvas.toDataURL("image/jpeg");
        io.emit('stream', {'img':img, 'threshold': tValue});
    }, 1000/fps);
</script>

<div class="space-y-3 w-full md:w-4/5">
    {#if !loading}
    <button class="btn btn-lg variant-filled-error w-full" on:click={stopVideoCapture}>
        {#if webcamError}
            <Icon icon="mdi:arrow-left" class="mr-2" width="30"/>
            Torna indietro
        {:else}
            <Icon icon="mdi:close" class="mr-2" width="30"/>
            Ferma riconoscimento real-time
        {/if}
    </button>
    {/if}
    <!-- svelte-ignore a11y-media-has-caption -->
    <Camera bind:videoSource bind:startWebcam bind:stopVideoCapture bind:loading interval={interval} bind:webcamError />
    {#if !webcamError}
        {#if loading }
            <CameraLoader />
        {:else}
            <RangeSlider name="threshold" bind:value={tValue} max={max} step={0.001}>
                <div class="flex justify-between items-center">
                    <div class="font-bold">Margine d'errore</div>
                    <div class="font-bold">{tValue} / {max}</div>
                </div>
            </RangeSlider>
        {/if}
    {/if}
</div>