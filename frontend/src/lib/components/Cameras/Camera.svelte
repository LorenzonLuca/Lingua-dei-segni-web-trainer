<script lang="ts">
    export let startWebcam: boolean
    export let videoSource: any = null;
    export let interval: any = undefined;
    export let loading: boolean = false
    export let webcamError: boolean = false;
    let webcamErrorMsg: string = "";
    let stream: any = null;

    async function obtenerVideoCamera(): Promise<void> {
        try {
            loading = true;
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1920 },
                    height: { ideal: 1080 },
                },
            });
            videoSource.srcObject = stream;
            videoSource.play();
            loading = false;       
        } catch (error: any) {
            webcamErrorMsg = error.message;
            webcamError = true;
            loading = false;
        }
    }

    export const stopVideoCapture = () =>{
        if (stream) {
            stream.getTracks().forEach(function (track: any) {
                track.stop();
            });
        }

        if(interval !== undefined){
            clearInterval(interval)
        }
        startWebcam = false;
    }

    obtenerVideoCamera();
</script>

<!-- svelte-ignore a11y-media-has-caption -->
<video bind:this={videoSource} class="mb-5" />
{#if webcamError}
    <div class="card variant-filled-error p-5 mb-5">
        <h2 class="text-2xl">Error to access webcam:</h2>
        <p>{webcamErrorMsg}</p>
    </div>
{/if}
