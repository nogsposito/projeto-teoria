"""
benchmark.py — Geração de entradas e coleta de resultados para Subset Sum (Python).
 
Metodologia:
  - Backtracking: tamanhos pequenos (10, 15, 20) — complexidade O(2^n) explode rapidamente
  - DP:           tamanhos maiores (50, 200, 500) — complexidade O(n×W), escala bem
  - 30 rodadas por (algoritmo × cenário × tamanho)
  - Calcula média e desvio-padrão do tempo em milissegundos
  - Salva os resultados em dados/resultados_python.csv
 
Precisão de tempo: time.perf_counter() — alta resolução, equivalente a
clock_gettime(CLOCK_MONOTONIC) no C.
"""
 
import time
import math
import csv
import os
import sys
import random
 
sys.setrecursionlimit(200_000)
 
from backtracking import subset_sum_backtracking
from dp import subset_sum_dp
 
 
# ---------------------------------------------------------------------------
# Configuração — tamanhos separados por algoritmo
# ---------------------------------------------------------------------------
 
NUM_RODADAS        = 30
TAMANHOS_BT        = [10, 15, 20]    # backtracking: O(2^n), limitar para não travar
TAMANHOS_DP        = [50, 100, 200]  # DP: O(n×W), aguenta entradas bem maiores
DADOS_DIR          = os.path.join(os.path.dirname(__file__), "..", "dados")
ENTRADAS_PATH      = os.path.join(DADOS_DIR, "entradas_compartilhadas.txt")
SAIDA_CSV          = os.path.join(DADOS_DIR, "resultados_python.csv")
 
 
# ---------------------------------------------------------------------------
# Auxiliares
# ---------------------------------------------------------------------------
 
def calcular_tempo_ms(func, *args) -> float:
    inicio = time.perf_counter()
    func(*args)
    fim = time.perf_counter()
    return (fim - inicio) * 1000.0
 
 
def estatisticas(tempos: list[float]) -> tuple[float, float]:
    media = sum(tempos) / len(tempos)
    variancia = sum((t - media) ** 2 for t in tempos) / len(tempos)
    return media, math.sqrt(variancia)
 
 
def testar_e_salvar(algoritmo: str, cenario: str, n: int,
                    conjunto: list[int], alvo: int,
                    writer, eh_dp: bool) -> None:
    func = subset_sum_dp if eh_dp else subset_sum_backtracking
    tempos = [calcular_tempo_ms(func, conjunto, n, alvo) for _ in range(NUM_RODADAS)]
    media, desvio = estatisticas(tempos)
    writer.writerow([algoritmo, cenario, n, f"{media:.4f}", f"{desvio:.4f}"])
    print(f"  [{algoritmo:12s}] {cenario:12s} n={n:3d} → "
          f"média={media:.4f} ms  dp={desvio:.4f} ms")
 
 
# ---------------------------------------------------------------------------
# Geração de entradas por tamanho e alvo fixo
# ---------------------------------------------------------------------------
 
def gerar_bloco(n: int, alvo_fixo: int | None = None) -> dict:
    """
    Gera os três cenários para um dado n.
    alvo_fixo: se informado, usa esse valor como alvo_melhor (para compatibilidade
               com entradas_compartilhadas.txt do C, onde alvo_melhor = 150).
    """
    # Melhor caso: alvo está no primeiro índice — backtracking/DP termina cedo
    alvo_melhor = alvo_fixo if alvo_fixo else 150
    vetor_melhor = [alvo_melhor] + [random.randint(1, 100) for _ in range(n - 1)]
 
    # Caso médio: alvo existe mas requer busca
    vetor_medio = [random.randint(1, 100) for _ in range(n)]
    alvo_medio = sum(vetor_medio[i] for i in range(0, n, 3))
 
    # Pior caso: todos pares, alvo ímpar inatingível
    vetor_pior = [random.randint(1, 50) * 2 for _ in range(n)]
    alvo_pior = sum(vetor_pior) + 1
 
    return {
        "n": n,
        "melhor": (vetor_melhor, alvo_melhor),
        "medio":  (vetor_medio,  alvo_medio),
        "pior":   (vetor_pior,   alvo_pior),
    }
 
 
# ---------------------------------------------------------------------------
# Parser do arquivo de entradas compartilhadas (gerado pelo C)
# ---------------------------------------------------------------------------
 
