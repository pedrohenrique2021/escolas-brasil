<script lang="ts">
	import { onMount } from "svelte";
	import { browser } from "$app/environment";

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
	let L: any;
	let layersById: Record<string, any> = {};
	let selectedId = $state(null);

	function corPorEscolas(total: number) {
		if (total === 0) return "#27272a";
		if (total <= 10) return "#3730a3";
		if (total <= 30) return "#4f46e5";
		if (total <= 60) return "#818cf8";
		return "#c7d2fe";
	}

	function desenharGeojson() {
		if (!map || !geojson || !L) return;

		if (geojsonLayer) {
			map.removeLayer(geojsonLayer);
		}
		layersById = {};

		function highlightFeature(e: any) {
			const layer = e.target;
			layer.setStyle({ weight: 2, color: "#ffffff", fillOpacity: 1 });
			layer.bringToFront();
		}

		function resetHighlight(e: any) {
			const id = e.target.feature.properties.id;
			if  (id === selectedId) return
			geojsonLayer.resetStyle(e.target);
		}

		function onEachFeature(feature: any, layer: any) {
			const p = feature.properties;

			layer.bindTooltip(
				`${p.name} — ${p.escolas_total ?? 0} escolas`,
				{ sticky: true }
			);

	layer.on({
		mouseover: highlightFeature,
		mouseout: resetHighlight,

		click: () => {
			// Remove o destaque do município anterior
			if (selectedId && layersById[selectedId]) {
				geojsonLayer.resetStyle(layersById[selectedId]);
			}

			// Define o município atual como selecionado
			selectedId = p.id;

			// Mantém o efeito de hover
			layer.setStyle({
				weight: 2,
				color: "#ffffff",
				fillOpacity: 1
			});

			layer.bringToFront();

			// Seu comportamento original
			onSelectMunicipio?.(p);

			map.fitBounds(layer.getBounds(), {
				maxZoom: 11
			});
		}
	});

	layersById[p.id] = layer;
}

		geojsonLayer = L.geoJSON(geojson, {
			style: (feature: any) => ({
				color: "#18181b",
				weight: 1,
				fillColor: corPorEscolas(feature.properties.escolas_total ?? 0),
				fillOpacity: 0.85
			}),
			onEachFeature
		}).addTo(map);

		map.fitBounds(geojsonLayer.getBounds());
	}

	onMount(async () => {
		if (!browser) return;

		L = await import("leaflet");
		await import("leaflet/dist/leaflet.css");

		map = L.map(mapContainer).setView(center, zoom);

		L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
			attribution: '&copy; OpenStreetMap contributors'
		}).addTo(map);

		desenharGeojson();
	});

	// redesenha sempre que o geojson (estado selecionado) mudar
	$effect(() => {
		if (geojson) {
			desenharGeojson();
		}
	});

	// pula pro município buscado, quando focusId mudar
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