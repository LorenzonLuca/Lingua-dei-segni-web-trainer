<script lang="ts">
	import PageTemplate from "$lib/components/PageTemplate.svelte";
    import { getLanguageImage, getSignImage } from "$lib/utils";
	import type { PageData } from "./$types";


    export let data: PageData;

    function convertDate(date: Date){
        const d = new Date(date);
        
        return `${String(d.getUTCDate()).padStart(2,'0')}.${String(d.getUTCMonth()+1).padStart(2,'0')}.${d.getUTCFullYear()} - 
        ${String(d.getUTCHours()).padStart(2,'0')}:${String(d.getUTCMinutes()).padStart(2,'0')}`;
    }
</script>

<PageTemplate title="Storico">
    <div slot="desc">
        Nello storico sono presenti i risultati migliori ottenuti durante l'esecuzione dei quiz. 
        La precisone é calcolata facendo una media delle differenze tra il gesto eseguito e il gesto salvato trasformando il risultato in percentuale. 
        In questo modo si può capire quanto é stata corretta l'esecuzione del gesto. Se la precisione é sopra al 90% vuol dire che é stata fatta una buona esecuzione.
    </div>
    <div class="space-y-6 text-center flex flex-col items-center w-full 2xl:w-2/3">
        {#if data.history}
            {#if data.history.length > 0}
                {#each data.history as h}
                    <div class=" card w-full flex flex-wrap flex-row p-6 space-x-2 items-center">
                        <div class="block xl:hidden">
                            <img src={getSignImage(h.base_pos, h.sign_pos)} alt="img segno" width="50" height="50" class="rounded-lg">
                        </div>
                        <div class="hidden xl:block">
                            <img src={getSignImage(h.base_pos, h.sign_pos)} alt="img segno" width="75" height="75" class="rounded-lg">
                        </div>
                        <img src={getLanguageImage(h.language)} alt="lingua" width="50" class="rounded-lg">
                        <div class="flex flex-col md:flex-row flex-wrap w-full xl:w-5/6 xl:pl-5 text-left text-lg">
                            <p class="w-full md:w-1/4 flex flex-col flex-wrap"><b>Categoria:</b>{h.category}</p>
                            <p class="w-full md:w-1/4 flex flex-col flex-wrap"><b>Termine:</b>{h.word}</p>
                            <p class="w-full md:w-1/4 flex flex-col flex-wrap"><b>Precisione:</b>{h.value}%</p>
                            <p class="w-full md:w-1/4 flex flex-col flex-wrap"><b>Data:</b>{convertDate(h.date)}</p>
                        </div>
                    </div>
                {/each}
            {:else}
                <p class="text-lg">Non ci sono valori presenti nello storico. Fai un quiz per salvare all'interno dello storico i tuoi risultati</p>
            {/if}
        {:else}
            <p class="text-lg text-error-500">Errore nella raccolta dei dati presenti nell'history</p>
        {/if}
    </div>
</PageTemplate>