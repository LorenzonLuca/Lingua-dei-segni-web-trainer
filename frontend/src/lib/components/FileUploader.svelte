<script lang="ts">
    import { FileDropzone } from "@skeletonlabs/skeleton";
    import Icon from '@iconify/svelte';

    export let img: string | undefined = undefined;
    let files: FileList;

    function loadImage(e: Event): void {
        if (validateFile(files[files.length - 1])) {
            imageToBase64(files[files.length - 1], (imgBase64: any) => {
                img = imgBase64;
            });
        }
    }
	
    function validateFile(file: any): boolean {
        const imageTypes = ["image/jpeg", "image/png"];
        return file && imageTypes.includes(file["type"]);
    }

	function imageToBase64(img: any, callback: Function): void {
        const reader = new FileReader();
        reader.addEventListener("load", () => callback(reader.result));
        reader.readAsDataURL(img);
    }
</script>

<FileDropzone bind:files name="img" on:change={loadImage}>
    <svelte:fragment slot="lead">
        <Icon
            icon="mdi:tray-upload"
            width="100"
            class="inline"
        />
    </svelte:fragment>
    <svelte:fragment slot="message">Carica o trascina un immagine</svelte:fragment>
    <svelte:fragment slot="meta">Formati accettati: PNG, JPG</svelte:fragment>
</FileDropzone>