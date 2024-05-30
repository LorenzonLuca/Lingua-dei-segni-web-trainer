<script lang="ts">
    import { basePosStore } from '$lib/stores';
    import { getModalStore } from '@skeletonlabs/skeleton';
    import { MAXSIGNS, getSignImage } from '$lib/utils';

    import type { SvelteComponent } from 'svelte';
    export let parent: SvelteComponent;

    const modalStore = getModalStore();

    let basePos: number = 0;

    basePosStore.subscribe((value) => {
        basePos = value;
    })

    let selectedSign = 0;

    function selectSign(n: number){
        selectedSign = n;
        submit();
    }

    function submit(): void {
        if ($modalStore[0].response) $modalStore[0].response(selectedSign);
        modalStore.close();
    }
</script>


<div class="bg-surface-500 p-4 md:p-10 rounded-lg w-full md:w-1/2 text-center space-y-3">
    <h2 class="text-lg md:text-2xl">Seleziona il gesto eseguito</h2>
    <div class="flex flex-wrap flex-row space-y-3">
        <div class="flex flex-wrap flex-row justify-center">
            {#each {length: MAXSIGNS[basePos]} as _, i}
                <button class="w-1/4 md:w-1/6 px-2 py-2" on:click={() => selectSign(i+1)}>
                    <img src={getSignImage(basePos, i+1)} alt="segno {basePos} - {i+1}"/>
                </button>
            {/each}
        </div>
    </div>
</div>