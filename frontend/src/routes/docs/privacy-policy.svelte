<script lang="ts">
	import { onMount } from 'svelte';
	import '$lib/hljs.css';

	onMount(async () => {
		const { default: hljs } = await import('highlight.js/lib/common');
		hljs.highlightAll();
	});
</script>

<svelte:head>
	<title>ClassQuiz/docs - Privacy policy</title>
	<meta
		name="description"
		content="How to self-host ClassQuiz, the open-source quiz-application"
	/>
</svelte:head>

<article
	class="prose prose-sm sm:prose lg:prose-lg xl:prose-xl mx-auto mt-10 prose-slate px-4 dark:prose-invert"
>
	<h1>Privacy Policy</h1>

	<h2>What gets stored for how long and why</h2>
	<table>
		<thead>
			<tr>
				<th>What?</th>
				<th>Why?</th>
				<th>How long?</th>
				<th>Where?</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td> The IP-Address of the user</td>
				<td>
					<ul>
						<li>To prevent abuse</li>
						<li>To provide user-sessions</li>
					</ul>
				</td>
				<td> For a very long time</td>
				<td> On the developers server, by Netcup, in Germany.</td>
			</tr>
			<tr>
				<td> The data the user enters (quizzes, email, username)</td>
				<td> Self-explaining</td>
				<td> Maximum of 30 days after you've deleted your account</td>
				<td> On the developers server, by Netcup, in Germany.</td>
			</tr>
			<tr>
				<td>The <b>hashed</b> password of the user</td>
				<td>Self-explaining</td>
				<td>Maximum of 30 days after you've deleted your account</td>
				<td>On my server, by Netcup, in Germany.</td>
			</tr>
		</tbody>
	</table>

	<h2>Cookies</h2>
	<p>
		Cookies are used to store access-tokens, user-sessions and preferences. They expire after a
		year.
	</p>

	<h2>Third-parties</h2>
	<p>
		This site uses <a href="https://sentry.io/">Sentry</a> to log errors. An opt-out is not
		available at the moment. This website also uses
		<a href="https://plausible.io/">Plausible</a> to log usage-data.
	</p>
</article>
