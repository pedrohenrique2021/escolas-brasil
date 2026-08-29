<script>
    import { onMount } from 'svelte';
    import { states } from '$lib/data';
    import { filters } from '$lib/stores.svelte.js';
    import Filter from './filter.svelte';

    let { onSelect, onSelectName } = $props();

    let totais = $state({});
    let selected = $state(null);

    function nomeArquivo(src) {
        return src.split('/').pop().replace('.json', '');
    }

    let sorted = $derived(
        [...states]
            .filter((state) =>
                state.name
                    .toLowerCase()
                    .includes(filters.searchQuery.toLowerCase())
            )
            .sort((a, b) => {

                if (filters.ordenacao === 'nome-az') {
                    return a.name.localeCompare(b.name);
                }

                if (filters.ordenacao === 'escolas-desc') {
                    const escolasA = totais[nomeArquivo(a.src)] ?? 0;
                    const escolasB = totais[nomeArquivo(b.src)] ?? 0;

                    return escolasB - escolasA;
                }

                if (filters.ordenacao === 'escolas-up') {
                    const escolasA = totais[nomeArquivo(a.src)] ?? 0;
                    const escolasB = totais[nomeArquivo(b.src)] ?? 0;

                    return escolasA - escolasB;
                }

                return 0;
            })
    );

    onMount(async () => {
        const res = await fetch('/data/geojson-enriched/_totais.json');
        totais = await res.json();
    });
</script>


<ul class="divide-y divide-zinc-900 gap-1.5 m-3">

    <Filter />

    {#each sorted as state}
        <li>
            <button
                onclick={() => {
                    selected = state.name;
                    onSelect(state.src);
                    onSelectName(state.name);
                }}
                class="
                    flex items-center gap-2.5 my-1 px-3 py-2
                    rounded-lg text-left w-full
                    bg-bg border hover:bg-gray-900
                    transition-all duration-200 cursor-pointer

                    {selected === state.name
                        ? 'border-blue-500/80 bg-blue-500/10 shadow-md shadow-blue-500/20 ring-1 ring-blue-500/20'
                        : ''}
                "
            >
                <div>
                    <p class="text-sm font-medium">
                        {state.name}
                    </p>

                    <p class="text-xs text-zinc-500">
                        {(totais[nomeArquivo(state.src)] ?? 0).toLocaleString('pt-BR')}
                        escolas
                    </p>
                </div>
            </button>
        </li>
    {/each}

</ul>