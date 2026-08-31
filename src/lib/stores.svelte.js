// $lib/stores.svelte.js

export const filters = $state({
	searchQuery: '',
	ordenacao: 'nome-az',
	selectedStateName: 'Acre',
	selectedStateSrc: '/data/geojson-enriched/Acre.json',
	selectedDependencia: 'Todas',
	totais: {}
});