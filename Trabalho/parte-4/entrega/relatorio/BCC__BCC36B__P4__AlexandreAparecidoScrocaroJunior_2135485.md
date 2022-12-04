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

### Detalhes da implementação

#### Bibliotecas

A biblioteca utilizada para fazer as chamadas à api do LLVM foi a llvmlite (biblioteca que vincula Python a LLVM). Além disso, para percorrer a árvore foi utilizada a biblioteca Anytree, mais especificamente seu método LevelOrderIter, que percorre a árvore aplicando a estratégia level-order (por nível) e começa no nó passado.

#### Utilização da API do LLVM no projeto

```Python
# Importação
from llvmlite import ir, binding as llvm

# Inicialização do LLVM
llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Criando e inicializando o módulo
module = ir.Module('test_{}.bc'.format(test_number)) # test_number = 001 ou similar
module.triple = llvm.get_process_triple()
target = llvm.Target.from_triple(module.triple)
target_machine = target.create_target_machine()
module.data_layout = target_machine.target_data

# Declarando variavel global inteira com nome a
# para uma var do tipo flutuante basta trocar ir.IntType(32) por ir.FloarType()
var = ir.GlobalVariable(module, ir.IntType(32), 'a')
var.initializer = ir.Constant(ir.IntType(32), 0) # Definindo constante 0 para inicialização da var
var.linkage = "common"
var.align = 4 # Definindo alinhamento


# Declarando função
function = ir.Function(module, ir.FunctionType(ir.IntType(32), []), name=function_name)
# se a funcao for a principal basta trocar function_name por 'main'

# Declarando bloco de entrada
entry_block = function.append_basic_block('entry')

# Adicionando bloco de entrada
builder = ir.IRBuilder(entry_block)

# Criando variável inteira (local)
var_local = builder.alloca(ir.IntType(32), name=var_name)
var.align = 4

# Atribuindo number à variavel a
builder.store(ir.Constant(ir.IntType(32), number), var_code)
# Atribuindo var2 à var1
builder.store(builder.load(var2), var1)

# escrevendo inteiro
print_integer = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.IntType(32)]), 'escrevaInteiro')

builder.call(print_integer, args=[builder.load(var)])

# escrevendo flutuante
print_float = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.FloatType()]), 'escrevaFlutuante')
builder.call(print_float, args=[builder.load(var)])

# Declarando inicio do repita
repeat_start = function.append_basic_block('repeat_start')
builder.branch(repeat_start)
builder.position_at_end(repeat_start)

# Declarando fim do repita
repeat_end = function.append_basic_block('repeat_end')
builder.cbranch(check_repeat, repeat_start, repeat_end)
builder.position_at_end(repeat_end)


# Declarando bloco de saida
exit_block = function.append_basic_block('exit')

# Adicionando bloco de saida
builder.branch(exit_block)
builder = ir.IRBuilder(exit_block)

# Salvando módulo
file = open('geracao-codigo-testes/gencode-{}.ll'.format(test_number), 'w')
file.write(str(module))
file.close()
```

---

#### Código e explicações

importações:

```Python
from llvmlite import ir, binding as llvm
from anytree import LevelOrderIter
```

##### Função init_global_vars:

Esta função percorre todas as variáveis globais da tabela de símbolos e as inicializa, sendo assim inicializa todas variáveis globais do código. É chamada dentro da função generate_i_code

Parâmetros:

- symbols_table: tabela de símbolos gerada na análise semântica.
- module: módulo inicializado na função generate_i_code

```Python
def init_global_vars(symbols_table, module):
    for var in symbols_table:
        if var['token'] == 'ID':
            if var['scope'] == 'global':
                if var['type'] == 'inteiro':
                    print('declaracao variavel => global => inteiro')
                    var['code'] = ir.GlobalVariable(module, ir.IntType(32), var['name'])
                    var['code'].initializer = ir.Constant(ir.IntType(32), 0)

                if var['type'] == 'flutuante':
                    print('declaracao variavel => global => flutuante')
                    var['code'] = ir.GlobalVariable(module, ir.FloatType(), var['name'])
                    var['code'].initializer = ir.Constant(ir.FloatType(), 0.0)

                var['code'].linkage = "common"
                var['code'].align = 4
```

##### Função alloca_local_vars:

Esta função percorre todas as variáveis locais (pela tabela de símbolos) da função passada e as inicializa, sendo assim inicializa todas variáveis locais da função, menos os parâmetros. É chamada dentro da função generate_i_code

Parâmetros:\

- symbols_table: tabela de símbolos gerada na análise semântica;
- builder: builder inicializado na função generate_i_code;
- function_name: nome da função que será tratada no momento.

```Python
def alloca_local_vars(symbols_table, builder, function_name):
    for var in symbols_table:
        if var['token'] == 'ID' and var['scope'] == function_name:
            if var['type'] == 'inteiro':
                print('declaracao variavel => scope={} => inteiro'.format(function_name))
                var['code'] = builder.alloca(ir.IntType(32), name=var['name'])

            if var['type'] == 'flutuante':
                print('declaracao variavel => scope={} => flutuante'.format(function_name))
                var['code'] = builder.alloca(ir.FloatType(), name=var['name'])

            var['code'].align = 4
```

##### Função generate_i_code:

Esta é a função principal do código. Além de inicializar o llvm e o módulo, ela chama as duas funções acima e lida com todas funções do código-fonte. Como o código é muito grande, vou comentar apenas seus detalhes e lógica abaixo.

Parâmetros:

