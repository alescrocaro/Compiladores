# Relatório com as expressões regulares do trabalho de Análise Léxica

**Autor:** Alexandre Aparecido Scrocaro Junior \
**R.A.:** 2135485

## Análise Léxica

### Especificação da linguagem de programação TPP

A linguagem TPP
Tipos básicos de dados suportado: inteiro e flutuante
• Suporte a arranjos uni e bidimensionais (arrays)
• Exemplos:
• tipo: identificador[dim]
• tipo: identificador[dim][dim]
• Variáveis locais e globais devem ter um dos tipos especificados
• Tipos de funções podem ser omitidos (quando omitidos viram um
procedimento e um tipo void é devolvido explicitamente
• Linguagem quase fortemente tipificada: nem todos os erros são
especificados mas sempre deve ocorrer avisos
• Operadores aritméticos: +, -, \* e /
• Operadores lógicos: e (&&), ou (||) e não (!)

### Especificação formal dos autômatos para a formação de cada classe de token da linguagem

### Detalhes da implementação da varredura na LP e ferramenta (e/ou bibliotecas) escolhidas pelo projetista

### Exemplos de saída do sistema de varredura (lista de tokens) para exemplos de entrada (código fonte)

### Implemente uma função que imprima a lista de tokens, não utilize a saída padrão da ferramenta de implementação de Analisadores Léxicos

### Utilize o formato de artigo da SBC2 para fazer o relatório. (PODE FAZER EM MARKDOWN)

### ttetes

- Será avaliado o funcionamento da varredura para a linguagem de programação TPP.
  - Varredura: programa de exemplo TPP de entrada na linha de comando.
  - Saída será o conjunto de pares (valor:token).
- Utilizar palavras reservadas em português (pt-BR)
- Construção da Análise Léxica;
- Inserção de comentários (para adicionar explicações futuras no código);
- Levantamento de erros (sugerindo classes de erros). Para isso: Contabilizar linhas (\n), colunas e lexema atual (as ferramentas fazem isso);
