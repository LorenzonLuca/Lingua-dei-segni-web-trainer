<script lang="ts">
	import Icon from '@iconify/svelte';
	import Camera from './Camera.svelte';
	import CameraLoader from './CameraLoader.svelte';

    export let startWebcam: boolean
    export let img: string | undefined = undefined;
    let videoSource: any = null;
    let stopVideoCapture: any;
    let loading: boolean = true;
    let webcamError: boolean = false;

    function takePhoto(){
        const canvas = document.createElement("canvas");
        canvas.width = videoSource.videoWidth;
        canvas.height = videoSource.videoHeight;
        canvas.getContext("2d")!.drawImage(videoSource, 0, 0, canvas.width, canvas.height);
        img = canvas.toDataURL("image/jpeg");
        stopVideoCapture();
    }

    
</script>

<div class="space-y-3 w-full md:w-4/5">
    {#if !loading}
        <button class="btn btn-lg variant-filled-error w-full" on:click={stopVideoCapture}>
            {#if webcamError}
                <Icon icon="mdi:arrow-left" class="mr-2" width="30"/>
                Torna indietro
            {:else}
                <Icon icon="mdi:close" class="mr-2" width="30"/>
                Chiudi webcam
            {/if}
        </button>
    {/if}
    <!-- svelte-ignore a11y-media-has-caption -->
    <Camera bind:videoSource bind:startWebcam bind:stopVideoCapture bind:loading bind:webcamError/>
    {#if !webcamError}
        {#if loading}
            <CameraLoader />
        {/if}
        {#if !loading}
            <button class="btn btn-lg variant-filled-success w-full" on:click={takePhoto}>
                <Icon icon="mdi:camera" class="mr-2" width="30"/>
                Scatta foto
            </button>
        {/if}
    {/if}
</div>