#include <stdbool.h>
#include <stdlib.h>

// função com programação dinâmica
bool subset_sum_dp(int conjunto[], int n, int alvo){

    // alocação dinâmica
    bool **dp = (bool **)malloc((n+1) * sizeof(bool *));
    for (int i = 0; i <= n; i++){
        dp[i] = (bool *)malloc((alvo + 1) * sizeof(bool));
    }

    for (int i = 0; i <= n; i++) {
        dp[i][0] = true;  // CORREÇÃO: dp na linha i, coluna 0
    }

    // 2. Se o alvo > 0 e o conjunto está vazio (linha 0), a resposta é falsa
    for (int j = 1; j <= alvo; j++) {
        dp[0][j] = false; // CORREÇÃO: dp na linha 0, coluna j
    }
    
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
    
    bool resultado = dp[n][alvo];

    // liberação da memória alocada
    for (int i = 0; i <= n; i++) free(dp[i]);
    free(dp);

    return resultado;

}