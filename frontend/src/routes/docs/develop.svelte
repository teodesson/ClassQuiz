<svelte:head>
	<title>ClassQuiz/docs - Development-setup</title>
	<meta
		name="description"
		content="How to import quizzes from KAHOOT! into ClassQuiz, the open-source quiz-application,  easily"
	/>
</svelte:head>
<article
	class="prose prose-sm sm:prose lg:prose-lg xl:prose-xl mx-auto mt-10 prose-slate px-4 dark:prose-invert"
>
	<h1>Development-setup</h1>

	<h2>Requirements</h2>
	<h4>Backend</h4>
	<ul>
		<li>
			<a href="https://www.python.org/">Python</a><br /><i
				>I just plan to support the most recent version of Python.</i
			><br /><i>At least Python 3.10</i>
		</li>
		<li><a href="https://caddyserver.com/">Caddy</a></li>
		<li><a href="https://pipenv.pypa.io/en/latest/">Pipenv</a></li>
		<li><a href="https://redis.io/">Redis</a></li>
		<li><a href="https://meilisearch.com">Meilisearch</a></li>
		<li><a href="https://caddyserver.com"><i>(Optional) Caddy</i></a></li>
		<li>Linux</li>
	</ul>

	<h4>Frontend</h4>
	<ul>
		<li><a href="https://pnpm.io/">pnpm</a></li>
	</ul>

	<h2>Setup</h2>
	<ul>
		<li>
			Clone the repo:
			<pre><code>git clone https://github.com/mawoka-myblock/classquiz</code></pre>
		</li>
		<li>
			Install the dependencies
			<ul>
				<li>
					Python:
					<pre><code>pipenv install</code></pre>
				</li>
				<li>
					JS:
					<pre><code>cd frontend && pnpm i</code></pre>
				</li>
			</ul>
		</li>
		<li>
			Start the other services
			<ul>
				<li>
					Caddy:
					<pre><code>caddy run</code></pre>
				</li>
				<li>
					Redis:
					<pre><code>redis-server</code></pre>
				</li>
			</ul>
		</li>
		<li>
			Add the following line to your <code>/etc/hosts</code>-file, so you can visit ClassQuiz
			via <code>test.com</code> (Required for the Captcha and Mapbox)
			<pre><code>127.0.0.1 test.com</code></pre>
		</li>
		<li>
			Set your config up in your .env-file. What you have to set up can you see in the
			<code>classquiz/config.py</code>-file. The things you have to set are the following:
			<ul>
				<li><code>hcaptcha_key</code></li>
				<li><code>mail_address</code></li>
				<li><code>mail_password</code></li>
				<li><code>mail_username</code></li>
				<li><code>mail_server</code></li>
				<li><code>mail_port</code></li>
				<li><code>secret_key</code></li>
				<li><code>meilisearch_url</code></li>
			</ul>
		</li>
		<li>
			Start the server
			<ul>
				<li>
					Backend:
					<pre><code>pipenv run uvicorn classquiz:app --reload</code></pre>
				</li>
				<li>
					Frontend:
					<pre><code>cd frontend && pnpm dev</code></pre>
				</li>
			</ul>
		</li>
	</ul>

	<h2>BEFORE you submit a Pull-Request</h2>
	<p>Please use <a href="https://gitmoji.dev">Gitmoji</a> for your commits.</p>
	<h4>Frontend</h4>
	<p>Please format and lint your code with</p>
	<pre><code>pnpm run format && pnpm run lint</code></pre>

	<h4>Backend</h4>
	<p>IDK, just check that it works!</p>
</article>
