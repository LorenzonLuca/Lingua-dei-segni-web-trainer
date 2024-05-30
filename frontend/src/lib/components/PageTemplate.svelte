<script lang="ts">
    export let title: string | undefined = undefined;
    export let containerExtraStyle: string = "";
</script>


<div class="container w-full mx-auto flex flex-row flex-wrap justify-center p-6 md:p-10 {containerExtraStyle}">
    {#if title}
        <div class="w-full text-3xl text-primary-500">
            <h1>{title}</h1>
        </div>
    {/if}
    <div class="mt-10 mb-20">
        <p class="text-lg">
            <slot name="desc" />
        </p>
    </div>
    <slot />
</div>
