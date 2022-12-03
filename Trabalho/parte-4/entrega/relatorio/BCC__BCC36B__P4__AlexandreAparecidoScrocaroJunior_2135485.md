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
from utils import *
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
  Primeiro inicio o bloco de entrada, e, para percorrer o corpo do repita, preciso realizar o mesmo procedimento feito para percorrer o corpo da função (percorrer de baixo pra cima). Então verifico cada corpo do repita e vejo se é 'leia' e utilizo o builder.store para fazer seu tratamento; 'escreva' e utilizo o builder.call e builder.load para fazer seu tratamento; 'atribuicao' checo se variável recebe um incremento ou decremento e faço seu tratamento com builder.add ou builder.sub e builder.call dando builder.load no numero do incremento/decremento, checo se a variável recebe uma chamada de função e uso builder.store, builder.call e builder.load. Por último verifico a expressao contida no 'até'

- declaracao_variaveis

```Python
                                            # expressao do 'ate'/'until'
                                            if node_repita.children[3].name == 'expressao_simples':
                                                print('funcao => corpo => repita => expressao simples (ate)')
                                                node_repita_expressao_simples = node_repita.children[3]
                                                for var in symbols_table:
                                                    if var['name'] == node_repita_expressao_simples.children[0].children[0].name:
                                                        var_code = var['code']
                                                        var1_code = builder.load(var_code, 'b_cmp', align=4)


                                                if node_repita_expressao_simples.children[2].name == 'NUM_INTEIRO' or node_repita_expressao_simples.children[2].name == 'NUM_FLUTUANTE':
                                                    number2_code = ir.Constant(ir.IntType(32), node_repita_expressao_simples.children[2].children[0].name)

                                                node_relacional = node_repita_expressao_simples.children[1].children[0]

                                                if node_relacional.name == '=':
                                                    relacional = '=='
                                                    check_repeat = builder.icmp_signed(relacional, var1_code, number2_code, name='repeat_until_check')

                                                else:
                                                    check_repeat = builder.icmp_signed(node_relacional.name, var1_code, number2_code, name='repeat_until_check')

                                                builder.cbranch(check_repeat, repeat_start, repeat_end)
                                                builder.position_at_end(repeat_end)


                                        ###############################
                                        # se corpo atual eh leia
                                        ###############################
                                        if function_body.children[1].name == 'leia':
                                            print('funcao => corpo => leia')
                                            node_leia = function_body.children[1]

                                            for symbol in symbols_table:
                                                if symbol['type'] == 'inteiro' and symbol['name'] == node_leia.children[2].children[0].name:
                                                    print('funcao => corpo => leia => inteiro')
                                                    builder.store(builder.call(read_integer, []), symbol['code'])

                                                if symbol['type'] == 'flutuante' and symbol['name'] == node_leia.children[2].children[0].name:
                                                    print('funcao => corpo => leia => flutuante')
                                                    builder.store(builder.call(read_float, []), symbol['code'])


                                        ###############################
                                        # se corpo atual eh escreva
                                        ###############################
                                        if function_body.children[1].name == 'escreva':
                                            print('funcao => corpo => escreva')

                                            for var in symbols_table:
                                                if var['name'] == function_body.children[1].children[2].children[0].name:
                                                    if var['type'] == 'inteiro':
                                                        builder.call(print_integer, args=[builder.load(var['code'])])

                                                    if var['type'] == 'flutuante':
                                                        builder.call(print_float, args=[builder.load(var['code'])])


                                        ###############################
                                        # se corpo atual eh atribuicao
                                        ###############################
                                        if function_body.children[1].name == 'atribuicao':
                                            print('funcao => corpo => atribuicao')
                                            # se var nao recebe funcao
                                            if function_body.children[1].children[2].name != 'chamada_funcao':
                                                node_atribuicao = function_body.children[1]

                                                # obtem infos da variavel recebendo a atribuicao na tabela de simbolos
                                                for var in symbols_table:
                                                    if var['token'] == 'ID':
                                                        if var['name'] == node_atribuicao.children[0].children[0].name:
                                                            if 'code' in var:
                                                                var_code = var['code']
                                                                var_type = var['type']


                                                # var recebe var
                                                if node_atribuicao.children[2].name == 'ID':
                                                    print('funcao => corpo => atribuicao (var := var)')
                                                    for var in symbols_table:
                                                        if var['name'] == node_atribuicao.children[2].children[0]:
                                                            builder.store(builder.load(var['code']), var_code)

                                                # var recebe soma ou numero
                                                else:
                                                    # var recebe uma soma/sub de variaveis
                                                    if node_atribuicao.children[2].name == 'expressao_aditiva':
                                                        print('funcao => corpo => atribuicao => expressao aditiva')
                                                        # parcela 1 da soma/sub eh variavel
                                                        if node_atribuicao.children[2].children[0].name == 'ID':
                                                            print('funcao => corpo => atribuicao => expressao aditivaa => parc1 => ID')
                                                            for var in symbols_table:
                                                                if var['name'] == node_atribuicao.children[2].children[0].children[0].name:
                                                                    var1_loaded = builder.load(var['code'])

                                                        # parcela 2 da soma/sub eh variavel
                                                        if node_atribuicao.children[2].children[2].name == 'ID':
                                                            print('funcao => corpo => atribuicao => expressao aditivaa => parc2 => ID')
                                                            for var in symbols_table:
                                                                if var['name'] == node_atribuicao.children[2].children[2].children[0].name:
                                                                    var2_loaded = builder.load(var['code'])

                                                        for symbol in symbols_table:
                                                            if symbol['name'] == node_atribuicao.children[0].children[0].name:
                                                                store = symbol['code']

                                                        result = builder.add(var1_loaded, var2_loaded, name='atrib_expression_result')
                                                        builder.store(result, store)

                                                    else:
                                                        print('funcao => corpo => atribuicao (var := numero)')
                                                        number = node_atribuicao.children[2].children[0].name
                                                        if var_type == 'inteiro' and node_atribuicao.children[2].name == 'NUM_INTEIRO':
                                                            builder.store(ir.Constant(ir.IntType(32), number), var_code)


                                            # se var recebe funcao
                                            if function_body.children[1].children[2].name == 'chamada_funcao':
                                                print('funcao => corpo => atribuicao (var := func)')
                                                node_atribuicao = function_body.children[1]
                                                node_chamada_funcao = node_atribuicao.children[2]

                                                for func in symbols_table:
                                                    if func['token'] == 'func' and func['name'] == node_chamada_funcao.children[0].name:
                                                        for var in symbols_table:
                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[0].children[0].name:
                                                                var1 = builder.load(var['code'])

                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[2].children[0].name:
                                                                var2 = builder.load(var['code'])

                                                        atrib_call = builder.call(func['code'], [var1, var2])

                                                        for var in symbols_table:
                                                            if var['name'] == node_atribuicao.children[0].children[0]:
                                                                symbol_code = var['code']

                                                        builder.store(atrib_call, symbol_code)


                            # sobe 1 corpo da funcao
                            function_body = function_body.parent



                        ############################################
                        # checa o retorno da funcao
                        ############################################
                        for function_return_node in LevelOrderIter(node):
                            if function_return_node.name == 'retorna' and function_return_node.children:
                                # checa os tipos de retorno (var, numero ou soma/subtracao)
                                if function_return_node.children[2].name == 'ID': # se retorna var
                                    print('funcao => retorno => var')

                                    for func_in_table in symbols_table:
                                        if func_in_table['name'] == function_return_node.children[2].children[0].name:
                                            if 'code' in func_in_table:
                                                function_return = func_in_table['name']

                                            else:
                                                function_return = 0

                                if function_return_node.children[2].name == 'NUM_INTEIRO':
                                    print('funcao => retorno => inteiro')
                                    function_return = function_return_node.children[2].children[0].name

                                if function_return_node.children[2].name == 'expressao_aditiva':
                                    if function_return_node.children[2].children[1].children[0].name == '+':
                                        print('funcao => retorno => expressao aditiva => soma')
                                        return1 = builder.alloca(ir.IntType(32), name=function_return_node.children[2].children[0].children[0].name)
                                        return2 = builder.alloca(ir.IntType(32), name=function_return_node.children[2].children[2].children[0].name)
                                        return1_load = builder.load(return1)
                                        return2_load = builder.load(return2)
                                        function_return = builder.add(return1_load, return2_load, name='add')

                                    if function_return_node.children[2].children[1].children[0].name == '-':
                                        print('funcao => retorno => expressao aditiva => subtracao')
                                        return1 = builder.alloca(ir.IntType(32), name=function_return_node.children[2].children[0].children[0].name)
                                        return2 = builder.alloca(ir.IntType(32), name=function_return_node.children[2].children[2].children[0].name)
                                        return1_load = builder.load(return1)
                                        return2_load = builder.load(return2)
                                        function_return = builder.sub(return1_load, return2_load, name='add')


            exit_block = function.append_basic_block('exit')
            builder.branch(exit_block)
            builder = ir.IRBuilder(exit_block)

            # build retorno de funcoes
            find_func_return = False
            for func_return in symbols_table:
                if func_return['name'] == function_return and func_return['token'] == 'ID' and func_return['type'] == 'inteiro':
                    var_returned = builder.load(func_return['code'], name='func_return', align=4)
                    builder.ret(var_returned)
                    find_func_return = True

            if find_func_return == False:
                if len(function.args) != 0:
                    res = builder.add(function.args[0], function.args[1], name='func_{}_return'.format(function.name))
                    builder.ret(res)

                else:
                    builder.ret(ir.Constant(ir.IntType(32), function_return))

    file = open('geracao-codigo-testes/gencode-{}.ll'.format(test_number), 'w')
    file.write(str(module))
    file.close()
    # print(module)
    print()
    print()
    print('----------------------------')
    print('Código intermediário gerado!')
    print('----------------------------')

```

##### Funções

#### Funções auxiliares

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
