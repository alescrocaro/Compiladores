# Relatório com as expressões regulares do trabalho de Análise Léxica

**Autor:** Alexandre Aparecido Scrocaro Junior \
**R.A.:** 2135485

## Tokens simples

### Símbolos

| TOKEN             | EXPRESSÃO REGULAR |
| ----------------- | ----------------- |
| t_MAIS            | \+                |
| t_MENOS           | -                 |
| t_MULTIPLICACAO   | \*                |
| t_DIVISAO         | /                 |
| t_ABRE_PARENTESE  | \(                |
| t_FECHA_PARENTESE | \)                |
| t_ABRE_COLCHETE   | \[                |
| t_FECHA_COLCHETE  | \]                |
| t_VIRGULA         | ,                 |
| t_ATRIBUICAO      | :=                |
| t_DOIS_PONTOS     | :                 |

### Operadores Lógicos.

| TOKEN       | EXPRESSÃO REGULAR |
| ----------- | ----------------- |
| t_E_LOGICO  | &&                |
| t_OU_LOGICO | \|\|              |
| t_NEGACAO   | !                 |

### Operadores Relacionais.

| TOKEN         | EXPRESSÃO REGULAR |
| ------------- | ----------------- |
| t_DIFERENCA   | <>                |
| t_MENOR_IGUAL | <=                |
| t_MAIOR_IGUAL | >=                |
| t_MENOR       | <                 |
| t_MAIOR       | >                 |
| t_IGUAL       | =                 |

## Tokens compostos

| TOKEN              | EXPRESSÃO REGULAR                                                     |
| ------------------ | --------------------------------------------------------------------- |
| digito             | [0-9]                                                                 |
| letra              | [a-zA-ZáÁãÃàÀéÉíÍóÓõÕ]                                                |
| sinal              | [-+]?                                                                 |
| id                 | (([a-zA-ZáÁãÃàÀéÉíÍóÓõÕ])(([0-9]) \| \_ \| ([a-zA-ZáÁãÃàÀéÉíÍóÓõÕ]))) |
| inteiro            | \d+                                                                   |
| flutuante          | \d+[eE][-+]?\d+ \| (\\.\d+ \| \d+ . \d\*)([eE][-+]?\d+)?              |
| notacao_cientifica | [-+]?([1-9]).\d+[eE][-+]?\d+                                          |

## Tokens especiais

| TOKEN           | EXPRESSÃO REGULAR |
| --------------- | ----------------- |
| Quebra de linha | \n+               |
