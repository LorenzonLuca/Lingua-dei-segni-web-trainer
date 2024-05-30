<script lang="ts">
	import { goto } from "$app/navigation";
	import PageTemplate from "$lib/components/PageTemplate.svelte";
    import { deltasStore } from "$lib/stores";
	import { calcPerc, getLanguageImage, getSignImage } from "$lib/utils";
	import Icon from "@iconify/svelte";

    let deltas: Array<WordDelta>;

	deltasStore.subscribe((value) =>{
		deltas = value;
        console.log(value);
	})

    function learnPage(){
        goto('/learn');
    }
</script>

<PageTemplate title="Risultati quiz">
    <div class="space-y-6 text-center flex flex-col items-center w-full 2xl:w-2/3">
        {#each deltas as d}
            <div class=" card w-full flex flex-wrap flex-row p-6 space-x-2 items-center">
                {#if d.word.basePos != undefined && d.word.signPos != undefined}
                    <div class="block xl:hidden">
                        <img src={getSignImage(d.word.basePos, d.word.signPos)} alt="img segno" width="50" height="50" class="rounded-lg">
                    </div>
                    <div class="hidden xl:block">
                        <img src={getSignImage(d.word.basePos, d.word.signPos)} alt="img segno" width="75" height="75" class="rounded-lg">
                    </div>
                {/if}
                <img src={getLanguageImage(d.word.language)} alt="lingua" width="50" class="rounded-lg">
                <div class="flex flex-col md:flex-row flex-wrap w-full xl:w-5/6 xl:pl-5 text-left text-lg">
                    <p class="w-full md:w-1/4 flex flex-col flex-wrap"><b>Categoria:</b>{d.word.category}</p>
                    <p class="w-full md:w-1/4 flex flex-col flex-wrap"><b>Termine:</b>{d.word.word}</p>
                    <p class="w-full md:w-1/4 flex flex-col flex-wrap"><b>Precisione:</b>{calcPerc(d.delta).toFixed(3)}%</p>
                </div>
            </div>
        {/each}
        <button class="btn btn-lg variant-filled-error w-full text-base md:text-xl" on:click={learnPage}>
            <Icon icon="mdi:arrow-left" class="mr-2" width="30"/>
            Torna alla pagina di apprendimento
        </button>
    </div>
</PageTemplate>