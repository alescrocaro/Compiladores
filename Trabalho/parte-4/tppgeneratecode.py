from llvmlite import ir 
from utils import *  
from llvmlite import binding as llvm 
from anytree import LevelOrderIter



#####################################
# aloca variaveis globais
#####################################
def init_global_vars(symbolsTable, module):
    for var in symbolsTable:
        if(var['token'] == 'ID'):
            if(var['scope'] == 'global'):
                if var['type'] == 'inteiro':
                    var['code'] = ir.GlobalVariable(module, ir.IntType(32), var['name'])
                    var['code'].initializer = ir.Constant(ir.IntType(32), 0)

                if var['type'] == 'flutuante':
                    var['code'] = ir.GlobalVariable(module, ir.FloatType(), var['name'])
                    var['code'].initializer = ir.Constant(ir.FloatType(), 0.0)

                var['code'].linkage = "common"
                var['code'].align = 4




###################################################
# aloca variaveis locais (que estao em funcoes)
###################################################
def alloca_local_vars(symbolsTable, builder, function_name):
    for var in symbolsTable:
        if var['token'] == 'ID' and var['scope'] == function_name:
            if(var['type'] == 'inteiro'):
                var['code'] = builder.alloca(ir.IntType(32), name=var['name'])

            if(var['type'] == 'flutuante'):
                var['code'] = builder.alloca(ir.FloatType(), name=var['name'])

            var['code'].align = 4





