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
}