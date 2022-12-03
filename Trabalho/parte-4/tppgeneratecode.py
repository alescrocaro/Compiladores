from llvmlite import ir, binding as llvm 
from anytree import LevelOrderIter
from utils import *  





#####################################
# aloca variaveis globais
#####################################
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





###################################################
# aloca variaveis locais (que estao em funcoes)
###################################################
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





###################################################
# gera codigo intermediario com llvm
###################################################
def generate_i_code(root, symbols_table, test_file):
    # inicia llvm e modulo
    llvm.initialize()
    llvm.initialize_all_targets()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    module = ir.Module('test.bc')
    module.triple = llvm.get_process_triple()
    target = llvm.Target.from_triple(module.triple)
    target_machine = target.create_target_machine()
    module.data_layout = target_machine.target_data
        
    read_integer = ir.Function(module, ir.FunctionType(ir.IntType(32), []), name="leiaInteiro")
    read_float = ir.Function(module, ir.FunctionType(ir.FloatType(), []), name="leiaFlutuante")

    print_integer = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.IntType(32)]), 'escrevaInteiro')
    print_float = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.FloatType()]), 'escrevaFlutuante')

    

    ########################################

    init_global_vars(symbols_table, module)

    ########################################



    ##################################
    # checa todas funcoes
    ##################################
    for function_in_table in symbols_table:
        # verifica se o simbolo (function_in_table) eh funcao
        if function_in_table['token'] == 'func':


            ################################################
            # checa se funcao tem parametros e os aloca
            ################################################
            if 'params_list' in function_in_table:
                print('funcao => lista parametros')
                t_func_with_params = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
                function = ir.Function(module, t_func_with_params, function_in_table['name']) 
                function_in_table['code'] = function

                i = 0
                for param in function_in_table['params_list']:
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

            alloca_local_vars(symbols_table, builder, function_in_table['name'])

            ################################################################################



            ####################################################
            # checa arvore noh a noh em busca das funcoes
            ####################################################
            for node in LevelOrderIter(root): 
                # se o noh se refere a uma declaracao de funcao
                if node.name == 'cabecalho':
                    # encontrar na arvore a funcao correspondente na tabela
                    if node.children[0].children[0].name == function_in_table['name']:

                        ############################################
                        # checa o corpo da funcao
                        ############################################
                        function_body = node.children[4]
                        # desce a arvore ate o ultimo corpo da funcao
                        while len(function_body.children) != 0: 
                            function_body = function_body.children[0] 
                        
                        # aqui nao se verifica o noh declaracao_variaveis pois isso ja eh feito na funcao alloca_local_vars
                        # sobe a arvore de volta percorrendo o corpo da funcao 
                        while function_body.parent.name != 'cabecalho': 
                            if function_body.name == 'corpo':
                                if function_body.children:
                                    if len(function_body.children) > 1:

                                        ###############################
                                        # se corpo atual eh repita
                                        ###############################
                                        if function_body.children[1].name == 'repita':
                                            print('funcao => corpo => repita')
                                            repeat_start = function.append_basic_block('repeat_start')
                                            repeat_end = function.append_basic_block('repeat_end')

                                            builder.branch(repeat_start)
                                            builder.position_at_end(repeat_start)


                                            node_repita = function_body.children[1]
                                            node_repita_body = function_body.children[1].children[1]
                                            # desce a arvore ate o ultimo corpo do repita
                                            while node_repita_body.children[0].children[0].name != 'vazio': 
                                                node_repita_body = node_repita_body.children[0]

                                            while len(node_repita_body.children) <= 2:

                                                # print('corpo atual no REPITA: ', current_node.children[1].name)
                                                # leia dentro do repita
                                                if node_repita_body.children[1].name == 'leia':
                                                    print('funcao => corpo => repita => leia')
                                                    node_leia = node_repita_body.children[1]
                                                    for var in symbols_table: 
                                                        if var['name'] == node_leia.children[2].children[0].name:
                                                            builder.store(builder.call(read_integer, []), var['code'])

                                                # escreva dentro do repita
                                                if node_repita_body.children[1].name == 'escreva': 
                                                    print('funcao => corpo => repita => escreva')
                                                    node_escreva = node_repita_body.children[1]
                                                    for var in symbols_table:
                                                        if var['name'] == node_escreva.children[2].children[0].name:
                                                            var_code_on_write = var['code']

                                                # atribuicao dentro do repita
                                                if node_repita_body.children[1].name == 'atribuicao':
                                                    node_atribuicao = node_repita_body.children[1]
                                                    node_received_in_atrib = node_repita_body.children[1].children[2]
                                                                          
                                                    # se var recebe uma soma que a 
                                                    if node_received_in_atrib.name == 'expressao_aditiva' and node_received_in_atrib.children[2].name != 'ID':

                                                        # se var recebe uma soma que a primeira parcela eh ela mesma e que a segunda parcela eh um numero (DECREMENTO, como i--)
                                                        if node_received_in_atrib.children[1].children[0].name == '+':
                                                            if node_atribuicao.children[0].children[0].name == node_received_in_atrib.children[0].children[0].name:
                                                                print('funcao => corpo => repita => atribuicao => incremento')
                                                                
                                                                for symbol in symbols_table: 
                                                                    if symbol['name'] == node_atribuicao.children[0].children[0].name:
                                                                        # numero da segunda parcela da soma
                                                                        part2_number = node_received_in_atrib.children[2].children[0].name
                                                                        part2_number_allocated = builder.alloca(ir.IntType(32), name=part2_number)
                                                                        part2_number_loaded = builder.load(part2_number_allocated)

                                                                        part1_var_loaded = builder.load(symbol['code'])
                                                                        builder.add(part1_var_loaded, part2_number_loaded, name='increment')
                                                                        builder.call(print_integer, [builder.load(symbol['code'])])  


                                                        # se var recebe uma subtracao que a primeira parcela eh ela mesma e que a segunda parcela eh um numero (DECREMENTO, como i--)
                                                        if node_received_in_atrib.children[1].children[0].name == '-':
                                                            if node_atribuicao.children[0].children[0].name == node_received_in_atrib.children[0].children[0].name:
                                                                print('funcao => corpo => repita => atribuicao => decremento')

                                                                for symbol in symbols_table:
                                                                    if symbol['name'] == node_atribuicao.children[0].children[0].name:
                                                                        # numero da segunda parcela da subtracao
                                                                        part2_number = node_received_in_atrib.children[2].children[0].name
                                                                        part2_number_allocated = builder.alloca(ir.IntType(32), name=part2_number)
                                                                        part2_number_loaded = builder.load(part2_number_allocated)

                                                                        part1_var_loaded = builder.load(symbol['code'])
                                                                        builder.sub(part1_var_loaded, part2_number_loaded, name='decrement', flags=())


                                                    # se funcao que esta sendo atribuida recebe lista de argumentos 
                                                    if node_received_in_atrib.name == 'chamada_funcao' and node_received_in_atrib.children[2].name == 'lista_argumentos':
                                                        # funcao recebe parametros normais (como vars)
                                                        print('funcao => corpo => repita => atribuicao => chamada_funcao => lista_argumentos')

                                                        node_chamada_funcao = node_atribuicao.children[2]

                                                        for var in symbols_table:
                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[0].children[0].name:
                                                                var1_code = var['code']

                                                            if var['token'] == 'ID' and var['name'] == node_chamada_funcao.children[2].children[2].children[0].name:
                                                                var2_code = var['code']

                                                        for func in symbols_table:
                                                            if func['token'] == 'func' and func['name'] == node_chamada_funcao.children[0].name: 
                                                                func_code = builder.call(func['code'], [builder.load(var1_code), builder.load(var2_code)])
                                                                for var_receiving_atrib in symbols_table: 
                                                                    if var_receiving_atrib['name'] == node_atribuicao.children[0].children[0].name:
                                                                        builder.store(func_code, var_receiving_atrib['code']) 
                                                                        builder.call(print_integer,[builder.load(var_code_on_write)])   




                                                node_repita_body = node_repita_body.parent 

                                            





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

                                                        # parcela 1 da soma/sub eh numero
                                                        elif node_atribuicao.children[2].children[0].name == 'NUM_INTEIRO' or node_atribuicao.children[2].children[0].name == 'NUM_FLUTUANTE':
                                                            print('funcao => corpo => atribuicao => expressao aditivaa => parc1 => num')
                                                            var1_loaded = ir.Constant(ir.IntType(32), node_atribuicao.children[2].children[0].children[0].name)

                                                        # parcela 2 da soma/sub eh variavel
                                                        if node_atribuicao.children[2].children[2].name == 'ID':
                                                            print('funcao => corpo => atribuicao => expressao aditivaa => parc2 => ID')
                                                            for var in symbols_table:
                                                                if var['name'] == node_atribuicao.children[2].children[2].children[0].name:
                                                                    var2_loaded = builder.load(var['code'])

                                                        # parcela 2 da soma/sub eh numero
                                                        elif node_atribuicao.children[2].children[2].name == 'NUM_INTEIRO' or node_atribuicao.children[2].children[2].name == 'NUM_FLUTUANTE':
                                                            print('funcao => corpo => atribuicao => expressao aditiva => parc2 => num')
                                                            var2_loaded = ir.Constant(ir.IntType(32), node_atribuicao.children[2].children[2].children[0].name)
                     
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

                                                if node_atribuicao.children[2].children[2].name == 'lista_argumentos':
                                                    print('funcao => corpo => atribuicao (var := func) => lista argumentos')
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


            exitBasicBlock = function.append_basic_block('exit')
            builder.branch(exitBasicBlock)
            builder = ir.IRBuilder(exitBasicBlock)

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

    test_number = test_file.split('-')[-1]
    file = open('geracao-codigo-testes/gencode-{}.ll'.format(test_number), 'w')
    file.write(str(module))
    file.close()
    print()
    print()
    print('----------------------------')
    print('Código intermediário gerado!')
    print('----------------------------')