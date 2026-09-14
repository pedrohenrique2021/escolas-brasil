<script lang="ts">
	import Escola from "./escola.svelte";
	let { municipio, onClose } = $props();

	let filtroDependencia = $state('Todas');

	let dependencias = $derived(
		municipio ? ['Todas', ...Object.keys(municipio.escolas_por_dependencia ?? {})] : []
	);

	let escolasFiltradas = $derived(
		municipio
			? (municipio.escolas ?? []).filter(
					(e: any) => filtroDependencia === 'Todas' || e.dependencia === filtroDependencia
				)
			: []
	);
</script>

{#if municipio}
	<div class="flex flex-col h-full">
		<div class="p-2">
			<div class="flex items-start justify-between">
				<h2 class="text-lg font-semibold">{municipio.name}</h2>
				<button onclick={onClose} class="text-zinc-500 hover:text-white text-sm">✕</button>
			</div>

			<p class="text-zinc-400 text-sm mt-1">{municipio.escolas_total ?? 0} escolas cadastradas</p>

			<div class="flex flex-wrap gap-2 mt-3">
				{#each dependencias as dep}
					<button
						onclick={() => (filtroDependencia = dep)}
						class="text-xs px-2 py-1 rounded-full border {filtroDependencia === dep
							? 'bg-indigo-600 border-indigo-600 text-white'
							: 'border-zinc-700 text-zinc-400 hover:text-white'}"
					>
						{dep}{dep !== 'Todas' ? ` (${municipio.escolas_por_dependencia[dep]})` : ''}
					</button>
				{/each}
			</div>
		</div>

		<div class="mt-4 flex-1 overflow-y-auto ">
			{#each escolasFiltradas as escola}
				<Escola {escola}/>
			{/each}

			{#if escolasFiltradas.length === 0}
				<p class="text-zinc-500 text-sm">Nenhuma escola encontrada.</p>
			{/if}
		</div>
	</div>
{/if}