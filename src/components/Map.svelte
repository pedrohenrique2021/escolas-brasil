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
	let L: any;

	const CORES = ["#27272a", "#3730a3", "#4f46e5", "#818cf8", "#c7d2fe"];

	// pega o número certo do município, respeitando o filtro ativo
	function escolasDoMunicipio(properties: any) {
		if (filters.selectedDependencia === 'Todas') {
			return properties.escolas_total ?? 0;
		}
		return properties.escolas_por_dependencia?.[filters.selectedDependencia] ?? 0;
	}

	// calcula os limiares (quantis) a partir dos valores REAIS do estado+filtro atual
	function calcularLimiares(valores: number[]) {
		const positivos = valores.filter((v) => v > 0).sort((a, b) => a - b);

		if (positivos.length === 0) return [0, 0, 0, 0];

		const quantil = (p: number) => {
			const idx = Math.floor(p * (positivos.length - 1));
			return positivos[idx];
		};

		return [quantil(0.25), quantil(0.5), quantil(0.75), quantil(1)];
	}

	function corPorValor(valor: number, limiares: number[]) {
		if (valor === 0) return CORES[0];
		if (valor <= limiares[0]) return CORES[1];
		if (valor <= limiares[1]) return CORES[2];
		if (valor <= limiares[2]) return CORES[3];
		return CORES[4];
	}

	function desenharGeojson() {
		if (!map || !geojson || !L) return;

		if (geojsonLayer) {
			map.removeLayer(geojsonLayer);
		}
		layersById = {};

		// coleta todos os valores do estado, já considerando o filtro ativo
		const valores = geojson.features.map((f: any) => escolasDoMunicipio(f.properties));
		const limiares = calcularLimiares(valores);

		function highlightFeature(e: any) {
			const layer = e.target;
			layer.setStyle({ weight: 2, color: "#ffffff", fillOpacity: 0.85 });
			layer.bringToFront();
		}

		function resetHighlight(e: any) {
			geojsonLayer.resetStyle(e.target);
		}

		function onEachFeature(feature: any, layer: any) {
			const p = feature.properties;
			const total = escolasDoMunicipio(p);
			const rotulo = filters.selectedDependencia === 'Todas'
				? 'escolas'
				: `escolas — ${filters.selectedDependencia}`;

			layer.bindTooltip(`${p.name} — ${total} ${rotulo}`, { sticky: true });

			layer.on({
				mouseover: highlightFeature,
				mouseout: resetHighlight,
				click: () => {
					onSelectMunicipio?.(p);
					map.fitBounds(layer.getBounds(), { maxZoom: 11 });
				}
			});

			layersById[p.id] = layer;
		}

		geojsonLayer = L.geoJSON(geojson, {
			style: (feature: any) => ({
				color: "#18181b",
				weight: 1,
				fillColor: corPorValor(escolasDoMunicipio(feature.properties), limiares),
				fillOpacity: 0.75
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

		L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=SUA_CHAVE_AQUI', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>'
		}).addTo(map);

		desenharGeojson();
	});

	$effect(() => {
		if (geojson) {
			desenharGeojson();
		}
	});

	$effect(() => {
		filters.selectedDependencia;
		if (map && geojson) {
			desenharGeojson();
		}
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