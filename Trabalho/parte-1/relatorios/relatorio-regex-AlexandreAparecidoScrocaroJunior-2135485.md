# Relatório com as expressões regulares do trabalho de Análise Léxica

**Autor:** Alexandre Aparecido Scrocaro Junior \
**R.A.:** 2135485

## Tokens simples

### Símbolos

| TOKEN           | EXPRESSÃO REGULAR |
| --------------- | ----------------- |
| MAIS            | \+                |
| MENOS           | -                 |
| VEZES           | \*                |
| DIVIDE          | /                 |
| DOIS_PONTOS     | :                 |
| VIRGULA         | ,                 |
| ABRE_PARENTESE  | \(                |
| FECHA_PARENTESE | \)                |
| ABRE_COLCHETE   | \[                |
| FECHA_COLCHETE  | \]                |
| ATRIBUICAO      | :=                |

### Operadores Lógicos.

| TOKEN | EXPRESSÃO REGULAR |
| ----- | ----------------- |
| E     | &&                |
| OU    | \|\|              |
| NAO   | !                 |

### Operadores Relacionais.

| TOKEN       | EXPRESSÃO REGULAR |
| ----------- | ----------------- |
| MENOR       | <                 |
| MAIOR       | >                 |
| IGUAL       | =                 |
| DIFERENTE   | <>                |
| MENOR_IGUAL | <=                |
| MAIOR_IGUAL | >=                |

## Tokens compostos

| TOKEN                  | EXPRESSÃO REGULAR                                                     |
| ---------------------- | --------------------------------------------------------------------- |
| digito                 | [0-9]                                                                 |
| letra                  | [a-zA-ZáÁãÃàÀéÉíÍóÓõÕ]                                                |
| sinal                  | [-+]?                                                                 |
| ID                     | (([a-zA-ZáÁãÃàÀéÉíÍóÓõÕ])(([0-9]) \| \_ \| ([a-zA-ZáÁãÃàÀéÉíÍóÓõÕ]))) |
| NUM_INTEIRO            | \d+                                                                   |
| NUM_PONTO_FLUTUANTE    | \d+[eE][-+]?\d+ \| (\\.\d+ \| \d+ . \d\*)([eE][-+]?\d+)?              |
| NUM_NOTACAO_CIENTIFICA | [-+]?([1-9]).\d+[eE][-+]?\d+                                          |

## Tokens especiais

| TOKEN           | EXPRESSÃO REGULAR |
| --------------- | ----------------- |
| Quebra de linha | \n+               |

## Tokens de palavras reservadas

| TOKEN     | EXPRESSÃO REGULAR |
| --------- | ----------------- |
| SE        | se                |
| ENTAO     | então             |
| SENAO     | senão             |
| FIM       | fim               |
| REPITA    | repita            |
| ATE       | até               |
| LEIA      | leia              |
| ESCREVA   | escreva           |
| RETORNA   | retorna           |
| INTEIRO   | inteiro           |
| FLUTUANTE | flutuante         |
