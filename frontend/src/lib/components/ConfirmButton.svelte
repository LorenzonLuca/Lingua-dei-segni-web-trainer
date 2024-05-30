<script lang="ts">
	import Icon from "@iconify/svelte";
    import { getModalStore, type ModalSettings } from '@skeletonlabs/skeleton';
			
    const modalStore = getModalStore();
    export let style: string = "w-1/2";
    export let func: Function;
    export let buttonText: string;
    export let icon: string;
    export let modalTitle: string = "Conferma";
    export let modalBody: string;

    function removeImg(){
        const modal: ModalSettings = {
            type: 'confirm',
            title: modalTitle,
            body: modalBody,
            buttonTextConfirm: 'Conferma',
            buttonTextCancel: 'Annulla',
            response: (r: boolean) => {
                if(r){
                    func();
                }
            }
        };
        modalStore.trigger(modal);
    }
</script>

<button class="btn btn-lg variant-filled-error {style}" on:click={removeImg}>
    <Icon icon={icon} class="mr-2" width="30"/>
    {buttonText}
</button>