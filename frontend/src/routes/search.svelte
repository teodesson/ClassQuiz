<script context="module" lang="ts">
	import { signedIn } from '$lib/stores';

	export async function load({ session }) {
		if (session.authenticated) {
			signedIn.set(true);
		}
		return {};
	}
</script>

<script lang="ts">
	import { getLocalization } from '$lib/i18n';
	const { t } = getLocalization();
	let search_term = '';
	let resp_data = null;

	const submit = async () => {
		console.log('Submit!', search_term);
		const res = await fetch('/api/v1/search/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				q: search_term,
				attributesToHighlight: ['*']
			})
		});
		if (res.status === 200) {
			let resp_data_temp: string = await res.text();
			resp_data_temp = resp_data_temp.replaceAll('<em>', '<mark>');
			resp_data_temp = resp_data_temp.replaceAll('</em>', '</mark>');
			resp_data = JSON.parse(resp_data_temp);
			console.log('Success!', resp_data);
		} else {
			console.error('Error!', res.status);
		}
	};
</script>

<svelte:head>
	<title>ClassQuiz - Search</title>
</svelte:head>

<div>
	<div class="flex justify-center">
		<div class="mb-3 xl:w-96">
			<form
				class="input-group relative flex items-stretch flex-row w-full mb-4"
				on:submit|preventDefault={submit}
			>
				<input
					type="search"
					class="form-control relative flex-auto min-w-0 block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
					placeholder={$t('search_page.at_least_3_characters')}
					aria-label="Search"
					aria-describedby="button-addon2"
					bind:value={search_term}
				/>
				<button
					class="inline-block px-6 py-2.5 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700  focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
					id="button-addon2"
					disabled={search_term.length <= 2}
					type="submit"
				>
					<svg
						aria-hidden="true"
						focusable="false"
						data-prefix="fas"
						data-icon="search"
						class="w-4"
						role="img"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 512 512"
					>
						<path
							fill="currentColor"
							d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"
						/>
					</svg>
				</button>
			</form>
		</div>
	</div>
</div>

{#if resp_data}
	{#if resp_data.hits.length !== 0}
		<div class="grid lg:grid-cols-3 grid-cols-1">
			{#each resp_data.hits as quiz}
				<div class="flex justify-center">
					<a href="/view/{quiz.id}" class="h-max w-fit">
						<div class="max-w-md py-4 px-8 bg-white shadow-lg rounded-lg my-20">
							<!--			<div class='flex justify-center md:justify-end -mt-16'>
											<img class='w-20 h-20 object-cover rounded-full border-2 border-indigo-500'
												 src='https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'>
										</div>-->
							<div>
								<h2 class="text-gray-800 text-3xl font-semibold">
									{@html quiz._formatted.title}
								</h2>
								<p class="mt-2 text-gray-600">
									{@html quiz._formatted.description}
								</p>
							</div>
							<div class="flex mt-4">
								<span
									>{$t('explore_page.made_by')} {@html quiz._formatted.user}</span
								>
							</div>
						</div>
					</a>
				</div>
			{/each}
		</div>
	{:else}
		<div class="flex justify-center">
			<h1 class="text-4xl">There is nothing here...</h1>
		</div>
		<div class="flex justify-center">
			<p>
				Not finding what you are looking for? Search on <a
					class="underline"
					href="https://create.kahoot.it/search?query={search_term}&tags=test&filter=filter%3D1"
					target="_blank">KAHOOT!</a
				>
				and <a href="/import" class="underline">Import</a> it!
			</p>
		</div>
	{/if}
{/if}

<style lang="scss">
	/* eslint-disable-next-line css-unused-selector */
	mark {
		background-color: #ff0;
		border-radius: 0.2em;
		color: #000;
		font-style: normal;
		font-weight: bold;
		padding: 0 0.2em;
	}
</style>
