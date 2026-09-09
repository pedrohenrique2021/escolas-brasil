// $lib/stores.svelte.js

export const filters = $state({
	searchQuery: '',
	ordenacao: 'nome-az',
	selectedStateName: 'Acre',
	selectedStateSrc: '/data/geojson-enriched/Acre.json',
	selectedDependencia: 'Todas',
	totais: {},
	geojsonAtual: null
});

export function municipioTotal(properties, dependenciaSelecionada) {
	if (dependenciaSelecionada === 'Todas') {
		return properties.escolas_total ?? 0;
	}
	return properties.escolas_por_dependencia?.[dependenciaSelecionada] ?? 0;
}

export function estadoTotal(resumoEstado, dependenciaSelecionada) {
	if (!resumoEstado) return 0;
	if (dependenciaSelecionada === 'Todas') return resumoEstado.total ?? 0;
	return resumoEstado.porDependencia?.[dependenciaSelecionada] ?? 0;
}