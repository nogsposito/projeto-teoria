#include <stdbool.h>
#include <stdlib.h>

// função com programação dinâmica
bool subset_sum_dp(int conjunto[], int n, int alvo){

    // alocação dinâmica
    bool **dp = (bool **)maloc((n+1) * sizeof(bool *));
    for (int i = 0; i <= n; i++){
        dp[i] = (bool *)malloc((alvo + 1) * sizeof(bool));
    }

    // se alvo é 0, resposta eé verdadeira (subconjunto vazio)
    for (int i = 0; i <= n; i++) dp[i] = true;

    // se alvo > 0 e conjunto é vazio, resposta é falsa
    for (int j = 1; j <= alvo; j++) dp[j] = false;

    // preenchendo a tabela dp
    for (int i = 1; i <= n; i++){
        for (int j = 1; j <= alvo; j++){

            if (conjunto[i-1] > j){
                
                dp[i][j] = dp[i-1][j];

            } else {
                
                dp[i][j] = dp[i - 1][j] || dp[i - 1][j - conjunto[i - 1]];
            
            }
        }
    }
    
    bool resultaado = dp[n][alvo];

    // liberação da memória alocada
    for (int i = 0; i <= n; i++) free(dp[i]);
    free(dp);

    return resultaado;

}