<script lang="ts">
	import '../../app.postcss';
	import { AppShell, AppBar, initializeStores, Toast } from '@skeletonlabs/skeleton';
	import logo from '$lib/images/logo.png'

	initializeStores();	

</script>

<Toast />

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<img src={logo} alt="Lingua dei segni Trainer" width="60"/>
				<!-- <strong class="text-2xl">Lingua dei segni Trainer</strong> -->
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
</AppShell>