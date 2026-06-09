# projeto-teoria

Implementação e análise de complexidade do algoritmo **Subset Sum** em duas linguagens: **C** e **Python**.

Duas abordagens são comparadas:
- **Backtracking** — força bruta recursiva, O(2ⁿ)
- **Programação Dinâmica (DP)** — Bottom-Up com tabela, O(n × W)

---

## Estrutura do Repositório

```
projeto-teoria/
├── c/
│   ├── backtracking.c      # Implementação backtracking em C
│   ├── dp.c                # Implementação DP em C
│   └── benchmark.c         # Geração de entradas + coleta de resultados (C)
├── python/
│   ├── backtracking.py     # Implementação backtracking em Python
│   ├── dp.py               # Implementação DP em Python
│   └── benchmark.py        # Geração de entradas + coleta de resultados (Python)
├── dados/
│   ├── entradas_compartilhadas.txt   # Vetores/alvos gerados pelo C (lidos pelo Python)
│   ├── resultados_c.csv              # Resultados da execução em C
│   └── resultados_python.csv         # Resultados da execução em Python
└── README.md
```

---

## Como Executar

### 1. Implementação em C

Os testes em C devem ser executados **primeiro**, pois geram o arquivo `entradas_compartilhadas.txt` que será lido pelo Python para garantir comparação justa com os mesmos vetores.

```bash
cd c/
gcc benchmark.c backtracking.c dp.c -o benchmark -lm
./benchmark
```

> A flag `-lm` é necessária para linkar a biblioteca matemática (`<math.h>`), usada no cálculo do desvio-padrão.

Após a execução, dois arquivos serão gerados em `dados/`:
- `entradas_compartilhadas.txt`
- `resultados_c.csv`

---

### 2. Implementação em Python

**Pré-requisito:** Python 3.10 ou superior. Não são necessárias bibliotecas externas — apenas a biblioteca padrão.

```bash
cd python/
python benchmark.py
```

O script irá:
1. Ler os vetores de `dados/entradas_compartilhadas.txt` (gerado pelo C).
2. Executar 30 rodadas para cada combinação de algoritmo × cenário × tamanho de entrada.
3. Salvar os resultados em `dados/resultados_python.csv`.

> Se `entradas_compartilhadas.txt` não existir, o script gera automaticamente suas próprias entradas seguindo a mesma lógica do C.

> ⚠️ **Aviso de tempo:** o backtracking com n=30 no pior caso pode demorar vários minutos em Python devido à sobrecarga do interpretador. Isso é esperado e reflete a diferença de desempenho entre as linguagens.

---

## Cenários de Teste

| Cenário      | Descrição                                                                 |
|-------------|---------------------------------------------------------------------------|
| Melhor Caso  | O alvo (`150`) está no primeiro índice do vetor — backtracking termina cedo |
| Caso Médio   | Distribuição aleatória; alvo existe mas requer busca                      |
| Pior Caso    | Todos os elementos são pares, alvo é ímpar (inatingível) — máximo de operações |

Cada cenário é executado **30 vezes** para os tamanhos de entrada `n = 10`, `n = 20` e `n = 30`.

---

## Documentação dos Ambientes de Execução

### C

- **Processador (CPU):** 12th Gen Intel(R) Core(TM) i5-1235U
- **Memória RAM:** 16 GB
- **Sistema Operacional:** Windows 11
- **Compilador:** GCC (GNU Compiler Collection) versão 14.2.0
- **Comando:** `gcc benchmark.c backtracking.c dp.c -o benchmark -lm`

### Python

- **Processador (CPU):** *(preencher com o da máquina usada)*
- **Memória RAM:** *(preencher)*
- **Sistema Operacional:** *(preencher)*
- **Versão do Python:** *(verificar com `python --version`)*
- **Medição de tempo:** `time.perf_counter()` — alta resolução, equivalente ao `clock_gettime(CLOCK_MONOTONIC)` usado no C

---

## Formato dos CSVs de Saída

```
Algoritmo, Cenario, Tamanho_N, Tempo_Medio_ms, Desvio_Padrao_ms
Backtracking, Melhor Caso, 10, 0.0003, 0.0002
DP, Pior Caso, 30, 1.2500, 0.0430
...
```
