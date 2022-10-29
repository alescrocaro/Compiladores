# Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Semântica (Trabalho – 3ª parte)

**Autor:** Alexandre Aparecido Scrocaro Junior \
**email:** alescrocaro@gmail.com

**Professor:** Rogério Aparecido Gonçalves\
**Universidade Tecnológica Federal do Paraná (UTFPR)**

## Análise Semântica

### Resumo

A terceira parte do trabalho consiste na implementação de um analisador semântico para a linguagem de programação TPP. O analisador foi desenvolvido em Python e conta com cinco funções principais - para fazer verificações e criar uma tabela de símbolos, além de uma função auxiliar para determinar o escopo de uma variável, e outra para podar a árvore. Para criação da tabela de símbolos foi utilizado um vetor de objetos.
Além de utilizar, a biblioteca Anytree para auxiliar ao percorrer a árvore sintática e para gerar a árvore abstrata.

---

### Especificação dos Autômatos

TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

---

### Regras Semânticas

As regras semânticas irão identificar os erros semânticos, o ideal seria utilizar o _raise Exception_ ao encontrar algum erro e parar a execução do programa, entretanto, foi utilizado o _print_, assim é possivel visualizar todos os erros do código. Essas regras foram definidas no documento de requisitos disponibilizado pelo professor e geram saídas de erro ou aviso. São elas:

#### Funções e Procedimentos

- Função Principal:\
  Todo programa escrito em TPP deve ter uma função principal declarada.
  Caso essa função não exista, a seguinte mensagem é apresentada:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Função principal não declarada

  A função principal é do tipo inteiro, assim é esperado que seu retorno também seja um valor inteiro, do contrário a seguinte mensagem é emitida:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Função principal deveria retornar inteiro, mas retorna vazio

  Uma função qualquer não pode fazer uma chamada à função principal. Deve ser verificado se existe alguma chamada para a função principal partindo de qualquer outra função do programa. Se houver, a seguinte mensagem aparece:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Chamada para a função principal não permitida.

  Se a função principal fizer uma chamada para ela mesma, a mensagem de aviso é emitida:

  &nbsp;&nbsp;&nbsp;&nbsp;Aviso: Chamada recursiva para principal.

- Parâmetros:\
  A quantidade de parâmetros reais de uma chamada de função deve ser igual a quantidade de parâmetros formais da sua definição. Caso contrário, gera a mensagem:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Chamada à função 'exemplo' com 2 parâmetros, mas foram declarados 3

- Retorno:\
  Uma função deve retornar um valor de tipo compatível com o tipo de retorno declarado. Se a função principal que é declarada com retorno inteiro, não apresenta um retorna(0), a seguinte mensagem é gerada:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Função principal deveria retornar inteiro, mas retorna vazio.

  Quando a função não é a principal, a mensagem mostrada é:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Função principal deveria retornar inteiro, mas retorna vazio.

- Declaração:\
  Funções precisam ser declaradas antes de serem chamadas. Caso contrário a seguinte mensagem de erro é emitida:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Chamada a função 'exemplo' que não foi declarada.

- Utilização:\
  Uma função pode ser declarada e não utilizada. Se isto acontecer a seguinte mensagem de aviso é emitida:

  &nbsp;&nbsp;&nbsp;&nbsp;Aviso: Função ‘func’ declarada, mas não utilizada.

#### Variáveis

Informações da variável - como tipo, nome, escopo - são armazenadas na tabela de símbolos. Ela pode ser declarada no escopo do procedimento, como expressão ou parâmetro formal, ou no escopo global.

- Utilização:\
  Se uma variável ‘a’ for apenas declarada e não for inicializada (escrita) ou não for utilizada (não lida), o analisador gera a mensagem:

  &nbsp;&nbsp;&nbsp;&nbsp;Aviso: Variável ‘a’ declarada e não utilizada.

  Se houver a tentativa de leitura ou escrita de qualquer variável não declarada, a seguinte mensagem é emitida:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Variável ‘a’ não declarada.

  Se uma variável ‘a’ for declarada duas vezes no mesmo escopo, o aviso é emitido:

  &nbsp;&nbsp;&nbsp;&nbsp;Aviso: Variável ‘a’ já declarada anteriormente

- Atribuição:\
  Na Atribuição, é verificado se os tipos da variável que está recebendo e o que ela está recebendo são compatíveis.

  Se uma variável do tipo inteiro receber uma expressão, função ou número do tipo flutuante, a seguinte mensagem é mostrada:

  &nbsp;&nbsp;&nbsp;&nbsp;Aviso: Atribuição de tipos distintos, ‘a’ eh inteiro e recebe 'expressao || retorno_da_funcao || numero' do tipo flutuante

  O contrário também pode acontecer, e então é mostrada a seguinte mensagem:

  &nbsp;&nbsp;&nbsp;&nbsp;Aviso: Atribuição de tipos distintos, ‘a’ eh flutuante e recebe 'expressao || retorno_da_funcao || numero' do tipo inteiro

#### Arranjos

- Índice:\
  Na linguagem TPP é possível declarar arranjos, pela sintaxe da linguagem o índice de um arranjo é inteiro e isso deve ser verificado - na tabela de símbolos são guardados a dimensão (0 para escalar, 1 para unidimensionais, 2 para bidimensionais e assim por diante) e o índice.

  Se o índice não for inteiro, a seguinte mensagem é emitida:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: Índice de array ‘X’ não inteiro.

  Se o acesso ao elemento do arranjo estiver fora de sua definição, por exemplo um vetor A é declarado como tendo 10 elementos (0 a 9) e há um acesso ao A[10], a seguinte mensagem de erro é apresentada:

  &nbsp;&nbsp;&nbsp;&nbsp;Erro: índice de array ‘A’ fora do intervalo

---

### Detalhes da implementação

Como o código está todo comentado, para facilitar a compreensão, e algumas funções possuem muitas linhas, nesta seção não irei utilizar capturas de tela.

#### Bibliotecas

Para percorrer a árvore foi utilizada a biblioteca Anytree, mais especificamente seus métodos LevelOrderIter, que percorre a árvore aplicando a estratégia level-order (por nível) e começa no nó passado, PreOrderIter, que percorre a árvore aplicando a estratégia de pre-order (percorre verticalmente até chegar na folha, quando encontrar folha volta e procura pelas próximas folhas) e começa no nó passado, além do UniqueDotExporter, do Anytree.exporter que foi utilizado para gerar a árvore abstrata. Também foram utilizados a análise sintática desenvolvida na parte dois do trabalho e o arquivo utils, que possui uma função para encontrar o escopo de uma variável.

#### Tabela de símbolos

---

### Árvore Sintática Abstrata

TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO \

---

### Exemplos de Entrada e Saída

TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO \

#### codigo xxxxxxxxxxx

**Entrada:**

```cpp



```

**Saída:**

TERMINAL:

ÁRVORE REDUZIDA:

#### codigo yyyyyyyyyyyyy

**Entrada:**

```cpp


```

**Saída:**

TERMINAL:

ÁRVORE REDUZIDA:

---

### Tabela de símbolos

TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO \

---

### Referências

TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO \

[Documentação do anytree](https://anytree.readthedocs.io/en/latest/)\
[Documentação do PLY (e Yacc)](https://www.dabeaz.com/ply/ply.html)\
Slides do professor
