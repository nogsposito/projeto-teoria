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

void testar_e_salvar(const char* algoritmo, const char* cenario, int n, int conjunto[], int alvo, FILE* csv, bool eh_dp){

    int NUM_RODADAS = 30;
    double tempos_rodadas[NUM_RODADAS];
    double soma_tempos = 0;

    // REMOVIDO o loop for (int t = 0...), mantendo apenas o loop das 30 rodadas
    for (int rodada = 0; rodada < NUM_RODADAS; rodada++) {
        struct timespec start, end;
        
        clock_gettime(CLOCK_MONOTONIC, &start);
        
        if (eh_dp) {
            subset_sum_dp(conjunto, n, alvo);
        } else {
            subset_sum_backtracking(conjunto, n, alvo);
        }
        
        clock_gettime(CLOCK_MONOTONIC, &end);
        
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

    fprintf(csv, "%s,%s,%d,%.4f,%.4f\n", algoritmo, cenario, n, media, desvio_padrao);
    
    fflush(csv); 

}

int main(){

    srand(time(NULL));

    int tamanhos[] = {10, 20, 30};
    int num_tamanhos = sizeof(tamanhos) / sizeof(tamanhos[0]);

    FILE *csv = fopen("../dados/resultados_c.csv", "w");
    if (csv == NULL) {
        printf("Erro: Crie uma pasta chamada 'dados' no diretorio anterior!\n");
        return 1;
    }
    fprintf(csv, "Algoritmo, Cenario, Tamanho_N, Tempo_Medio_ms, Desvio_Padrao_ms\n");

    FILE *entradas_py = fopen("../dados/entradas_compartilhadas.txt", "w");

    printf("Iniciando bateria de testes. Isso pode demorar alguns minutos...\n");

    for (int t = 0; t < num_tamanhos; t++) {

        int n = tamanhos[t];

        int *vetor_melhor = (int*)malloc(n * sizeof(int));
        int *vetor_medio = (int*)malloc(n * sizeof(int));
        int *vetor_pior = (int*)malloc(n * sizeof(int));

        // 1. GERANDO MELHOR CASO
        vetor_melhor[0] = 150;
        int alvo_melhor = 150;
        for (int i = 1; i < n; i++) vetor_melhor[i] = rand() % 100 + 1;

        // 2. GERANDO CASO MÉDIO
        int soma_parcial = 0;
        for (int i = 0; i < n; i++) {
            vetor_medio[i] = rand() % 100 + 1;
            if (i % 3 == 0) soma_parcial += vetor_medio[i];
        }
        int alvo_medio = soma_parcial;  // alvo existe mas requer busca

        // 3. GERANDO PIOR CASO
        int soma_total = 0;
        for (int i = 0; i < n; i++) {
            vetor_pior[i] = (rand() % 50 + 1) * 2;
            soma_total += vetor_pior[i];
        }
        int alvo_pior = soma_total + 1; // ímpar inatingível

        // EXPORTANDO AS ENTRADAS PARA PYTHON LER
        fprintf(entradas_py, "TAMANHO:%d\n", n);
        
        fprintf(entradas_py, "ALVO_MELHOR:%d\nVETOR_MELHOR:", alvo_melhor);
        for(int i=0; i<n; i++) fprintf(entradas_py, "%d,", vetor_melhor[i]);
        
        fprintf(entradas_py, "\nALVO_MEDIO:%d\nVETOR_MEDIO:", alvo_medio);
        for(int i=0; i<n; i++) fprintf(entradas_py, "%d,", vetor_medio[i]);
        
        fprintf(entradas_py, "\nALVO_PIOR:%d\nVETOR_PIOR:", alvo_pior);
        for(int i=0; i<n; i++) fprintf(entradas_py, "%d,", vetor_pior[i]);
        
        fprintf(entradas_py, "\n---\n");

        fflush(entradas_py); 

        // EXECUTANDO OS TESTES (Backtracking)
        testar_e_salvar("Backtracking", "Melhor Caso", n, vetor_melhor, alvo_melhor, csv, false);
        testar_e_salvar("Backtracking", "Caso Medio", n, vetor_medio, alvo_medio, csv, false);
        testar_e_salvar("Backtracking", "Pior Caso", n, vetor_pior, alvo_pior, csv, false);

        // EXECUTANDO OS TESTES (Programação Dinâmica)
        testar_e_salvar("DP", "Melhor Caso", n, vetor_melhor, alvo_melhor, csv, true);
        testar_e_salvar("DP", "Caso Medio", n, vetor_medio, alvo_medio, csv, true);
        testar_e_salvar("DP", "Pior Caso", n, vetor_pior, alvo_pior, csv, true);

        // Liberando memória
        free(vetor_melhor);
        free(vetor_medio);
        free(vetor_pior);
        
        printf("Concluido tamanho n=%d...\n", n);
    }

    fclose(csv);
    fclose(entradas_py);
    printf("Todos os testes finalizados! Resultados em dados/resultados_c.csv\n");

    return 0;
}