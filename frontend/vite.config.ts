import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	server: {
		https: {
			key: './../key.pem',
			cert: './../cert.pem',
		},
		proxy: {}
	},
	plugins: [sveltekit(), purgeCss()]
});