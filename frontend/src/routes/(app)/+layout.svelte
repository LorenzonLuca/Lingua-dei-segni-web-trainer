<script lang="ts">
    import type { LayoutData } from './$types';
	import '../../app.postcss';
	import { AppShell, AppBar, initializeStores, Modal, type ModalComponent, Toast, Drawer, getDrawerStore, type DrawerSettings  } from '@skeletonlabs/skeleton';
	import { enhance } from "$app/forms";
	import logo from '$lib/images/logo.png'
	import BasePositionSelector from '$lib/components/Modals/BasePositionSelector.svelte';
	import WordsForm from '$lib/components/Modals/WordsForm.svelte';
	import SignSelector from '$lib/components/Modals/SignSelector.svelte';
	import Icon from '@iconify/svelte';

	export let data: LayoutData;

	initializeStores();
	const drawerStore = getDrawerStore();

	const modalRegistry: Record<string, ModalComponent> = {
		basePosModal: {ref: BasePositionSelector},
		wordsForm: {ref: WordsForm},
		signModal: {ref: SignSelector}
	}

	function openMenu(){
		const settings: DrawerSettings = { id: 'menu' };
		drawerStore.open(settings);
	}

	function closeDrawer(){
		drawerStore.close();
	}
</script>

<Modal components={modalRegistry}/>
<Toast />
<Drawer>
	{#if $drawerStore.id == 'menu'}
		<div class="flex flex-wrap flex-col pt-20 pl-5 space-y-3">
			<h1 class="text-3xl text-primary-500 mb-6">Menu</h1>
			<a href="/" class="text-2xl hover:text-primary-500" on:click={closeDrawer}>Riconosci</a>
			<a href="/learn" class="text-2xl hover:text-primary-500" on:click={closeDrawer}>Apprendi</a>
			{#if data.logged}
				<a href="/history" class="text-2xl hover:text-primary-500" on:click={closeDrawer}>Storico</a>
				{#if data.user?.admin}
					<a href="/insert" class="text-2xl hover:text-primary-500" on:click={closeDrawer}>Inserisci</a>
				{/if}
			{/if}
		</div>
		{/if}
</Drawer>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<div class="block md:hidden">
					<button type="button" class="btn-icon bg-transparent" on:click={openMenu}>
						<Icon icon="mdi:menu" width="30"/>
					</button>
				</div>
				<img src={logo} alt="Lingua dei segni Trainer" width="60"/>
				<div class="hidden md:block">
					<a href="/" class="text-2xl mx-2 hover:text-primary-500">Riconosci</a>
					<a href="/learn" class="text-2xl mx-2 hover:text-primary-500">Apprendi</a>
					{#if data.logged}
						<a href="/history" class="text-2xl mx-2 hover:text-primary-500">Storico</a>
						{#if data.user?.admin}
							<a href="/insert" class="text-2xl mx-2 hover:text-primary-500">Inserisci</a>
						{/if}
					{/if}
				</div>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				{#if data.logged}
					<p class="text-xl">{data.user?.username}</p>
					<form method="post" action="?/logout" use:enhance>
						<button class="btn btn-md variant-ghost-surface" type="submit">Logout</button>
					</form>
				{:else}
					<a class="btn btn-md variant-ghost-surface" href="/login">
						Login
					</a>
					<a class="btn btn-md variant-ghost-surface" href="/register">
						Register
					</a>
				{/if}
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
</AppShell>
