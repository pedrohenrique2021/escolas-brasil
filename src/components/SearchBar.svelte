<script lang="ts">
	let { query = $bindable(''), resultados = [], onPick } = $props();
</script>

<div class="relative">
	<input
		type="text"
		bind:value={query}
		placeholder="Buscar município..."
		class="w-72 rounded-lg bg-zinc-900/90 backdrop-blur border border-zinc-700 px-3 py-2 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
	/>

	{#if query && resultados.length > 0}
		<ul class="absolute mt-1 w-72 rounded-lg bg-zinc-900/95 backdrop-blur border border-zinc-700 overflow-hidden">
			{#each resultados as municipio}
				<li>
					<button
						class="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-700 hover:text-white"
						onclick={() => {
							onPick(municipio.properties.id);
							query = '';
						}}
					>
						{municipio.properties.name}
						<span class="text-zinc-500 text-xs">
							— {municipio.properties.escolas_total ?? 0} escolas
						</span>
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</div>