- root: Nó da árvore a passado de
- symbols_table: tabela de símbolos gerada na análise semântica;
- builder: builder inicializado na função generate_i_code;
- function_name: nome da função que será tratada no momento.

Primeiramente, inicializei o llvm e o módulo, assim como defini o código para o leia inteiro e flutuante e escreva inteiro e flutuante.

Após isso chamei a função init_global_vars para inicializar todas as funções globais do código. Com isso feito, parti para a checagem das funções do código-fonte. Para tanto, percorri a tabela de símbolos, checando se o símbolo é função.

Em primeiro plano, checo se a função tem parâmetros e faço os devidos tratamentos para iniciar ela e seus params (se possuir), iniciando seu bloco de entrada (utilizando builder). E então é possível alocar suas variáveis locais.

Agora checo a árvore em busca do nó 'cabecalho' que indica o início de uma função. Então verifico se o nome da função encontrada existe na tabela de símbolos para evitar inconsistências. Com isso, é possível checar o corpo da função, para isso percorro o corpo até chegar no último nó de corpo e depois percorro esses corpos de baixo pra cima na árvore, isso é feito pois na árvore os corpos aparecem na ordem inversa ao código fonte, ou seja, a primeira linha de corpo no código fonte é o último nó de corpo na árvore. Para checar o corpo da função, checo qual é o nó de corpo atual, cada um deles é tratado individualmente, como apresentado abaixo:

- repita:\
  Primeiro inicio o bloco de entrada, e, para percorrer o corpo do repita, preciso realizar o mesmo procedimento feito para percorrer o corpo da função (percorrer de baixo pra cima). Então verifico cada corpo do repita e vejo se é 'leia' e utilizo o builder.store para fazer seu tratamento; 'escreva' e utilizo o builder.call e builder.load para fazer seu tratamento; 'atribuicao' checo se variável recebe um incremento ou decremento e faço seu tratamento com builder.add ou builder.sub e builder.call dando builder.load no numero do incremento/decremento, checo se a variável recebe uma chamada de função e uso builder.store, builder.call e builder.load. Por último verifico a expressao contida no 'até' e utilizo o builder.cbranch e builder.position_at_end para fazer seus tratamentos.

- leia:\
  Primeiro verifico se a variável a ser lida era inteiro ou flutuante e fiz o devido tratamento utilizando o ir.Function e builder.call dentro do builder.store.

- escreva:\
  Primeiro verifico se a variável a ser escrita era inteiro ou flutuante e fiz o devido tratamento utilizando o ir.Function e builder.load dentro do builder.call.

- atribuicao:\
  Primeiro verifico se a variável está recebendo outra variável e uso o builder.store para tratá-la; verifico se a variável está recebendo uma expressão aditiva então uso o builder.add e o builder.store para tratá-la; verifico se a variável está recebendo um número e uso o builder.store; verifico se a variável está recebendo uma chamada de função, checo os parametros passados e utilizo builder.load, call e o store para tratá-la.

- declaracao_variaveis:\
  A declaração de variáveis não é verificada aqui pois já foi feita a checagem de variáveis nas funções init_global_vars e alloca_local_vars.

Depois disso, verifico o retorno das funções. Primeiro verifico o retorno de variável, depois verifico o retorno de número e então de expressão aditiva (para este é necessário o builder.add ou builder.sub). Para todos é utilizado o builder.ret, que identifica o retorno de funções.

Então pulo para o bloco básico de saída da função.

Por último o módulo gerado é escrito em um arquivo e pode ser visualizado normalmente.

---

### Exemplo de Entrada e Saída

#### gencode-006.tpp (código de teste)

**Entrada:**

```cpp
inteiro: a
inteiro: b

inteiro principal()
	a := 10
fim

```

**Saída:**

```
; ModuleID = "test_006.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

define i32 @"soma"(i32 %"b", i32 %"a")
{
entry:
  %"b.1" = alloca i32, align 4
  %"a.1" = alloca i32, align 4
  %"a.2" = alloca i32
  %"b.2" = alloca i32
  %".4" = load i32, i32* %"a.2"
  %".5" = load i32, i32* %"b.2"
  %"add" = add i32 %".4", %".5"
  br label %"exit"
exit:
  %"func_soma_return" = add i32 %"b", %"a"
  ret i32 %"func_soma_return"
}

define i32 @"main"()
{
entry:
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 0, i32* %"i"
  br label %"repeat_start"
repeat_start:
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"a.1"
  %".6" = call i32 @"leiaInteiro"()
  store i32 %".6", i32* %"a"
  %".8" = call i32 @"leiaInteiro"()
  store i32 %".8", i32* %"b.1"
  %".10" = call i32 @"leiaInteiro"()
  store i32 %".10", i32* %"b"
  %".12" = load i32, i32* %"c"
  call void @"escrevaInteiro"(i32 %".12")
  %"1" = alloca i32
  %".14" = load i32, i32* %"1"
  %".15" = load i32, i32* %"i"
  %"increment" = add i32 %".15", %".14"
  %".16" = load i32, i32* %"i"
  call void @"escrevaInteiro"(i32 %".16")
  %"var_for_compare" = load i32, i32* %"i", align 4
  %"check_repeat" = icmp eq i32 %"var_for_compare", 5
  br i1 %"check_repeat", label %"repeat_start", label %"repeat_end"
repeat_end:
  br label %"exit"
exit:
  ret i32 0
}
```

---

### Referências

Slides do professor Rogério Aparecido Gonçalves ministrados na matéria de Compiladores;\
Além de seu repositório [llvm-gencode-samples](https://github.com/rogerioag/llvm-gencode-samples], que contém exemplos da utilização do llvm em Python.

```

```
