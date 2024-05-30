<script lang="ts">
	import { PUBLIC_WEBCAM_FRAMES } from '$env/static/public';
	import Camera from './Camera.svelte';
	import CameraLoader from './CameraLoader.svelte';

    export let io: any;
    export let startWebcam: boolean;
    export let stopVideoCapture: any;
    export let signId: any = 0;
    export let pauseStream: boolean = false;
    export let socketEvent: string = 'stream_learn';
    const fps:number = Number(PUBLIC_WEBCAM_FRAMES);
    let videoSource: any = null;
    let loading: boolean = true;
    let webcamError: boolean = false;

    let interval = setInterval(() => {
        if(pauseStream) return;
        const canvas = document.createElement("canvas");
        canvas.width = videoSource.videoWidth;
        canvas.height = videoSource.videoHeight;
        canvas.getContext("2d")!.drawImage(videoSource, 0, 0, canvas.width, canvas.height);
        let img = canvas.toDataURL("image/jpeg");
        io.emit(socketEvent, {'img': img, 'id': signId});
    }, 1000/fps);
</script>

<div class=" w-full md:w-4/5">
    <!-- svelte-ignore a11y-media-has-caption -->
    <Camera bind:videoSource bind:startWebcam bind:stopVideoCapture bind:loading interval={interval} bind:webcamError/>
    {#if loading && !webcamError}
        <CameraLoader />
    {/if}
</div>