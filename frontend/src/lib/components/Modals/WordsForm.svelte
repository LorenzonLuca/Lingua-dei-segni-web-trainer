<script lang="ts">
	import { getModalStore } from '@skeletonlabs/skeleton';
    import ita from '$lib/images/languages/ita.png';
    import fra from '$lib/images/languages/fra.png';
    import type { SvelteComponent } from 'svelte';
	import CategoryList from './CategoryList.svelte';
    import Icon from '@iconify/svelte';
	import { getLanguageImage, isEmptyString } from '$lib/utils';
    import { wordsStore } from '$lib/stores';

    export let parent: SvelteComponent;
    export let words: Array<Word> = [];
    let word: string = "";
    let category: string = "";
    let searchValue: string = "";
    let language: number = 0;

    wordsStore.subscribe((value) => {
        words = value;
    })

    const modalStore = getModalStore();


    // Handle Form Submission
    function submit(): void {
        wordsStore.set(words);
        if ($modalStore[0].response) $modalStore[0].response(words ? words : undefined);
        modalStore.close();
    }

    function addWord(){        
        if(isEmptyString(word) || isEmptyString(category)){
            return;
        }
        let lang = language == 0 ? 'italian' : 'french';
        words = [...words, {word: word, category: category, language: lang}]

        word = "";
        category = "";
        searchValue = "";
        language = 0;
    }

    function switchLanguage(n: number){
        language = n
    }

    function removeWord(w: Word){
        words = words.filter((word) => w != word);
    }
</script>

<div class="bg-surface-500 p-4 md:p-10 rounded-lg w-full lg:w-1/2 text-center space-y-3">
    <h2 class="text-2xl">Inserisci i termini</h2>
    <div class="flex flex-wrap flex-row">
        <div class="w-full md:w-1/2 text-left space-y-2">
            <label class="label">
                <span>Termine:</span>
                <input class="input" type="text" placeholder="Termine" name="password" bind:value={word}/>
            </label>
            <CategoryList bind:value={category} bind:searchValue/>
            <div class="flex flex-wrap flex-row justify-evenly">
                <button class={language == 0 ? "p-3 rounded-lg bg-tertiary-500" : "p-3 rounded-lg"} on:click={() => switchLanguage(0)}>
                    <img src={ita} alt="ita" width="60"/>
                </button>
                <button class={language == 1? "p-3 rounded-lg bg-tertiary-500" : "p-3 rounded-lg"} on:click={() => switchLanguage(1)}>
                    <img src={fra} alt="fra" width="60"/>
                </button>
            </div>
            <button class="btn btn-lg variant-filled-secondary w-full" on:click={addWord}>
                <Icon icon="mdi:add-circle-outline" class="mr-2" width="30" />
                Aggiungi termine
            </button>
        </div>
        <div class="w-1/2 text-left p-6 space-y-2 hidden md:block">
            {#each words as w}
                <div class="w-full flex flex-wrap flex-row justify-between items-center">
                    <div class="flex flex-wrap flex-row justify-center items-center space-y-0 space-x-2">
                        <button type="button" class="btn-icon btn-icon-sm variant-filled-error" on:click={() => removeWord(w)}>
                            <Icon icon="mdi:close" width="25"/>
                        </button>
                        <img src={getLanguageImage(w.language)} alt="language" width="45"/>
                    </div>
                    <div class="flex flex-wrap flex-col lg:w-1/2">
                        <p class="w-full"><b>Termine:</b> {w.word}</p>
                        <p class="w-full"><b>Categoria:</b> {w.category}</p>
                    </div>
                </div>
            {/each}
        </div>
    </div>
    <button class="btn btn-lg variant-filled-primary w-full" on:click={submit}>
        <Icon icon="mdi:add-circle-outline" class="mr-2" width="30" />
        Salva tutti i termini
    </button>
    <div class="w-full text-left space-y-2 block w-full md:hidden">
        {#each words as w}
            <div class="w-full flex flex-wrap flex-row items-center">
                <div class="flex flex-wrap flex-row justify-center items-center space-x-2 w-1/3">
                    <button type="button" class="btn-icon btn-icon-sm variant-filled-error" on:click={() => removeWord(w)}>
                        <Icon icon="mdi:close" width="25"/>
                    </button>
                    <img src={getLanguageImage(w.language)} alt="language" width="45"/>
                </div>
                <div class="flex flex-wrap flex-col w-2/3">
                    <p class="w-full text-ellipsis"><b>Termine:</b> {w.word}</p>
                    <p class="w-full truncate"><b>Categoria:</b> {w.category}</p>
                </div>
            </div>
        {/each}
    </div>
</div>