def parse_entradas(path: str) -> dict[int, dict]:
    """Lê entradas_compartilhadas.txt e retorna um dict keyed por n."""
    resultado = {}
    with open(path, "r") as f:
        conteudo = f.read()
    for bloco in conteudo.split("---"):
        bloco = bloco.strip()
        if not bloco:
            continue
        linhas = {l.split(":")[0]: l.split(":", 1)[1] for l in bloco.splitlines() if ":" in l}
        n           = int(linhas["TAMANHO"])
        alvo_melhor = int(linhas["ALVO_MELHOR"])
        vetor_melhor = [int(x) for x in linhas["VETOR_MELHOR"].split(",") if x.strip()]
        alvo_medio  = int(linhas["ALVO_MEDIO"])
        vetor_medio  = [int(x) for x in linhas["VETOR_MEDIO"].split(",") if x.strip()]
        alvo_pior   = int(linhas["ALVO_PIOR"])
        vetor_pior   = [int(x) for x in linhas["VETOR_PIOR"].split(",") if x.strip()]
        resultado[n] = {
            "n": n,
            "melhor": (vetor_melhor, alvo_melhor),
            "medio":  (vetor_medio,  alvo_medio),
            "pior":   (vetor_pior,   alvo_pior),
        }
    return resultado
 
 
# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
 
def main():
    os.makedirs(DADOS_DIR, exist_ok=True)
 
    # Carrega entradas do C se disponível (só para os tamanhos do BT)
    entradas_c: dict[int, dict] = {}
    if os.path.exists(ENTRADAS_PATH):
        print(f"Lendo entradas compartilhadas de: {ENTRADAS_PATH}")
        entradas_c = parse_entradas(ENTRADAS_PATH)
    else:
        print("Arquivo de entradas compartilhadas não encontrado — gerando entradas próprias.")
 
    with open(SAIDA_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tamanho_N",
                         "Tempo_Medio_ms", "Desvio_Padrao_ms"])
 
        print("\nIniciando bateria de testes...\n")
 
        # ── BACKTRACKING (tamanhos pequenos) ─────────────────────────────────
        print(">>> BACKTRACKING (O(2^n)) — tamanhos: " + str(TAMANHOS_BT))
        for n in TAMANHOS_BT:
            print(f"=== n = {n} ===")
            # usa entradas do C se existir para esse n; caso contrário gera novas
            bloco = entradas_c.get(n) or gerar_bloco(n)
            vetor_melhor, alvo_melhor = bloco["melhor"]
            vetor_medio,  alvo_medio  = bloco["medio"]
            vetor_pior,   alvo_pior   = bloco["pior"]
 
            testar_e_salvar("Backtracking", "Melhor Caso", n,
                            vetor_melhor, alvo_melhor, writer, eh_dp=False)
            testar_e_salvar("Backtracking", "Caso Medio",  n,
                            vetor_medio,  alvo_medio,  writer, eh_dp=False)
            testar_e_salvar("Backtracking", "Pior Caso",   n,
                            vetor_pior,   alvo_pior,   writer, eh_dp=False)
 
        # ── PROGRAMAÇÃO DINÂMICA (tamanhos maiores) ───────────────────────────
        print("\n>>> DP (O(n×W)) — tamanhos: " + str(TAMANHOS_DP))
        for n in TAMANHOS_DP:
            print(f"=== n = {n} ===")
            bloco = gerar_bloco(n)  # entradas do C não têm esses tamanhos
            vetor_melhor, alvo_melhor = bloco["melhor"]
            vetor_medio,  alvo_medio  = bloco["medio"]
            vetor_pior,   alvo_pior   = bloco["pior"]
 
            testar_e_salvar("DP", "Melhor Caso", n,
                            vetor_melhor, alvo_melhor, writer, eh_dp=True)
            testar_e_salvar("DP", "Caso Medio",  n,
                            vetor_medio,  alvo_medio,  writer, eh_dp=True)
            testar_e_salvar("DP", "Pior Caso",   n,
                            vetor_pior,   alvo_pior,   writer, eh_dp=True)
 
    print(f"\nTodos os testes finalizados! Resultados em {SAIDA_CSV}")
 
 
if __name__ == "__main__":
    main()