# Projeto de Implementação de um Compilador para a Linguagem TPP: Geração de código intermediário (Trabalho – 4ª parte)

**Autor:** Alexandre Aparecido Scrocaro Junior \
**email:** alescrocaro@gmail.com

**Professor:** Rogério Aparecido Gonçalves\
**Universidade Tecnológica Federal do Paraná (UTFPR)**

## Geração de código intermediário

### Resumo do projeto

A quarta parte do trabalho consiste na implementação de um gerador de código intermediário para a linguagem de programação TPP. O gerador foi desenvolvido em Python e conta com uma função principal - que verifica o conteúdo de funções, além de chamar outras duas funções auxiliares que vão alocar as variáveis globais e locais. A biblioteca utilizada para auxiliar a geração do código intermediário foi a llvmlite (biblioteca que vincula Python a LLVM, para escrever compiladores). Além de utilizar o módulo LevelOrderIter da biblioteca Anytree para percorrer a árvore abstrata gerada na análise semântica.

---

### Introdução

A Geração de Código é a tarefa final de um compilador, o código executável para uma máquina - que deve representar fielmente a semântica do código-fonte. Esta fase é uma das mais complexas de um compilador, porque não depende apenas da linguagem de programação usada no código fonte, mas também de detalhes da arquitetura, da estrutura do ambiente de execução e do Sistema Operacional da máquina na qual o código será executado. A geração de código envolve tentativas de aplicar melhorias no código: velocidade, tamanho e ajustes de acordo com a arquitetura-alvo (como registradores, modos de endereçamento e memória).

Devido à complexidade desta fase, o compilador a divide em alguns passos que vão necessitar de um tipo de código abstrato, chamado de código intermediário - que é o objetivo deste trabalho, para tanto precisa-se do llvm.

---

### LLVM

O Projeto LLVM é uma infraestrutura para o desenvolvimento de ferramentas de compilação. Um código LLVM-IR (IR = Intermediate Representation) é organizado em containers, os principais componentes são: módulo, função, bloco básico e instrução.

O módulo representa um arquivo com código fonte ou uma unidade de tradução. Todo o restante do código deve estar dentro de um módulo. As funções estão contidadas em um módulo e irão conter partes do código, elas são declaradas com seus nomes e seus argumentos, uma função é um container de BasicBlocks. O bloco básico é um pedaço contíguo de instruções (como um bloco de código). Uma instrução é uma operação única expressa em um código. Podendo ser uma opção como uma adição de inteiros, ou uma instrução de load/store da/para memória.

![image](https://user-images.githubusercontent.com/37521313/205456301-c6c3f8e9-d940-417d-a12a-a6c0fe6e58f1.png)

#### Utilização da API do LLVM no projeto

Importação:

```Python
from llvmlite import ir, binding as llvm
```

Criando módulo

```Python
module = ir.Module('test_{}.bc'.format(test_number)) # test_number = 001 ou similar
```

Salvando módulo

```Python
file = open('geracao-codigo-testes/gencode-{}.ll'.format(test_number), 'w')
file.write(str(module))
file.close()
```

Declarando função

```Python
from llvmlite import ir, binding as llvm
```

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
![image](https://user-images.githubusercontent.com/37521313/198850740-f5cf9823-cac6-4ac2-83ac-2d7fc04cb272.png)

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
![image](https://user-images.githubusercontent.com/37521313/198850752-db98e943-35fc-41b5-a253-f0c1b8fbf2aa.png)

ÁRVORE REDUZIDA:
![image](https://user-images.githubusercontent.com/37521313/198850192-7a7f55a1-1c9b-4b02-ac05-03dcff4393a4.png)

---

### Tabela de símbolos

A tabela de símbolos consiste em um vetor de objetos, os quais contém todas informações necessárias (para a análise semântica) de vetores e funções. Sua implementação foi explanada na seção 'Detalhes da implementação' do presente documento. Essa tabela é usada para descobrir erros ou inconsistências (alertas)

---

### Referências

[Documentação do anytree](https://anytree.readthedocs.io/en/latest/)\
Slides do professor Rogério Aparecido Gonçalves ministrados na matéria de Compiladores;\
Além de seu repositório [llvm-gencode-samples](https://github.com/rogerioag/llvm-gencode-samples], que contém exemplos da utilização do llvm em Python.
