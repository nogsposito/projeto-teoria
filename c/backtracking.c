#include <stdbool.h>

// função recursiva de força bruta
bool subset_sum_backtracking(int conjunto[], int n, int alvo){

    // casos base
    if (alvo == 0) return true;
    if (n == 0 && alvo != 0) return false;

    // se o último elemento for maior que o alvo, ele não pode ser incluído
    if (conjunto[n-1] > alvo){
        return subset_sum_backtracking(conjunto, n-1, alvo);
    }

    // explora as duas possibilidades: incluir ou excluir o último elemento
    return subset_sum_backtracking(conjunto, n-1, alvo) || subset_sum_backtracking(conjunto, n-1, alvo - conjunto[n-1]);

}