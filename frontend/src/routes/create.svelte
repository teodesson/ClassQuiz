<script context="module" lang="ts">
	import { signedIn } from '$lib/stores';

	export async function load({ session, url }) {
		if (!session.authenticated) {
			return {
				status: 302,
				redirect: '/account/login?returnTo=/create'
			};
		}
		if (session.authenticated) {
			signedIn.set(true);
		}
		const token = url.searchParams.get('token');
		const pin = url.searchParams.get('pin');
		let auto_connect = url.searchParams.get('connect') !== null;
		if (token === null || pin === null) {
			auto_connect = false;
		}
		return {
			props: {
				game_pin: pin === null ? '' : pin,
				game_token: token === null ? '' : token,
				auto_connect: auto_connect
			}
		};
	}
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import Editor from '$lib/editor.svelte';
	import { getLocalization } from '$lib/i18n';
	import { navbarVisible } from '$lib/stores';
	import { dataSchema } from '$lib/yupSchemas';

	navbarVisible.set(true);

	const { t } = getLocalization();

	interface Data {
		public: boolean;
		title: string;
		description: string;
		questions: Question[];
	}

	interface Question {
		question: string;
		time: string;
		answers: Answer[];
	}

	interface Answer {
		right: boolean;
		answer: string;
	}

	let responseData = {
		open: false
	};

	let data: Data;
	let confirm_to_leave = true;
	onMount(() => {
		const from_localstorage = localStorage.getItem('create_game');
		if (from_localstorage === null) {
			data = {
				description: '',
				public: false,
				title: '',
				questions: [{ question: '', time: '20', answers: [{ right: false, answer: '' }] }]
			};
		} else {
			data = JSON.parse(from_localstorage);
		}
	});

	const submit = async () => {
		if (!(await dataSchema.isValid(data))) {
			return;
		}
		const res = await fetch('/api/v1/quiz/create', {
			method: 'POST',
			body: JSON.stringify(data),
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (res.status === 401) {
			localStorage.setItem('create_game', JSON.stringify(data));
			window.location.href = '/account/login';
		} else if (res.status === 200) {
			localStorage.removeItem('create_game');
			responseData.open = true;
		}
	};
	const confirmUnload = () => {
		if (!confirm_to_leave) {
			return;
		}
		event.preventDefault();
		event.returnValue = '';
		localStorage.setItem('create_game', JSON.stringify(data));
	};
</script>

<svelte:window on:beforeunload={confirmUnload} />
<svelte:head>
	<title>ClassQuiz - Create</title>
</svelte:head>

{#if data !== undefined}
	<form on:submit|preventDefault={submit} class="grid grid-cols-1 gap-2">
		<Editor bind:data />
	</form>
{/if}

<div
	class="fixed z-10 inset-0 overflow-y-auto"
	aria-labelledby="modal-title"
	role="dialog"
	aria-modal="true"
	class:hidden={!responseData.open}
>
	<div
		class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
	>
		<div
			class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
			aria-hidden="true"
		/>

		<span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
			>&#8203;</span
		>
		<div
			class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
		>
			<div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
				<div class="sm:flex sm:items-start">
					<div
						class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
					>
						<!-- Heroicon name: outline/exclamation -->
						<svg
							class="w-6 h-6 text-green-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
					</div>
					<div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
						<h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
							{$t('create_page.success.title')}
						</h3>
						<div class="mt-2">
							<p class="text-sm text-gray-500">{$t('create_page.success.body')}</p>
						</div>
					</div>
				</div>
			</div>
			<div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
				<button
					type="button"
					on:click={() => {
						confirm_to_leave = false;
						window.location.href = '/overview';
					}}
					class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
					>{$t('words.close')}
				</button>
			</div>
		</div>
	</div>
</div>
