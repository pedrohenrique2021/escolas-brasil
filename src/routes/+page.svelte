<script lang="ts">
	import Map from "../components/Map.svelte";
	import Sidebar from "../components/Sidebar.svelte";
	import SearchBar from "../components/SearchBar.svelte";
	import MunicipioPanel from "../components/MunicipioPanel.svelte";
	import { filters } from "$lib/stores.svelte";

	let selectedSrc = $state('/data/geojson-enriched/Acre.json');
	 

	let geojsonData = $state(null);
	let searchQuery = $state('');
	let selectedMunicipio = $state(null);
	let focusId = $state(null);

	function handleSelect(src: string) {
		selectedSrc = src;
		selectedMunicipio = null;
		focusId = null;
		searchQuery = '';
	}

	function handleStateName(name: string) {
		filters.selectedStateName = name;
	}

	function handleSelectMunicipio(properties: any) {
		selectedMunicipio = properties;
	}

	function handlePickMunicipio(id: string) {
		focusId = id;
	}

	// busca o geojson do estado selecionado sempre que a URL mudar
	$effect(() => {
		if (!selectedSrc) return;
		fetch(selectedSrc)
			.then((res) => res.json())
			.then((data) => (geojsonData = data));
	});

	let municipiosFiltrados = $derived(
		geojsonData
			? geojsonData.features
					.filter((f: any) => f.properties.name.toLowerCase().includes(searchQuery.toLowerCase()))
					.slice(0, 8)
			: []
	);
</script>

<style>
	::-webkit-scrollbar {
		width: 10px;
	}
	::-webkit-scrollbar-track {
		background: #f1f1f1;
		border-radius: 5px;
	}
	::-webkit-scrollbar-thumb {
		background: #888;
		border-radius: 5px;
	}
	::-webkit-scrollbar-thumb:hover {
		background: #555;
	}
</style>

<div class="h-screen w-screen flex flex-col bg-zinc-950 text-white overflow-hidden">
	<nav class="h-[60px] shrink-0 flex items-center px-6 border-b border-zinc-800">
		<span class="font-semibold">Escolas Brasil — {filters.selectedStateName}</span>
	</nav>

	<div class="flex flex-1 overflow-hidden">
		<div class="w-64 shrink-0 overflow-y-scroll border-r border-zinc-800">
			<Sidebar onSelect={handleSelect} onSelectName={handleStateName} />
		</div>

		<div class="flex-1 relative">
			<div class="absolute top-4 left-12 z-[1000]">
				<SearchBar bind:query={searchQuery} resultados={municipiosFiltrados} onPick={handlePickMunicipio} />
			</div>

			<Map geojson={geojsonData} {focusId} onSelectMunicipio={handleSelectMunicipio} />
		</div>

		{#if selectedMunicipio}
			<div class="w-80 shrink-0 overflow-y-scroll border-l border-zinc-800">
				<MunicipioPanel municipio={selectedMunicipio} onClose={() => (selectedMunicipio = null)} />
			</div>
		{/if}
	</div>
</div>