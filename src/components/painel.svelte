<script>
	import { filters, municipioTotal, estadoTotal } from "$lib/stores.svelte.js";

	let show = $state(false);
	let options = [
		{ name: 'Todas' },
		{ name: 'Municipal' },
		{ name: 'Privada' },
		{ name: 'Estadual' },
		{ name: 'Federal' }
	];

	function nomeArquivo(src) {
		return src.split('/').pop().replace('.json', '');
	}

	function selecionarFiltro(nome) {
		filters.selectedDependencia = nome;
	}

	let resumoEstado = $derived(filters.totais[nomeArquivo(filters.selectedStateSrc)]);
	let totalFiltrado = $derived(estadoTotal(resumoEstado, filters.selectedDependencia));

	let rotulo = $derived(
		filters.selectedDependencia === 'Todas'
			? 'Total de escolas'
			: `Escolas — ${filters.selectedDependencia}`
	);

	// ranking real, a partir dos municípios do estado atual
	let topMunicipios = $derived.by(() => {
		const features = filters.geojsonAtual?.features ?? [];

		return [...features]
			.map((f) => ({
				name: f.properties.name,
				total: municipioTotal(f.properties, filters.selectedDependencia)
			}))
			.sort((a, b) => b.total - a.total)
			.slice(0, 5);
	});
</script>

<div class="border border-border rounded-xl p-4 bg-bg/50">

	<!-- Cabeçalho -->
	<div class="flex items-start justify-between mb-4">
		<div>
			<p class="text-xs uppercase tracking-wide text-zinc-500 mb-1">
				Estado
			</p>
			<h2 class="text-lg font-semibold text-blue-600 dark:text-sky-400">
				{filters.selectedStateName}
			</h2>
		</div>
	</div>

	<!-- Informação principal -->
	<div class="mb-4">
		<p class="text-sm text-zinc-400">{rotulo}</p>
		<p class="text-2xl font-bold text-zinc-100">
			{totalFiltrado.toLocaleString('pt-BR')}
		</p>
	</div>

	<!-- Filtros -->
	<div>
		<p class="text-xs text-zinc-500 mb-2">Tipo de escola</p>

		<div class="flex flex-wrap gap-2">
			{#each options as option}
				<button
					onclick={() => selecionarFiltro(option.name)}
					class="text-xs px-3 py-1.5 rounded-full border transition-colors cursor-pointer
						{filters.selectedDependencia === option.name
							? 'border-blue-500/50 bg-blue-500/10 text-blue-500 hover:bg-blue-500/20'
							: 'border-zinc-700 text-zinc-400 hover:bg-zinc-800 hover:text-white'}"
				>
					{option.name}
				</button>
			{/each}
			<button
				onclick={() => (show = !show)}
				class="text-xs px-3 py-1.5 rounded-full border border-zinc-700 text-zinc-400 hover:bg-zinc-800 hover:text-white transition-colors cursor-pointer"
			>
				{show ? 'menos' : 'mais'} detalhes
			</button>
		</div>
	</div>

	<div
		class="grid overflow-hidden transition-[grid-template-rows] duration-500 ease-in-out"
		class:grid-rows-[1fr]={show}
		class:grid-rows-[0fr]={!show}
	>
		<div class="min-h-0 pt-4">
			<div class="text-center">
				<span class="text-xs uppercase tracking-wide text-zinc-500">
					Mais detalhes
				</span>
			</div>

			<div class="border-t border-zinc-800 mt-2"></div>

			<div class="mt-4">
				<p class="text-xs text-zinc-500 mb-3">
					Municípios com mais escolas
					{#if filters.selectedDependencia !== 'Todas'}
						<span class="text-zinc-600">— {filters.selectedDependencia}</span>
					{/if}
				</p>

				<div class="space-y-2">
					{#each topMunicipios as municipio, i}
						<div class="grid grid-cols-[32px_1fr_auto] items-center gap-3 px-2 py-2 rounded-lg hover:bg-zinc-800/40 transition-colors">
							<span class="text-xs font-medium text-zinc-500">
								{String(i + 1).padStart(2, '0')}
							</span>
							<span class="text-sm text-zinc-300 truncate">
								{municipio.name}
							</span>
							<span class="text-sm font-semibold text-blue-500">
								{municipio.total.toLocaleString('pt-BR')}
							</span>
						</div>
					{:else}
						<p class="text-xs text-zinc-600 px-2">Nenhum dado disponível.</p>
					{/each}
				</div>
			</div>
		</div>
	</div>

</div>