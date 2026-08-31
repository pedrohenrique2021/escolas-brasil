<script>
	import { filters } from "$lib/stores.svelte.js";

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

	let totalFiltrado = $derived.by(() => {
		if (!resumoEstado) return 0;
		if (filters.selectedDependencia === 'Todas') return resumoEstado.total ?? 0;
		return resumoEstado.porDependencia?.[filters.selectedDependencia] ?? 0;
	});

	let rotulo = $derived(
		filters.selectedDependencia === 'Todas'
			? 'Total de escolas'
			: `Escolas — ${filters.selectedDependencia}`
	);
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
		<p class="text-sm text-zinc-400">
			{rotulo}
		</p>

		<p class="text-2xl font-bold text-zinc-100">
			{totalFiltrado.toLocaleString('pt-BR')}
		</p>
	</div>

	<!-- Filtros -->
	<div>
		<p class="text-xs text-zinc-500 mb-2">
			Tipo de escola
		</p>

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
		</div>
	</div>

</div>