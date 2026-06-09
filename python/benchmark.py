"""
benchmark.py — Geração de entradas e coleta de resultados para Subset Sum (Python).

Metodologia:
  - Lê as entradas compartilhadas geradas pelo C (entradas_compartilhadas.txt).
  - Executa 30 rodadas por (algoritmo × cenário × tamanho).
  - Calcula média e desvio-padrão do tempo em milissegundos.
  - Salva os resultados em dados/resultados_python.csv.

Precisão de tempo: time.perf_counter() — alta resolução, equivalente a
clock_gettime(CLOCK_MONOTONIC) no C.
"""

import time
import math
import csv
import os
import sys
import random

# O backtracking tem complexidade O(2^n). Para n=30, cada chamada pode fazer
# até 2^30 ≈ 10^9 operações no pior caso — o que em Python pode levar vários
# minutos. Aumente o limite de recursão para evitar RecursionError.
sys.setrecursionlimit(200_000)

from backtracking import subset_sum_backtracking
from dp import subset_sum_dp


# Configuração

NUM_RODADAS = 30
TAMANHOS = [10, 20, 30]
DADOS_DIR = os.path.join(os.path.dirname(__file__), "..", "dados")
ENTRADAS_PATH = os.path.join(DADOS_DIR, "entradas_compartilhadas.txt")
SAIDA_CSV = os.path.join(DADOS_DIR, "resultados_python.csv")


# Auxiliares

def calcular_tempo_ms(func, *args) -> float:
    """Executa func(*args) e retorna o tempo gasto em milissegundos."""
    inicio = time.perf_counter()
    func(*args)
    fim = time.perf_counter()
    return (fim - inicio) * 1000.0  # converte para ms


def estatisticas(tempos: list[float]) -> tuple[float, float]:
    """Retorna (média, desvio-padrão) de uma lista de tempos."""
    media = sum(tempos) / len(tempos)
    variancia = sum((t - media) ** 2 for t in tempos) / len(tempos)
    desvio = math.sqrt(variancia)
    return media, desvio


def testar_e_salvar(algoritmo: str, cenario: str, n: int,
                    conjunto: list[int], alvo: int,
                    writer, eh_dp: bool) -> None:
    """Executa NUM_RODADAS medições e escreve uma linha no CSV."""
    func = subset_sum_dp if eh_dp else subset_sum_backtracking
    tempos = [calcular_tempo_ms(func, conjunto, n, alvo) for _ in range(NUM_RODADAS)]
    media, desvio = estatisticas(tempos)
    writer.writerow([algoritmo, cenario, n, f"{media:.4f}", f"{desvio:.4f}"])
    print(f"  [{algoritmo:12s}] {cenario:12s} n={n:2d} → "
          f"média={media:.4f} ms  dp={desvio:.4f} ms")


# Parser do arquivo de entradas compartilhadas

def parse_entradas(path: str) -> list[dict]:
    """
    Lê entradas_compartilhadas.txt gerado pelo C e retorna uma lista de dicts:
        [{"n": int, "melhor": (vetor, alvo), "medio": (vetor, alvo), "pior": (vetor, alvo)}, ...]
    """
    blocos = []
    with open(path, "r") as f:
        conteudo = f.read()

    for bloco in conteudo.split("---"):
        bloco = bloco.strip()
        if not bloco:
            continue
        linhas = {l.split(":")[0]: l.split(":", 1)[1] for l in bloco.splitlines() if ":" in l}
        n = int(linhas["TAMANHO"])
        alvo_melhor = int(linhas["ALVO_MELHOR"])
        vetor_melhor = [int(x) for x in linhas["VETOR_MELHOR"].split(",") if x.strip()]
        alvo_medio = int(linhas["ALVO_MEDIO"])
        vetor_medio = [int(x) for x in linhas["VETOR_MEDIO"].split(",") if x.strip()]
        alvo_pior = int(linhas["ALVO_PIOR"])
        vetor_pior = [int(x) for x in linhas["VETOR_PIOR"].split(",") if x.strip()]
        blocos.append({
            "n": n,
            "melhor": (vetor_melhor, alvo_melhor),
            "medio":  (vetor_medio,  alvo_medio),
            "pior":   (vetor_pior,   alvo_pior),
        })
    return blocos


# Geração de entradas (modo standalone — sem arquivo C)

def gerar_entradas(tamanhos: list[int]) -> list[dict]:
    """
    Gera as mesmas três categorias de entrada do C, para uso quando
    entradas_compartilhadas.txt não está disponível.
    """
    blocos = []
    for n in tamanhos:
        # Melhor caso: alvo está no início do vetor → backtracking termina cedo
        vetor_melhor = [150] + [random.randint(1, 100) for _ in range(n - 1)]
        alvo_melhor = 150

        # Caso médio: distribuição aleatória, alvo existe mas requer busca
        vetor_medio = [random.randint(1, 100) for _ in range(n)]
        alvo_medio = sum(vetor_medio[i] for i in range(0, n, 3))

        # Pior caso: todos os elementos são pares, alvo é ímpar (inatingível)
        vetor_pior = [random.randint(1, 50) * 2 for _ in range(n)]
        alvo_pior = sum(vetor_pior) + 1

        blocos.append({
            "n": n,
            "melhor": (vetor_melhor, alvo_melhor),
            "medio":  (vetor_medio,  alvo_medio),
            "pior":   (vetor_pior,   alvo_pior),
        })
    return blocos

# Main

def main():
    os.makedirs(DADOS_DIR, exist_ok=True)

    # Tenta usar as entradas geradas pelo C; caso contrário, gera novas
    if os.path.exists(ENTRADAS_PATH):
        print(f"Lendo entradas compartilhadas de: {ENTRADAS_PATH}")
        blocos = parse_entradas(ENTRADAS_PATH)
    else:
        print("Arquivo de entradas compartilhadas não encontrado.")
        print("Gerando entradas próprias (os dados não serão idênticos ao C).")
        blocos = gerar_entradas(TAMANHOS)

    with open(SAIDA_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tamanho_N",
                         "Tempo_Medio_ms", "Desvio_Padrao_ms"])

        print("\nIniciando bateria de testes. Isso pode demorar alguns minutos...\n")

        for bloco in blocos:
            n = bloco["n"]
            print(f"=== n = {n} ===")

            vetor_melhor, alvo_melhor = bloco["melhor"]
            vetor_medio,  alvo_medio  = bloco["medio"]
            vetor_pior,   alvo_pior   = bloco["pior"]

            # --- Backtracking ---
            testar_e_salvar("Backtracking", "Melhor Caso", n,
                            vetor_melhor, alvo_melhor, writer, eh_dp=False)
            testar_e_salvar("Backtracking", "Caso Medio",  n,
                            vetor_medio,  alvo_medio,  writer, eh_dp=False)
            testar_e_salvar("Backtracking", "Pior Caso",   n,
                            vetor_pior,   alvo_pior,   writer, eh_dp=False)

            # --- Programação Dinâmica ---
            testar_e_salvar("DP", "Melhor Caso", n,
                            vetor_melhor, alvo_melhor, writer, eh_dp=True)
            testar_e_salvar("DP", "Caso Medio",  n,
                            vetor_medio,  alvo_medio,  writer, eh_dp=True)
            testar_e_salvar("DP", "Pior Caso",   n,
                            vetor_pior,   alvo_pior,   writer, eh_dp=True)

    print(f"\nTodos os testes finalizados! Resultados em {SAIDA_CSV}")


if __name__ == "__main__":
    main()
