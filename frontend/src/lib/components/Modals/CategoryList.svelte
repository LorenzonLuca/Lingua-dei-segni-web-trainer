<script lang="ts">
    export let value:any = undefined;
    const values = ['Nazione','Città', 'Circolazione', 'Professione/Scuola', 'Famiglia', 'Sport/Tempo libero', 'Cibo', 'Economia domestica', 'Persone',
        'Animali','Natura','Casa/Edificio','Politica/Diritto','Medicina','Economia','In generale', 'Religione', 'Verbo', 'Proprietà', 'Eventi/Media'];
    export let searchValue: string = "";

    let filtered = values;
    $: filtered = values.filter((str) => str.toLowerCase().includes(searchValue.toLowerCase()));
</script>

<div>
    <label class="label mt-3">
        <span>Categoria:</span>
        <input class="input" type="text" placeholder="Cerca" name="text" bind:value={searchValue}/>
    </label>
    <select class="select" size="4" bind:value={value}>
        {#if searchValue === ""}
            {#each values as v}
                <option value={v}>{v}</option >
        {/each}
        {:else}
            {#each filtered as v}
                <option value={v}>{v}</option >
            {/each}
        {/if}
    </select>
</div>