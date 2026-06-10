def subset_sum_backtracking(conjunto: list[int], n: int, alvo: int) -> bool:
    """
    Função recursiva de força bruta (Backtracking) para o Subset Sum.
    Explora todas as combinações possíveis de inclusão/exclusão de elementos.
    """

    # casos base
    if alvo == 0:
        return True
    if n == 0 and alvo != 0:
        return False

    # se o último elemento for maior que o alvo, ele não pode ser incluído
    if conjunto[n - 1] > alvo:
        return subset_sum_backtracking(conjunto, n - 1, alvo)

    # explora as duas possibilidades: incluir ou excluir o último elemento
    return (
        subset_sum_backtracking(conjunto, n - 1, alvo)
        or subset_sum_backtracking(conjunto, n - 1, alvo - conjunto[n - 1])
    )