###################################################
# gera codigo intermediario com llvm
###################################################
def generate_i_code(root, symbolsTable):
    # inicia llvm e modulo
    llvm.initialize()
    llvm.initialize_all_targets()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    module = ir.Module()
    module.triple = llvm.get_default_triple()
    target = llvm.Target.from_triple(module.triple)
    target_machine = target.create_target_machine()
    module.data_layout = target_machine.target_data
        
    read_integer = ir.Function(module, ir.FunctionType(ir.IntType(32), []), name="leiaInteiro")
    read_float = ir.Function(module, ir.FunctionType(ir.FloatType(), []), name="leiaFlutuante")

    print_integer = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.IntType(32)]), 'escrevaInteiro')
    print_float = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.FloatType()]), 'escrevaFlutuante')

    
    ########################################

    init_global_vars(symbolsTable, module)

    ########################################



    ##################################
    # checa todas funcoes
    ##################################
    for function_in_table in symbolsTable:
        # verifica se o simbolo (function_in_table) eh funcao
        if(function_in_table['token'] == 'func'):

            ############################################
            # checa se funcao tem parametros
            ############################################
            if('lista-parametros' in function_in_table):
                print('funcao => lista_parametros')
                t_func_with_params = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
                function = ir.Function(module, t_func_with_params, function_in_table['name']) 
                function_in_table['code'] = function

                i = 0
                for param in function_in_table['lista-parametros']:
                    function.args[i].name = param
                    i += 1

                entry_block = function.append_basic_block('entry')  
                builder = ir.IRBuilder(entry_block) 

            else:
                if function_in_table['name'] != 'principal':
                    print('funcao => sem parametros => !=principal')
                    function = ir.Function(module, ir.FunctionType(ir.IntType(32), []), name=function_in_table['name'])  

                else:
                    print('funcao => sem parametros => principal')
                    function = ir.Function(module, ir.FunctionType(ir.IntType(32), []), name='main') 

                function_in_table['code'] = function 

                entry_block = function.append_basic_block('entry')  
                builder = ir.IRBuilder(entry_block)



            ################################################################################

            alloca_local_vars(symbolsTable, builder, function_in_table['name'])

            ################################################################################



            ####################################################
            # checa arvore noh a noh em busca das funcoes
            ####################################################
            for node in LevelOrderIter(root): 
                # se o noh se refere a uma declaracao de funcao
                if node.name == 'cabecalho':
                    # encontrar na arvore a funcao correspondente na tabela
                    if node.children[0].children[0].name == function_in_table['name']:
                        # obtem o retorno da funcao
                        for function_return_node in LevelOrderIter(node): 

                            ############################################
                            # checa o retorno da funcao 
                            ############################################      
                            if function_return_node.name == 'retorna' and function_return_node.children:
                                # checa os tipos de retorno (var, numero ou soma/subtracao)
                                if function_return_node.children[2].name == 'ID': # se retorna var
                                    print('funcao => retorno => var')

                                    # da pra trocar isso simplesmente por function_return = function_return_node.children[2].children[0].name ??????
                                    for func_in_table in symbolsTable: 
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




                        ############################################
                        # checa o corpo da funcao
                        ############################################

                        # (corpo eh como uma linha no codigo)
                        function_body = node.children[4]
                        # vai ate o ultimo corpo da funcao e depois volta pra cima
                        while len(function_body.children) != 0: 
                            function_body = function_body.children[0] 
                        
                        # aqui nao se verifica o noh declaracao_variaveis pois isso ja eh feito na funcao alloca_local_vars

                        while function_body.parent.name != 'cabecalho': 
                            if function_body.name == 'corpo':
                                if function_body.children:
                                    if len(function_body.children) > 1:

                                        ###############################
                                        # se corpo atual eh repita
                                        ###############################
                                        if function_body.children[1].name == 'repita':
                                            print('funcao => corpo => repita')
                                            node_repita = function_body.children[1]
                                            repeat_start = function.append_basic_block('repeat_start')
                                            repeat_end = function.append_basic_block('repeat_end')

                                            builder.branch(repeat_start)
                                            builder.position_at_end(repeat_start)

                                            for current_node in LevelOrderIter(node_repita):
                                                # leia dentro do repita
                                                if current_node.name == 'leia' and len(current_node.children) > 1:
                                                    print('funcao => corpo => repita => leia')
                                                    for var in symbolsTable: 
                                                        if var['name'] == current_node.children[2].children[0].name:
                                                            builder.store(builder.call(read_integer, []), var['code'])

                                                # escreva dentro do repita
                                                if current_node.name == 'escreva' and len(current_node.children) > 1: 
                                                    print('funcao => corpo => repita => escreva')
                                                    for var in symbolsTable:
                                                        if var['name'] == current_node.children[2].children[0].name:
                                                            var_code_on_write = var['code']


                                                # atribuicao dentro do repita
                                                if current_node.name == 'atribuicao':
                                                    print('funcao => corpo => repita => atribuicao')

                                                    # se var recebe uma soma que a primeira parcela eh ela mesma e a segunda parcela eh um numero (INCREMENTO, como i++)
                                                    if current_node.children[2].name == 'expressao_aditiva' and current_node.children[2].children[2].name != 'ID' and current_node.children[2].children[1].children[0].name == '+':
                                                        if current_node.children[0].children[0].name == current_node.children[2].children[0].children[0].name:
                                                            print('funcao => corpo => repita => atribuicao => incremento')
                                                            
                                                            for symbol in symbolsTable: 
                                                                if symbol['name'] == current_node.children[0].children[0].name:
                                                                    # numero da segunda parcela da soma
                                                                    part2_number = current_node.children[2].children[2].children[0].name
                                                                    part2_number_allocated = builder.alloca(ir.IntType(32), name=part2_number)
                                                                    part2_number_loaded = builder.load(part2_number_allocated)

                                                                    part1_var_loaded = builder.load(symbol['code'])
                                                                    builder.add(part1_var_loaded, part2_number_loaded, name='increment', flags=())
                                                                    builder.call(print_integer, [builder.load(symbol['code'])])  


                                                    # se var recebe uma subtracao que a primeira parcela eh ela mesma e que a segunda parcela eh um numero (DECREMENTO, como i--)
                                                    if current_node.children[2].name == 'expressao_aditiva' and current_node.children[2].children[2].name != 'ID' and current_node.children[2].children[1].children[0].name == '-':
                                                        if current_node.children[0].children[0].name == current_node.children[2].children[0].children[0].name:
                                                            print('funcao => corpo => repita => atribuicao => decremento')

                                                            for symbol in symbolsTable:
                                                                if symbol['name'] == current_node.children[0].children[0].name:
                                                                    # numero da segunda parcela da subtracao
                                                                    part2_number = current_node.children[2].children[2].children[0].name
                                                                    part2_number_allocated = builder.alloca(ir.IntType(32), name=part2_number)
                                                                    part2_number_loaded = builder.load(part2_number_allocated)

                                                                    part1_var_loaded = builder.load(symbol['code'])
                                                                    builder.sub(part1_var_loaded, part2_number_loaded, name='decrement', flags=())


                                                    # se funcao que esta sendo atribuida recebe lista de argumentos 
                                                    if current_node.children[2].name == 'chamada_funcao' and current_node.children[2].children[2].name == 'lista_argumentos':
                                                        # funcao recebe parametros normais (como vars)
                                                        print('funcao => corpo => repita => atribuicao => chamada_funcao => lista_argumentos')

                                                        node_chamada_funcao = current_node.children[2]

                                                        for var in symbolsTable:
                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[0].children[0].name:
                                                                var1_code = var['code']

                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[2].children[0].name:
                                                                var2_code = var['code']

                                                        for func in symbolsTable:
                                                            if func['token'] == 'func' and func['name'] == node_chamada_funcao.children[0].name: 
                                                                func_code = builder.call(func['code'], [builder.load(var1_code), builder.load(var2_code)])
                                                                for var_receiving_atrib in symbolsTable: 
                                                                    if var_receiving_atrib['name'] == current_node.children[0].children[0].name:
                                                                        builder.store(func_code, var_receiving_atrib['code']) 
                                                                        builder.call(print_integer,[builder.load(var_code_on_write)])   


                                                    # var recebe uma soma/sub de variaveis
                                                    if current_node.children[2].name == 'expressao_aditiva':
                                                        print('funcao => corpo => repita => atribuicao => expressao aditiva')
                                                        # parcela 1 da soma/sub eh variavel
                                                        if current_node.children[2].children[0].name == 'ID':
                                                            for var in symbolsTable:
                                                                if var['name'] == current_node.children[2].children[0].children[0].name:
                                                                    var1_loaded = builder.load(var['code'])

                                                        # parcela 1 da soma/sub eh numero
                                                        elif current_node.children[2].children[0].name == 'NUM_INTEIRO' or current_node.children[2].children[0].name == 'NUM_FLUTUANTE':
                                                            var1_loaded = ir.Constant(ir.IntType(32), current_node.children[2].children[0].children[0].name)

                                                        # parcela 2 da soma/sub eh variavel
                                                        if current_node.children[2].children[2].name == 'ID':
                                                            for var in symbolsTable:
                                                                if var['name'] == current_node.children[2].children[2].children[0].name:
                                                                    var2_loaded = builder.load(var['code'])

                                                        # parcela 2 da soma/sub eh numero
                                                        elif current_node.children[2].children[2].name == 'NUM_INTEIRO' or current_node.children[2].children[2].name == 'NUM_FLUTUANTE':
                                                            var2_loaded = ir.Constant(ir.IntType(32), current_node.children[2].children[2].children[0].name)
                     
                                                        for symbol in symbolsTable: 
                                                            if symbol['name'] == current_node.children[0].children[0].name: 
                                                                store = symbol['code'] 
                                            
                                                        result = builder.add(var1_loaded , var2_loaded , name='atrib_expression_result', flags=())
                                                        builder.store(result, store)


                                            # expressao do 'ate'/'until'
                                            if node_repita.children[3].name == 'expressao_simples': 
                                                print('funcao => corpo => repita => expressao simples (ate)')
                                                node_repita_expressao_simples = node_repita.children[3]
                                                for var in symbolsTable: 
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

                                            for symbol in symbolsTable: 
                                                if symbol['type'] == 'inteiro' and symbol['name'] == node_leia.children[2].children[0].name:
                                                    print('funcao => corpo => leia => inteiro')
                                                    builder.store(builder.call(read_integer, ()), symbol['code'])  

                                                if symbol['type'] == 'flutuante' and symbol['name'] == node_leia.children[2].children[0].name:
                                                    print('funcao => corpo => leia => flutuante')
                                                    builder.store(builder.call(read_float, ()), symbol['code'])  


                                        ###############################
                                        # se corpo atual eh escreva
                                        ###############################
                                        if function_body.children[1].name == 'escreva':
                                            print('funcao => corpo => escreva')

                                            for var in symbolsTable: 
                                                if var['name'] == function_body.children[1].children[2].children[0].name:
                                                    if var['type'] == 'inteiro':
                                                        builder.call(print_integer, args=[builder.load(var['code'])])  

                                                    if var['type'] == 'flutuante':
                                                        builder.call(print_float, args=[builder.load(var['code'])])


                                        ##############################################################
                                        # se corpo atual eh atribuicao que nao recebe funcao                                       
                                        ##############################################################
                                        if function_body.children[1].name == 'atribuicao' and function_body.children[1].children[2].name != 'chamada_funcao':
                                            node_atribuicao = function_body.children[1]

                                            # obtem infos da variavel recebendo a atribuicao na tabela de simbolos
                                            for var in symbolsTable: 
                                                if var['token'] == 'ID':
                                                    if var['name'] == node_atribuicao.children[0].children[0].name:
                                                        if 'code' in var:
                                                            var_code = var['code']  
                                                            var_type = var['type']  

                                            # var recebe numero
                                            if node_atribuicao.children[2].name != 'ID':
                                                print('funcao => atribuicao => numero')
                                                number = node_atribuicao.children[2].children[0].name
                                                if(var_type == 'inteiro' and node_atribuicao.children[2].name == 'NUM_INTEIRO'):
                                                    builder.store(ir.Constant(ir.IntType(32), number), var_code)         

                                            if node_atribuicao.children[2].name == 'ID':
                                                print('funcao => atribuicao => var')
                                                for var in symbolsTable: 
                                                    if var['name'] == node_atribuicao.children[2].children[0]:
                                                        builder.store(builder.load(var['code']), var_code)
                                       
                                       
                                        ##############################################################
                                        # se corpo atual eh atribuicao que recebe funcao                                        
                                        ##############################################################
                                        if function_body.children[1].name == 'atribuicao' and function_body.children[1].children[2].name == 'chamada_funcao':
                                            print('funcao => corpo => atribuicao (var := func)')
                                            node_atribuicao = function_body.children[1]

                                            if node_atribuicao.children[2].children[2].name == 'lista_argumentos':
                                                print('funcao => corpo => atribuicao (var := func) => lista argumentos')
                                                node_chamada_funcao = node_atribuicao.children[2]

                                                for func in symbolsTable:
                                                    if func['token'] == 'func' and func['name'] == node_chamada_funcao.children[0].name:
                                                        for var in symbolsTable:
                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[0].children[0].name:
                                                                var1 = builder.load(var['code'])

                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[2].children[0].name:
                                                                var2 = builder.load(var['code'])

                                                        atrib_call = builder.call(func['code'], [var1, var2])

                                                        for var in symbolsTable:
                                                            if var['name'] == node_atribuicao.children[0].children[0]:
                                                                symbol_code = var['code']

                                                        builder.store(atrib_call, symbol_code)


                            # sobe 1 corpo da funcao
                            function_body = function_body.parent



            exitBasicBlock = function.append_basic_block('exit')
            builder.branch(exitBasicBlock)
            builder = ir.IRBuilder(exitBasicBlock)

            # build retorno de funcoes
            find_func_return = False
            for func_return in symbolsTable:
                if func_return['name'] == function_return and func_return['token'] == 'ID' and func_return['type'] == 'inteiro':
                    var_returned = builder.load(func_return['code'], name='func_return', align=4)
                    builder.ret(var_returned)
                    find_func_return = True

            if find_func_return == False:
                if len(function.args) != 0:
                    res = builder.add(function.args[0], function.args[1])
                    builder.ret(res)

                else:
                    builder.ret(ir.Constant(ir.IntType(32), function_return))


    file = open('generated_code.ll', 'w')
    file.write(str(module))
    file.close()
    print()
    print('Código intermediário gerado!')