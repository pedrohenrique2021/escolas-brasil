import csv
import json
import os
import unicodedata

RAW_CSV = "raw-data/escolas.csv"
BOUNDARIES_DIR = "../static/data/geojson"
OUTPUT_DIR = "../static/data/geojson-enriched"

UF_TO_FILE = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapa", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceara", "DF": "DistritoFederal", "ES": "EspiritoSanto",
    "GO": "Goias", "MA": "Maranhao", "MT": "MatoGrosso", "MS": "MatoGrossoDoSul",
    "MG": "MinasGerais", "PA": "Para", "PB": "Paraiba", "PR": "Parana",
    "PE": "Pernambuco", "PI": "Piaui", "RJ": "RioDeJaneiro", "RN": "RioGrandeDoNorte",
    "RS": "RioGrandeDoSul", "RO": "Rondonia", "RR": "Roraima", "SC": "SantaCatarina",
    "SP": "SaoPaulo", "SE": "Sergipe", "TO": "Tocantins"
}


def normalizar(texto: str) -> str:
    """Remove acentos e padroniza maiúsculas pra comparar nomes com segurança."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.strip().upper()


def carregar_escolas_agrupadas():
    """Lê o CSV e agrupa escolas por (UF, município normalizado)."""
    grupos = {}

    with open(RAW_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uf = row["UF"].strip()
            municipio = row["Município"].strip()
            chave = (uf, normalizar(municipio))

            if chave not in grupos:
                grupos[chave] = {
                    "total": 0,
                    "por_dependencia": {},
                    "escolas": []
                }

            grupos[chave]["total"] += 1

            dep = row.get("Dependência Administrativa", "Não Informado").strip() or "Não Informado"
            grupos[chave]["por_dependencia"][dep] = grupos[chave]["por_dependencia"].get(dep, 0) + 1

            grupos[chave]["escolas"].append({
                "nome": row["Escola"],
                "inep": row["Código INEP"],
                "dependencia": dep,
                "categoria": row.get("Categoria Administrativa", ""),
                "categoriaPrivada": row.get("Categoria Escola Privada", "").strip(),
                "restricao": row.get("Restrição de Atendimento", ""),
                "localizacao": row.get("Localização", "").strip(),
                "localidadeDiferenciada": row.get("Localidade Diferenciada", "").strip(),
                "endereco": row.get("Endereço", "").strip(),
                "telefone": row.get("Telefone", "").strip(),
                "porte": row.get("Porte da Escola", "").strip(),
                "etapas": row.get("Etapas e Modalidade de Ensino Oferecidas", "").strip(),
                "ofertasEspeciais": row.get("Outras Ofertas Educacionais", "").strip(),
                "conveniada": row.get("Conveniada Poder Público", "").strip(),
                "regulamentada": row.get("Regulamentação pelo Conselho de Educação", "").strip()
            })

    return grupos


def enriquecer_estado(uf: str, nome_arquivo: str, grupos: dict):
    caminho_entrada = os.path.join(BOUNDARIES_DIR, f"{nome_arquivo}.json")
    if not os.path.exists(caminho_entrada):
        print(f"[aviso] arquivo de fronteira não encontrado: {caminho_entrada}")
        return

    with open(caminho_entrada, encoding="utf-8") as f:
        geojson = json.load(f)

    nao_encontrados = []

    for feature in geojson["features"]:
        nome_municipio = feature["properties"]["name"]
        chave = (uf, normalizar(nome_municipio))
        dados = grupos.get(chave)

        if dados:
            feature["properties"]["escolas_total"] = dados["total"]
            feature["properties"]["escolas_por_dependencia"] = dados["por_dependencia"]
            feature["properties"]["escolas"] = dados["escolas"]
        else:
            feature["properties"]["escolas_total"] = 0
            feature["properties"]["escolas_por_dependencia"] = {}
            feature["properties"]["escolas"] = []
            nao_encontrados.append(nome_municipio)

    if nao_encontrados:
        print(f"[{uf}] {len(nao_encontrados)} municípios sem escolas casadas: {nao_encontrados[:5]}...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    caminho_saida = os.path.join(OUTPUT_DIR, f"{nome_arquivo}.json")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)

    print(f"[{uf}] {nome_arquivo}.json gerado ({len(geojson['features'])} municípios).")


def gerar_resumo_por_estado(uf_to_file: dict):
    """Soma o total de escolas de cada estado, e também por dependência administrativa,
    a partir dos arquivos já enriquecidos."""
    resumo = {}

    for uf, nome_arquivo in uf_to_file.items():
        caminho = os.path.join(OUTPUT_DIR, f"{nome_arquivo}.json")
        if not os.path.exists(caminho):
            continue

        with open(caminho, encoding="utf-8") as f:
            geojson = json.load(f)

        total = 0
        por_dependencia = {}

        for feature in geojson["features"]:
            props = feature["properties"]
            total += props.get("escolas_total", 0)

            for dep, qtd in props.get("escolas_por_dependencia", {}).items():
                por_dependencia[dep] = por_dependencia.get(dep, 0) + qtd

        resumo[nome_arquivo] = {
            "total": total,
            "porDependencia": por_dependencia
        }

    caminho_saida = os.path.join(OUTPUT_DIR, "_totais.json")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)

    print(f"\nResumo por estado gerado em {caminho_saida}")


def main():
    print("Lendo e agrupando escolas.csv...")
    grupos = carregar_escolas_agrupadas()
    print(f"{len(grupos)} combinações (UF, município) encontradas no CSV.\n")

    for uf, nome_arquivo in UF_TO_FILE.items():
        enriquecer_estado(uf, nome_arquivo, grupos)

    gerar_resumo_por_estado(UF_TO_FILE)


if __name__ == "__main__":
    main()