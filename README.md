# projeto-teoria


### DOCUMENTAÇÃO DO AMBIENTE DE EXECUÇÃO (C)

Para garantir a validade e seguir a metodologia de isolamento, os testes da implementação em C foram executados no seguinte ambiente:

- Processador (CPU): 12th Gen Intel(R) Core(TM) i5-1235U

- Memória RAM: 16 GB

- Sistema Operacional: Windows 11

- Compilador Utilizado: GCC (GNU Compiler Collection) versão 14.2.0

- Comando e Flags de Compilação: Foi utilizado o comando gcc benchmark.c backtracking.c dp.c -o benchmark -lm. A flag -lm foi explicitamente utilizada para linkar a biblioteca matemática (<math.h>), necessária para o cálculo do desvio-padrão dos tempos medidos.

- Condições de Execução: Durante a execução das 30 rodadas dos testes com o clock_gettime(), os aplicativos em segundo plano foram fechados para evitar ruídos e interferências do escalonador do Sistema Operacional nas métricas de tempo.
