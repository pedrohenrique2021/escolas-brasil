<script>
    import { filters } from '$lib/stores.svelte.js';

    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import {
        faArrowDownAZ,
        faArrowDown91,
        faArrowUp91
    } from '@fortawesome/free-solid-svg-icons';

    function alternarOrdenacao() {
        if (filters.ordenacao === 'escolas-desc') {
            filters.ordenacao = 'escolas-up';
        } else {
            filters.ordenacao = 'escolas-desc';
        }
    }
</script>

<div class="flex items-center gap-2 mb-3">

    <input
        type="text"
        bind:value={filters.searchQuery}
        placeholder="Pesquisar estado..."
        class="w-full px-4 py-2 rounded-lg
            bg-bg border border-zinc-800
            text-sm text-white
            placeholder:text-zinc-500
            outline-none
            focus:border-blue-500
            focus:ring-1 focus:ring-blue-500"
    />

    <div class="flex items-center gap-1 shrink-0">

        <button
            onclick={() => filters.ordenacao = 'nome-az'}
            title="Ordenar por nome (A-Z)"
            class="p-1.5 rounded-md cursor-pointer
                {filters.ordenacao === 'nome-az'
                    ? 'bg-zinc-800 text-white'
                    : 'text-zinc-400 hover:bg-zinc-800 hover:text-white'}"
        >
            <FontAwesomeIcon icon={faArrowDownAZ} />
        </button>

        <button
            onclick={alternarOrdenacao}
            title="Ordenar por quantidade de escolas"
            class="p-1.5 rounded-md cursor-pointer
                {filters.ordenacao === 'escolas-desc' ||
                filters.ordenacao === 'escolas-up'
                    ? 'bg-zinc-800 text-white'
                    : 'text-zinc-400 hover:bg-zinc-800 hover:text-white'}"
        >
            {#if filters.ordenacao === 'escolas-desc'}
                <FontAwesomeIcon icon={faArrowDown91} />
            {:else}
                <FontAwesomeIcon icon={faArrowUp91} />
            {/if}
        </button>

    </div>
</div>