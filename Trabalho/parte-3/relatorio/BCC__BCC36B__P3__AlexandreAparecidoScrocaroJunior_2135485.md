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

&nbsp;&nbsp;A tabela de símbolos é um vetor de objetos (que possuem todas informações de variáveis ou funções), para preenchê-lo, é utilizida a PreOrderIter para iterar a árvore gerada na análise sintática.

&nbsp;&nbsp;Para encontrar declarações de variáveis com somente uma variável, é analisado se o nó atual da iteração possui o nome 'declaracao_variaveis' e possui apenas um filho e então define-se qual variavel é na contagem (1, 2, 3...), tipo, nome, dimensão, índice, token, estado e escopo, então adiciona-se um objeto com essas informações em um vetor que contém todas variáveis (se ela já não existe no vetor). Já para declarações com duas variáveis, analisa-se se o nó atual da iteração possui o nome 'declaracao_variaveis' e seu filho 'lista_variaveis' possui mais de uma variável, e então define-se as mesmas informações anteriores para as duas variáveis. Para declarações com mais de 2 variáveis, é verificado se o nó atual da iteração possui o nome 'declaracao_variaveis' e se seu filho 'lista_variaveis' possui outro filho 'lista_variaveis' e então são definidas as mesmas informações anteriores para todas variáveis.

&nbsp;&nbsp;Já para encontrar funções, é verificado se o nó atual da iteração possui o nome 'declaracao_funcao', se for são definidas informações como qual objeto é na contagem (1, 2, 3...), token, estado, tipo do retorno, quantidade de parâmetros formais (e quais são esses parâmetros), além de inserir cada um dos parâmetros na lista de variáveis.

#### Funções de checagem

Essas funções irão informar os erros e alertas definidos na seção de regras do presente documento. Mas é importante informar que, além dos erros ou avisos lançados nessas funções, alguns são emitidos já na construção da tabela de símbolos.

&nbsp;&nbsp;check_main:\
&nbsp;&nbsp;Percorre toda a tabela de símbolos em busca da função principal.

&nbsp;&nbsp;check_functions:\
&nbsp;&nbsp;Percorre toda a tabela de símbolos e verifica o retorno das funções - se tem retorno, se retorna o tipo correto e se a variável que está sendo retornada existe. Além disso, percorre toda a árvore em busca de chamadas de função e verifica se há chamadas para função principal, se a função chamada existe e se a quantidade de parâmetros reais coincide com os parâmetros formais. Ao fim da função, percorre a tabela de símbolos e verifica se a função foi utilizada.

&nbsp;&nbsp;check_vars:\
&nbsp;&nbsp;Percorre a tabela de símbolos atualizando o estado das variáveis que participam de atribuições - verifica variáveis que não são utilizadas. Além de percorrer a árvore buscando por variáveis que são utilizadas sem serem definidas.

&nbsp;&nbsp;check_multi_dimensional_vars:\
&nbsp;&nbsp;Percorre a árvore e busca por variáveis que são vetores ou matrizes, verifica se está sendo utilizado um índice com valor em ponto flutuante e se o índice utilizado está fora do intervalo permitido.

&nbsp;&nbsp;check_assignments:\
&nbsp;&nbsp;Percorre a árvore e busca por variáveis. Verifica se a variável está recebendo um valor compatível com seu tipo e se a variável existe (assim como a variável que a está sendo atribuída)

#### Funções auxiliares

Encontradas no arquivo utils.py, são partes do código que se repetem e são transformadas em métodos. Por conta da falta de tempo só fiz isso para uma função, mas acredito que seria possível fazer para outras partes, como a verificação do índex ou dimensão da variável.

&nbsp;&nbsp;find_scope:\
&nbsp;&nbsp;Verifica se o pai do nó atual é 'declaracao', se for o tipo é global, senão a variável se encontra dentro de uma função, então percorre a árvore verticalmente para cima até chegar ao cabeçalho da função e atribui o escopo da variável como o nome da função.

---

### Árvore Sintática Abstrata

Após a análise semântica, é gerada uma árvore abstrata por meio da função 'cut_tree'. Essa árvore consiste em uma árvore simplificada da árvore gerada na análise sintática. Abaixo podem ser observadas imagens que exemplificam essa simplificação.

&nbsp;&nbsp;cut_tree:\
&nbsp;&nbsp;Percorre toda a árvore e verifica todos os nós que possuem apenas um filho e esse filho também possui filhos (assim é possível remover um nó) e então atualiza os filhos do nó.

#### Exemplo de poda da árvore
##### Entrada
![image](https://user-images.githubusercontent.com/37521313/198850061-9b6fe767-ce6c-46bb-b640-dcf426f498e9.png)
##### Saída
![image](https://user-images.githubusercontent.com/37521313/198850070-68614a61-61aa-4132-ba6a-c2441212f161.png)


---

### Exemplos de Entrada e Saída

#### sema-004.tpp (código de teste)

**Entrada:**

```cpp
inteiro: a
inteiro: b

inteiro principal()
	a := 10
fim

```

**Saída:**

TERMINAL:
![image](https://user-images.githubusercontent.com/37521313/198850127-c4cb4b7a-8c2a-4703-b4d8-326d61f5c579.png)


ÁRVORE REDUZIDA:
![image](https://user-images.githubusercontent.com/37521313/198850157-a8fafee9-3258-4641-80c7-f1b8834d2a19.png)


#### sema-013.tpp (código de teste)

**Entrada:**

```cpp
flutuante: a
inteiro: b

inteiro func()
  a := 10
  principal()
  retorna(a)
fim

inteiro principal()
	b := 18
	a := func()
fim


```

**Saída:**

TERMINAL:
![image](https://user-images.githubusercontent.com/37521313/198850183-91566dd3-134c-4591-81d2-71e7d2145951.png)


ÁRVORE REDUZIDA:
![image](https://user-images.githubusercontent.com/37521313/198850192-7a7f55a1-1c9b-4b02-ac05-03dcff4393a4.png)


---

### Tabela de símbolos

A tabela de símbolos consiste em um vetor de objetos, os quais contém todas informações necessárias (para a análise semântica) de vetores e funções. Sua implementação foi explanada na seção 'Detalhes da implementação' do presente documento. Essa tabela é usada para descobrir erros ou inconsistências (alertas)

---

### Referências

[Documentação do anytree](https://anytree.readthedocs.io/en/latest/)\
Slides do professor
