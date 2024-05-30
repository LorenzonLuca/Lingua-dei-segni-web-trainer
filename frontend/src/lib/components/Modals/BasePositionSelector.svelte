<script lang="ts">
    import base01 from '$lib/images/basePositions/base01.jpg';
    import base02 from '$lib/images/basePositions/base02.jpg';
    import base03 from '$lib/images/basePositions/base03.jpg';
    import base04 from '$lib/images/basePositions/base04.jpg';
    import base05 from '$lib/images/basePositions/base05.jpg';
    import base06 from '$lib/images/basePositions/base06.jpg';
	import { getModalStore } from '@skeletonlabs/skeleton';
    import { basePosStore } from '$lib/stores';

    import type { SvelteComponent } from 'svelte';
    export let parent: SvelteComponent;

    const modalStore = getModalStore();


    let selectedPos: any = undefined;

    function selectPos(v: number){
        switch(v){
            case 0:
                selectedPos = {'id': 0, 'img':base01};
                break;
            case 1:
                selectedPos = {'id': 1, 'img':base02};
                break;
            case 2:
                selectedPos = {'id': 2, 'img':base03};
                break;
            case 3:
                selectedPos = {'id': 3, 'img':base04};
                break;
            case 4:
                selectedPos = {'id': 4, 'img':base05};
                break;
            case 5:
                selectedPos = {'id': 5, 'img':base06};
                break;
        }
        submit();
    }

    // Handle Form Submission
    function submit(): void {
        if(selectPos != undefined){
            basePosStore.set(selectedPos.id);
        }
        if ($modalStore[0].response) $modalStore[0].response(selectedPos);
        modalStore.close();
    }
</script>

<div class="bg-surface-500 p-4 md:p-10 rounded-lg w-full md:w-1/2 text-center space-y-3">
    <h2 class="text-lg md:text-2xl">Seleziona la posizione base</h2>
    <div class="flex flex-wrap flex-row space-y-3">
        <div class="flex flex-wrap flex-row space-x-3 justify-center ">
            <button on:click={() => selectPos(0)} class="w-1/4">
                <img src={base01} alt="base01"/>
            </button>
            <button on:click={() => selectPos(1)} class="w-1/4">
                <img src={base02} alt="base02"/>
            </button>
            <button on:click={() => selectPos(2)} class="w-1/4">
                <img src={base03} alt="base03"/>
            </button>
        </div>
        <div class="flex flex-wrap flex-row space-x-3 justify-center">
            <button on:click={() => selectPos(3)} class="w-1/4">
                <img src={base04} alt="base04"/>
            </button>
            <button on:click={() => selectPos(4)} class="w-1/4">
                <img src={base05} alt="base05"/>
            </button>
            <button on:click={() => selectPos(5)} class="w-1/4">
                <img src={base06} alt="base06"/>
            </button>
        </div>
    </div>
</div>