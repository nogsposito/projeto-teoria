def subset_sum_dp(conjunto: list[int], n: int, alvo: int) -> bool:
    """
    Função com Programação Dinâmica (Bottom-Up) para o Subset Sum.
    Constrói uma tabela dp[i][j] que indica se é possível atingir
    a soma j usando os primeiros i elementos do conjunto.
    """

    # alocação da tabela dp como lista de listas
    dp = [[False] * (alvo + 1) for _ in range(n + 1)]

    # caso base 1: alvo == 0 sempre é possível (subconjunto vazio)
    for i in range(n + 1):
        dp[i][0] = True

    # caso base 2: conjunto vazio, alvo > 0 → impossível
    for j in range(1, alvo + 1):
        dp[0][j] = False

    # preenchendo a tabela dp
    for i in range(1, n + 1):
        for j in range(1, alvo + 1):
            if conjunto[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - conjunto[i - 1]]

    return dp[n][alvo]
