<script context="module" lang="ts">
	import { signedIn } from '$lib/stores';

	export async function load({ session }) {
		if (session.authenticated) {
			signedIn.set(true);
		}
		return {};
	}
</script>

<script>
	import '../app.css';
	import Navbar from '$lib/navbar.svelte';
	import { navbarVisible, pathname } from '$lib/stores';
	import * as Sentry from '@sentry/browser';
	import { BrowserTracing } from '@sentry/tracing';
	import { initLocalizationContext } from '$lib/i18n';
	import { browser } from '$app/env';

	if (browser) {
		pathname.set(window.location.pathname);
		if (
			localStorage.theme === 'dark' ||
			(!('theme' in localStorage) &&
				window.matchMedia('(prefers-color-scheme: dark)').matches)
		) {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}

		// Whenever the user explicitly chooses light mode
		// 		localStorage.theme = 'light';
		//
		// // Whenever the user explicitly chooses dark mode
		// 		localStorage.theme = 'dark';
		//
		// // Whenever the user explicitly chooses to respect the OS preference
		// 		localStorage.removeItem('theme');
	}

	initLocalizationContext();

	if (import.meta.env.VITE_SENTRY !== undefined) {
		Sentry.init({
			dsn: String(import.meta.env.VITE_SENTRY),
			integrations: [new BrowserTracing()],

			// Set tracesSampleRate to 1.0 to capture 100%
			// of transactions for performance monitoring.
			// We recommend adjusting this value in production
			tracesSampleRate: 0.5
		});
	}
</script>

{#if $navbarVisible}
	<Navbar />
	<div class="pt-16 h-screen">
		<div class="z-40" />
		<slot />
	</div>
{:else}
	<slot />
{/if}

<style lang="scss">
	:global(html:not(.dark)) {
		// height: 100%;
		// width: 100%;

		background: linear-gradient(to right, #009444, #39b54a, #8dc63f) repeat-y;
		background-size: cover;
		/*background: linear-gradient(-225deg, #231557 0%, #44107A 29%, #FF1361 67%, #FFF800 100%); */
		/*background: linear-gradient(-225deg, #22E1FF 0%, #1D8FE1 48%, #625EB1 100%); */
		color: black;

		// background-size: 400% 400%;

		//animation: background_animation 5s ease infinite;
	}

	:global(html.dark) {
		background-color: #0f2702;
		background-size: cover;
		color: white;
	}

	@keyframes background_animation {
		0% {
			background-position: 0% 50%;
		}
		50% {
			background-position: 100% 50%;
		}
		100% {
			background-position: 0% 50%;
		}
	}
</style>
