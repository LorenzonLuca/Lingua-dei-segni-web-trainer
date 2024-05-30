import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	server: {
		https: {
			key: './../signlanguage-privateKey.key',
			cert: './../signlanguage.crt',
		}
	},
	plugins: [sveltekit(), purgeCss()]
});