<script>
	let { escola } = $props();

	let show = $state(false);

	let etapas = $derived(
		escola.etapas ? escola.etapas.split(',').map((e) => e.trim()) : []
	);

	let temRestricao = $derived(
		escola.restricao && !escola.restricao.toUpperCase().includes('SEM RESTRIÇÃO')
	);

	let temLocalidadeDiferenciada = $derived(
		escola.localidadeDiferenciada &&
			!escola.localidadeDiferenciada.toUpperCase().includes('NÃO ESTÁ')
	);
</script>

<div class="text-sm text-zinc-300 border-b border-zinc-800 p-2 bg-black">

	<!-- Cabeçalho -->
	<div class="flex items-center justify-between">
		<div>
			<p class="font-medium text-zinc-100">{escola.nome}</p>
			<span class="text-xs text-blue-400">{escola.categoria}</span>
			<span class="text-zinc-700">•</span>
			<span class="text-xs text-zinc-500">INEP {escola.inep}</span>
		</div>

		<button
			onclick={() => (show = !show)}
			class="text-xs px-3 py-1.5 rounded-full border border-zinc-700 text-zinc-400 hover:bg-zinc-800 hover:text-white transition-colors cursor-pointer"
		>
			{show ? 'ocultar' : 'detalhes'}
		</button>
	</div>

	<!-- Alertas — agora FORA do flex do cabeçalho -->
	{#if temRestricao || temLocalidadeDiferenciada}
		<div class="mt-3 space-y-1.5">
			{#if temRestricao}
				<div class="flex items-start gap-2 rounded-lg border border-amber-500/20 bg-amber-500/5 px-3 py-2">
					<span class="text-amber-400 text-xs">!</span>
					<p class="text-[11px] leading-relaxed text-amber-300/80">{escola.restricao}</p>
				</div>
			{/if}

			{#if escola.localidadeDiferenciada && escola.localidadeDiferenciada !== 'Não Informado'}
				<div class="flex items-start gap-2 rounded-lg border border-sky-500/20 bg-sky-500/5 px-3 py-2">
					<span class="text-sky-400 text-xs">i</span>
					<p class="text-[11px] leading-relaxed text-sky-300/80">{escola.localidadeDiferenciada}</p>
				</div>
			{/if}
		</div>
	{/if}

	<!-- Conteúdo expansível -->
	<div
		class="grid overflow-hidden transition-[grid-template-rows] duration-500 ease-in-out"
		class:grid-rows-[1fr]={show}
		class:grid-rows-[0fr]={!show}
	>
		<div class="min-h-0">

			<section class="pt-4">
				<div class="flex items-center gap-2 mb-2">
					<span class="text-xs text-zinc-500">Localização</span>
					<span class="text-xs text-zinc-200">{escola.localizacao}</span>
				</div>
				<p class="text-xs leading-relaxed text-zinc-400">{escola.endereco}</p>
				<p class="text-xs text-zinc-500 mt-1">{escola.telefone}</p>
			</section>

			<section class="mt-5">
				<p class="text-[10px] uppercase tracking-wider text-zinc-600 mb-2">Perfil</p>
				<div class="grid grid-cols-2 gap-2">
					<div class="rounded-lg border border-zinc-800 bg-zinc-950/50 p-3">
						<p class="text-[10px] text-zinc-600 mb-1">Dependência</p>
						<p class="text-xs font-medium text-zinc-200">{escola.dependencia}</p>
					</div>
					<div class="rounded-lg border border-zinc-800 bg-zinc-950/50 p-3">
						<p class="text-[10px] text-zinc-600 mb-1">Porte</p>
						<p class="text-xs font-medium text-zinc-200">{escola.porte}</p>
					</div>
				</div>
			</section>

			<section class="mt-5">
				<p class="text-[10px] uppercase tracking-wider text-zinc-600 mb-2">Etapas de ensino</p>
				<div class="flex flex-wrap gap-1.5">
					{#if etapas.length > 0}
						{#each etapas as etapa}
							<span class="text-[11px] px-2.5 py-1 rounded-md bg-blue-500/10 border border-blue-500/20 text-blue-400">
								{etapa}
							</span>
						{/each}
					{:else}
							<span class="text-[11px] px-2.5 py-1 rounded-md bg-orange-500/10 border border-orange-500/20 text-orange-400">
								Não informado
							</span>
					{/if}
				</div>
			</section>

			{#if escola.ofertasEspeciais}
				<section class="mt-5">
					<p class="text-[10px] uppercase tracking-wider text-zinc-600 mb-2">Atendimento</p>
					<div class="rounded-lg border border-zinc-800 bg-zinc-950/40 px-3 py-2.5">
						<p class="text-xs text-zinc-300">{escola.ofertasEspeciais}</p>
					</div>
				</section>
			{/if}

			<section class="mt-5 mb-3">
				<p class="text-[10px] uppercase tracking-wider text-zinc-600 mb-2">Administração</p>
				<div class="grid grid-cols-2 gap-2">
					<div>
						<p class="text-[10px] text-zinc-600">Conveniada</p>
						<span class={`text-[11px] px-2.5 py-1 rounded-md border ${ escola.conveniada?.toLowerCase() === 'sim' ? 'bg-green-500/10 border-green-500/20 text-green-400' : 'bg-red-500/10 border-red-500/20 text-red-400' }`}>
							{escola.conveniada}
						</span>
			 
					</div>
					<div>
						<p class="text-[10px] text-zinc-600">Regulamentada</p>
						<span class={`text-[11px] px-2.5 py-1 rounded-md border ${ escola.regulamentada?.toLowerCase() === 'sim' ? 'bg-green-500/10 border-green-500/20 text-green-400' : escola.regulamentada?.toLowerCase() === 'não' ? 'bg-red-500/10 border-red-500/20 text-red-400' : 'bg-orange-500/10 border-orange-500/20 text-orange-400' }`} > 
							{#if escola.regulamentada}
								{escola.regulamentada}
							{:else}
								Não informado
							{/if}
						</span>
					</div>
				</div>
			</section>

		</div>
	</div>

</div>