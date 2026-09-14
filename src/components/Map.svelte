<script lang="ts">
	import { onMount } from "svelte";
	import { browser } from "$app/environment";
	import { filters } from "$lib/stores.svelte.js";

	let {
		geojson,
		center = [-15.78, -47.93] as [number, number],
		zoom = 4,
		focusId = null,
		onSelectMunicipio
	} = $props();

	let mapContainer: HTMLDivElement;
	let map: any;
	let geojsonLayer: any;
	let layersById: Record<string, any> = {};
	let layerDestacada: any = null;
	let L: any;

	const CORES = ["#27272a", "#3730a3", "#4f46e5", "#818cf8", "#c7d2fe"];
	const HOVER_STYLE = { weight: 2, color: "#ffffff", fillOpacity: 0.85 };

	function escolasDoMunicipio(properties: any) {
		return filters.selectedDependencia === 'Todas'
			? properties.escolas_total ?? 0
			: properties.escolas_por_dependencia?.[filters.selectedDependencia] ?? 0;
	}

	function calcularLimiares(valores: number[]) {
		const positivos = valores.filter((v) => v > 0).sort((a, b) => a - b);
		if (!positivos.length) return [0, 0, 0, 0];

		const quantil = (p: number) => positivos[Math.floor(p * (positivos.length - 1))];
		return [0.25, 0.5, 0.75, 1].map(quantil);
	}

	function corPorValor(valor: number, [q1, q2, q3]: number[]) {
		if (valor === 0) return CORES[0];
		if (valor <= q1) return CORES[1];
		if (valor <= q2) return CORES[2];
		if (valor <= q3) return CORES[3];
		return CORES[4];
	}

	function destacar(layer: any) {
		if (layerDestacada && layerDestacada !== layer) {
			geojsonLayer.resetStyle(layerDestacada);
		}
		layer.setStyle(HOVER_STYLE);
		layer.bringToFront();
		layerDestacada = layer;
	}

	function limparDestaque(layer: any) {
		geojsonLayer.resetStyle(layer);
		if (layerDestacada === layer) layerDestacada = null;
	}

	function desenharGeojson() {
		if (!map || !geojson || !L) return;

		if (geojsonLayer) map.removeLayer(geojsonLayer);
		layersById = {};
		layerDestacada = null;

		const limiares = calcularLimiares(geojson.features.map((f: any) => escolasDoMunicipio(f.properties)));

		geojsonLayer = L.geoJSON(geojson, {
			style: (feature: any) => ({
				color: "#18181b",
				weight: 1,
				fillColor: corPorValor(escolasDoMunicipio(feature.properties), limiares),
				fillOpacity: 0.75
			}),
			onEachFeature: (feature: any, layer: any) => {
				const p = feature.properties;
				const total = escolasDoMunicipio(p);
				const sufixo = filters.selectedDependencia === 'Todas' ? '' : ` — ${filters.selectedDependencia}`;

				layer.bindTooltip(`${p.name} — ${total} escolas${sufixo}`, { sticky: true });
				layer.on({
					mouseover: (e: any) => destacar(e.target),
					mouseout: (e: any) => limparDestaque(e.target),
					click: () => {
						destacar(layer),
						onSelectMunicipio?.(p);
						map.fitBounds(layer.getBounds(), { maxZoom: 11 });
					}
				});

				layersById[p.id] = layer;
			}
		}).addTo(map);

		map.fitBounds(geojsonLayer.getBounds());
	}

	onMount(async () => {
		if (!browser) return;

		L = await import("leaflet");
		await import("leaflet/dist/leaflet.css");

		map = L.map(mapContainer).setView(center, zoom);
		L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=SUA_CHAVE_AQUI', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>'
		}).addTo(map);

		desenharGeojson();
	});

	// redesenha sempre que o estado OU o filtro de dependência mudarem
	$effect(() => {
		geojson;
		filters.selectedDependencia;
		desenharGeojson();
	});

	$effect(() => {
		const layer = focusId ? layersById[focusId] : null;
		if (layer && map) {
			map.fitBounds(layer.getBounds(), { maxZoom: 12 });
			layer.openTooltip();
			onSelectMunicipio?.(layer.feature.properties);
		}
	});
</script>

<div bind:this={mapContainer} class="w-full h-full"></div>