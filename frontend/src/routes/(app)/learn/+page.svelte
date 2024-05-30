<script lang="ts">
    import { goto } from "$app/navigation";
	import PageTemplate from "$lib/components/PageTemplate.svelte";

    function startQuiz(){
        goto('/learn/quiz')
    }

    function startTraining(){
        goto('/learn/training')
    }
</script>

<PageTemplate title="Apprendi">
    <div slot="desc">
        Entrambe le modalità di apprendimento utilizzano il riconoscimento in tempo reale.<br>
        Nella modalità allenamento viene mostrato all'utente un termine con la lingua, categoria e un'immagine del gesto che bisogna eseguire. Quando si esegue il gesto
        in modo corretto l'utente potrà passare al prossimo termine.<br>
        Nella modalità quiz invece viene mostrato all'utente soltanto il termine con lingua e categoria ma senza mostrare l'immagine del gesto che bisogna eseguire.
        L'utente dovrà eseguire il gesto corretto senza avere un resoconto in tempo reale. Quando é convinto di avere eseguito bene il gesto può passare al termine successivo.
    </div>
	<div class="space-y-12 text-center flex flex-col items-center w-full">
        <button class="btn variant-filled-surface btn-lg w-full md:w-1/2" on:click={startTraining}>Avvia allenamento</button>
        <button class="btn variant-filled-surface btn-lg w-full md:w-1/2" on:click={startQuiz}>Avvia quiz</button>       
    </div>
</PageTemplate>