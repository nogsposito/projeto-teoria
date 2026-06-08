#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>

// assinatura das funções
bool subset_sum_backtracking(int conjunto[], int n, int alvo);
bool subset_sum_dp(int conjunto[], int n, int alvo);

// função auxiliar para calcular o tempo em milissegundos
double calcular_tempo_ms(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;
}

int main(){

    int NUM_RODADAS = 30;

    int tamanhos[] = {10, 20, 25}; // pequeno, médio e grande *
    int num_tamanhos = 3;

    FILE *csv = fopen("../dados/resultados.csv", "w");
    if (csv == NULL) {
        perror("Erro ao abrir o arquivo CSV");
        return EXIT_FAILURE;
    }

    fprintf(csv, "Algoritmo, cenariom tamanho_n, tempo_medio_ms, devio_padrao_ms\n");

    for (int t = 0; t < num_tamanhos; t++){

        int n = tamanhos[t];
        int *vetor_pior_caso = (int*)malloc(n * sizeof(int));

        // pior caso (alvo ímpar)
        for (int i = 0; i < n; i++){
            vetor_pior_caso[i] = 2;
        }
        int soma_alvo_pior = 99999;

        double tempos_rodadas[NUM_RODADAS];
        double soma_tempos = 0;

        for (int rodada = 0; rodada < NUM_RODADAS; rodada++){
            struct timespec start, end;

            // medir tempo do backtracking
            clock_gettime(CLOCK_MONOTONIC, &start); // Marca o início [1, 2]
            
            subsetSum_backtracking(vetor_pior_caso, n, soma_alvo_pior);
            
            clock_gettime(CLOCK_MONOTONIC, &end); // Marca o fim [1, 2]
            
            double tempo_gasto = calcular_tempo_ms(start, end);
            tempos_rodadas[rodada] = tempo_gasto;
            soma_tempos += tempo_gasto;
        }

        // cálculos estatísticos
        double media = soma_tempos / NUM_RODADAS;
        double variancia = 0;

        for (int r = 0; r < NUM_RODADAS; r++){
            variancia += pow(tempos_rodadas[r] - media, 2);
        }

        variancia /= NUM_RODADAS;
        double desvio_padrao = sqrt(variancia);

        fprintf(csv, "Backtracking, Pior caso, %d, %.4f, %.4f\n", n, media, desvio_padrao);

        free(vetor_pior_caso);

    }

    fclose(csv);
    printf("Benchmark concluído. Resultados salvos em '../dados/resultados.csv'\n");
    return 0;

}