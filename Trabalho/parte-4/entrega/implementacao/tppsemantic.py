from anytree import LevelOrderIter, PreOrderIter
from anytree.exporter import UniqueDotExporter
from sys import argv, exit
from tppparser import root
from utils import *
from tppgeneratecode import *




##################################################################################
##################################################################################
############################ cria tabela de simbolos #############################
##################################################################################
##################################################################################
def create_symbols_table(root):
    counter = 0
    vars = []
    # Itera a arvore usando estrategia pre-order
    # Comeca na raiz ate chegar numa folha, entao volta e procura pela próxima folha
    for node_i in PreOrderIter(root):
        node_name = node_i.name


        # DECLARACAO DE VARIAVEIS COM SOMENTE 1 VAR #
        if node_name == 'declaracao_variaveis' and len(node_i.children[2].children) == 1: 
            # verifica se tem indice (eh array/matriz)
            if len(node_i.children[2].children[0].children) == 2:
                if node_i.children[2].children[0].children[1].name == 'indice':
                    # percorre a subarvore do indice
                    for n in PreOrderIter(node_i.children[2].children[0].children[1]):
                        if n.name == 'numero':
                            if n.children[0].name == 'NUM_PONTO_FLUTUANTE':
                                print("Erro: atribuição de array '{}' com indice nao inteiro".format(node_i.children[2].children[0].children[0].children[0].name))
                            else:
                                indexSingleVar = n.children[0].children[0].name
            else:
                indexSingleVar = 0

            if len(node_i.children[2].children[0].children) == 2:
                # eh matriz
                if len(node_i.children[2].children[0].children[1].children) == 4:
                    dimensionSingleVar = 2

                # eh array
                else:
                    dimensionSingleVar = 1

            else:
                dimensionSingleVar = 0

            # atribui infos da var
            typeSingleVar = node_i.children[0].children[0].children[0].name
            tokenSingleVar =  node_i.children[2].children[0].children[0].name
            nameSingleVar =  node_i.children[2].children[0].children[0].children[0].name
            variable = {}
            counter += 1
            variable['reference'] = counter
            variable['type'] = typeSingleVar
            variable['name'] = nameSingleVar
            variable['dimension'] = dimensionSingleVar
            variable['index'] = indexSingleVar
            variable['token'] = tokenSingleVar
            variable['state'] = 'declarada'

            variable['scope'] = find_scope(node_i)


            # procura pela variavel na tabela de vars, se nao existir, adiciona; senao devolve erro
            exists = 0
            for var in vars:
                if var['name'] == variable['name'] and var['scope'] == variable['scope']:
                    exists = 1

            if exists == 0:
                vars.append(variable)

            else:
                print("Aviso: Variavel '{}' ja declarada anteriormente".format(variable['name']))



        # DECLARACAO DE VARIAVEIS COM DUAS VARS #    
        # len(node_i.children[2].children) == 3 ----> noh lista_variaveis possui mais de 1 var
        if node_name == 'declaracao_variaveis' and len(node_i.children[2].children) == 3: 
            # PRIMEIRA VAR
            if node_i.children[2].children[0].children[0].name == 'var':

                # verifica se tem indice (eh array/matriz)
                if len(node_i.children[2].children[0].children[0].children) == 2:
                    if node_i.children[2].children[0].children[0].children[1].name == 'indice':
                        # percorre a subarvore do indice
                        for n in PreOrderIter(node_i.children[2].children[0].children[0].children[1]):
                            if n.name == 'numero':
                                if n.children[0].name == 'NUM_PONTO_FLUTUANTE':
                                    print("Erro: atribuição de array '{}' com indice nao inteiro".format(node_i.children[2].children[0].children[0].children[0].name))
                                else:
                                    indexFirstVar = n.children[0].children[0].name
                else:
                    indexFirstVar = 0

                if len(node_i.children[2].children[0].children[0].children) == 2:
                    # eh matriz
                    if len(node_i.children[2].children[0].children[0].children[1].children) == 4:
                        dimensionFirstVar = 2

                    # eh array
                    else:
                        dimensionFirstVar = 1

                else:
                    dimensionFirstVar = 0


                name = node_i.children[2].children[0].children[0].children[0].children[0].name
                type =  node_i.children[0].children[0].children[0].name
                token =  node_i.children[2].children[0].children[0].children[0].name
                state = 'declarada'

                counter += 1
                variable = {}
                variable['reference'] = counter
                variable['type'] = type
                variable['name'] = name
                variable['dimension'] = dimensionFirstVar
                variable['index'] = indexFirstVar
                variable['token'] = token
                variable['state'] = state

                variable['scope'] = find_scope(node_i)


                exists = 0
                for var in vars:
                    if var['name'] == name:
                        exists = 1

                if exists == 0:
                    vars.append(variable)

            # SEGUNDA VAR
            if node_i.children[2].children[2].name == 'var': 
                name = node_i.children[2].children[2].children[0].children[0].name
                type =  node_i.children[0].children[0].children[0].name
                token =  node_i.children[2].children[2].children[0].name
                state = 'declarada'

                dimension = 0
                index = 0
                counter += 1
                variable = {}
                variable['reference'] = counter
                variable['type'] = type
                variable['name'] = name
                variable['dimension'] = dimension
                variable['index'] = index
                variable['token'] = token
                variable['state'] = state

                variable['scope'] = find_scope(node_i)


                exists = 0
                for var in vars:
                    if var['name'] == name:
                        exists = 1

                if exists == 0:
                    vars.append(variable)


        # DECLARACAO DE VARIAVEIS COM MAIS DE DUAS VARS # 
        # len(node_i.children[2].children[0].children) == 3 ----> noh lista_variaveis possui um filho que tambem eh lista_variaveis
        if node_name == 'declaracao_variaveis' and len(node_i.children[2].children[0].children) == 3:
            # atualiza o noh para percorrer toda a declaracao
            current_node = node_i.children[2].children[0]

            # percorre toda a subarvore de lista_variaveis
            while len(current_node.children) > 1:
                name = current_node.children[2].children[0].children[0].name
                type = node_i.children[0].children[0].children[0].name
                token = node_i.children[2].children[2].children[0].name
                state = 'declarada'

                dimension = 0
                index1 = 0
                counter += 1
                variable = {}
                variable['reference'] = counter
                variable['type'] = type
                variable['name'] = name
                variable['dimension'] = dimension
                variable['index'] = index1
                variable['token'] = token
                variable['state'] = state

                variable['scope'] = find_scope(node_i) 


                exists = 0
                for var in vars:
                    if var['name'] == variable['name']:
                        exists = 1

                if exists == 0:
                    vars.append(variable)

                # noh atual atualiza para a proxima lista_variaveis
                current_node = current_node.children[0]

            # ultima subarvore do primeiro 'current_node'
            name_n = current_node.children[0].children[0].children[0].name
            type_n = node_i.children[0].children[0].children[0].name
            token_n = current_node.children[0].children[0].name
            state_n = 'declarada'

            dimension_n = 0
            index_n = 0
            counter += 1
            variable = {}
            variable['reference'] = counter
            variable['type'] = type_n
            variable['name'] = name_n
            variable['dimension'] = dimension_n
            variable['index'] = index_n
            variable['token'] = token_n
            variable['state'] = state_n

            variable['scope'] = find_scope(node_i)


            exists = 0
            for var in vars:
                if var['name'] == name_n:
                    exists = 1

            if exists == 0:
                vars.append(variable)

            
            # segunda var, que estava no mesmo nivel que o primeiro current_node (volta la pra cima da subarvore) 
            name = node_i.children[2].children[2].children[0].children[0].name
            type = node_i.children[0].children[0].children[0].name
            token = node_i.children[2].children[2].children[0].name
            state = 'declarada'

            dimension = 0
            index = 0
            counter += 1
            variable = {}
            variable['reference'] = counter
            variable['type'] = type
            variable['name'] = name
            variable['dimension'] = dimension
            variable['index'] = index
            variable['token'] = token
            variable['state'] = state

            variable['scope'] = find_scope(node_i)


            exists = 0
            for var in vars:
                if var['name'] == variable['name']:
                    exists = 1

            if exists == 0:
                vars.append(variable)



        # DECLARACAO_FUNCAO
        if node_name == 'declaracao_funcao':
            counter += 1
            func = {}
            func['reference'] = counter
            func['token'] = 'func'
            func['state'] = 'declarada'

            # se funcao tem tipo: diferente de vazio
            if len(node_i.children) == 2:
                func['type'] = node_i.children[0].children[0].children[0].name
                func['name'] = node_i.children[1].children[0].children[0].name
                func['state'] = 'declarada'

                # define o retorno da funcao
                for node2 in PreOrderIter(node_i):
                    if node2.name == 'retorna':
                        for node3 in PreOrderIter(node2):
                            # define retorno como nome da var retornada
                            if node3.name == 'var':
                                func['retorno'] = node3.children[0].children[0].name

                            # define retorno como inteiro ou flutuante
                            elif node3.name == 'numero':
                                if node3.children[0].name == 'NUM_INTEIRO':
                                    func['retorno'] = 'inteiro'
                                if node3.children[0].name == 'NUM_PONTO_FLUTUANTE':
                                    func['retorno'] = 'flutuante'
                                    

                # nao tem parametros
                if node_i.children[1].children[2].children[0].name == 'vazio':
                    func['formal-params'] = 0

                # tem 1 parametro
                elif node_i.children[1].children[2].children[0].name == 'parametro':
                    func['params_list'] =  node_i.children[1].children[2].children[0].children[2].children[0].name
                    func['formal-params'] = 1
                    # add param a lista de vars
                    param = {}
                    counter += 1
                    param['reference'] = counter
                    param['type'] = node_i.children[1].children[2].children[0].children[0].children[0].children[0].name
                    param['name'] = node_i.children[1].children[2].children[0].children[2].children[0].name
                    param['dimension'] = 0
                    param['index'] = 0
                    param['token'] = 'ID'
                    param['state'] = 'utilizada'
                    param['scope'] = node_i.children[1].children[0].children[0].name
                    vars.append(param)

                # tem mais de 1 parametro
                else:
                    cont = 1
                    # aux = node do lista parametros
                    aux = node_i.children[1].children[2]
                    func['params_list'] = []
                    func['params_list'].append(aux.children[2].children[2].children[0].name)
                    # add primeiro param a lista de vars
                    param = {}
                    counter += 1
                    param['reference'] = counter
                    param['type'] = aux.children[2].children[0].children[0].children[0].name
                    param['name'] = aux.children[2].children[2].children[0].name
                    param['dimension'] = 0
                    param['index'] = 0
                    param['token'] = 'ID'
                    param['state'] = 'utilizada'
                    param['scope'] = node_i.children[1].children[0].children[0].name
                    vars.append(param)
                    
                    # lida com o resto dos parametros
                    while(aux.children[0].name == 'lista_parametros'):
                        # recebe prox param
                        aux = aux.children[0]

                        # ultimo parametro
                        if len(aux.children) == 1:
                            func['params_list'].append(aux.children[0].children[2].children[0].name)
                            # add param a lista de vars
                            param = {}
                            counter += 1
                            param['reference'] = counter
                            param['type'] = aux.children[0].children[0].children[0].children[0].name
                            param['name'] = aux.children[0].children[2].children[0].name
                            param['dimension'] = 0
                            param['index'] = 0
                            param['token'] = 'ID'
                            param['state'] = 'utilizada'
                            param['scope'] = node_i.children[1].children[0].children[0].name
                            vars.append(param)

                        # acessado sempre q n for o ultimo nem o primeiro parametro
                        else:
                            func['params_list'].append(aux.children[2].children[2].children[0].name)
                            # add param a lista de vars
                            param = {}
                            counter += 1
                            param['reference'] = counter
                            param['type'] = aux.children[2].children[0].children[0].children[0].name
                            param['name'] = aux.children[2].children[2].children[0].name
                            param['dimension'] = 0
                            param['index'] = 0
                            param['token'] = 'ID'
                            param['state'] = 'utilizada'
                            param['scope'] = node_i.children[1].children[0].children[0].name
                            vars.append(param)

                        cont += 1
                    
                    func['formal-params'] = cont

            # se funcao eh tipo vazio
            else:
                func['type'] = 'vazio'
                func['name'] = node_i.children[0].children[0].children[0].name
                
                # n tem parametros
                if node_i.children[0].children[2].children[0].name == 'vazio':
                    func['formal-params'] = 0

                # tem 1 parametro
                elif node_i.children[0].children[2].children[0].name == 'parametro':
                    aux = node_i.children[0].children[2].children[0]
                    func['params_list'] =  aux.children[2].children[0].name
                    func['formal-params'] = 1
                    # add param a lista de vars
                    param = {}
                    counter += 1
                    param['reference'] = counter
                    param['type'] = aux.children[0].children[0].children[0].name
                    param['name'] = aux.children[2].children[0].name
                    param['dimension'] = 0
                    param['index'] = 0
                    param['token'] = 'ID'
                    param['state'] = 'utilizada'
                    param['scope'] = node_i.children[0].children[0].children[0].name
                    vars.append(param)

                # tem mais de 1 parametro
                else:
                    cont = 1
                    # aux = node do lista parametros
                    aux = node_i.children[0].children[2]
                    func['params_list'] = []
                    func['params_list'].append(aux.children[2].children[2].children[0].name)
                    # add primeiro param a lista de vars
                    param = {}
                    counter += 1
                    param['reference'] = counter
                    param['type'] = aux.children[2].children[0].children[0].children[0].name
                    param['name'] = aux.children[2].children[2].children[0].name
                    param['dimension'] = 0
                    param['index'] = 0
                    param['token'] = 'ID'
                    param['state'] = 'utilizada'
                    param['scope'] = node_i.children[0].children[0].children[0].name
                    vars.append(param)
                    
                    # lida com o resto dos parametros
                    while(aux.children[0].name == 'lista_parametros'):
                        # recebe prox param
                        aux = aux.children[0]

                        # ultimo parametro
                        if len(aux.children) == 1:
                            func['params_list'].append(aux.children[0].children[2].children[0].name)
                            # add param a lista de vars
                            param = {}
                            counter += 1
                            param['reference'] = counter
                            param['type'] = aux.children[0].children[0].children[0].children[0].name
                            param['name'] = aux.children[0].children[2].children[0].name
                            param['dimension'] = 0
                            param['index'] = 0
                            param['token'] = 'ID'
                            param['state'] = 'utilizada'
                            param['scope'] = node_i.children[0].children[0].children[0].name
                            vars.append(param)

                        # acessado sempre q n for o ultimo nem o primeiro parametro
                        else:
                            func['params_list'].append(aux.children[2].children[2].children[0].name)
                            # add param a lista de vars
                            param = {}
                            counter += 1
                            param['reference'] = counter
                            param['type'] = aux.children[2].children[0].children[0].children[0].name
                            param['name'] = aux.children[2].children[2].children[0].name
                            param['dimension'] = 0
                            param['index'] = 0
                            param['token'] = 'ID'
                            param['state'] = 'utilizada'
                            param['scope'] = node_i.children[0].children[0].children[0].name
                            vars.append(param)

                        cont += 1
                    
                    func['formal-params'] = cont

                # verifica se funcao vazia tem retorno
                for node2 in PreOrderIter(node_i):
                    if node2.name == 'retorna':
                        for node3 in PreOrderIter(node2):
                            if node3.name == 'var':
                                print("Erro: Funcao '{}' do tipo vazio retornando '{}'".format(func['name'], node3.children[0].children[0].name))
                                
                            elif node3.name == 'numero':
                                print("Erro: Funcao '{}' do tipo vazio retornando '{}'".format(func['name'], node3.children[0].children[0].name))


            vars.append(func)

    return vars





##################################################################################
##################################################################################
################ verifica se existe funcao principal no programa #################
##################################################################################
##################################################################################
def check_main(symbols_table): 
    flag = 0
    for symbol in symbols_table:
        if symbol['name'] == 'principal':
            flag = 1

    if flag == 0:
        print('Erro: Funcao principal nao declarada')





##################################################################################
##################################################################################
###################### verifica o retorno de todas funcoes #######################
##################################################################################
##################################################################################
def check_functions(root, symbols_table):
    # VERIFICA O RETORNO DAS FUNCOES
    for symbol in symbols_table:
        # se funcao eh do tipo inteiro ou flutuante
        if symbol['token'] == 'func' and (symbol['type'] == 'inteiro' or symbol['type'] == 'flutuante'):
            for symbol2 in symbols_table:
                # se funcao tiver retorno, atribui tipo da variavel ao retorno da funcao
                if 'retorno' in symbol:
                    if symbol2['name'] == symbol['retorno']:
                        symbol['retorno'] = symbol2['type']

                # senao, devolve erro
                else:
                    if symbol['name'] == 'principal':
                        print('Erro: Funcao principal deveria retornar inteiro, mas retorna vazio')
                    else:
                        print("Aviso: Funcao '{}' sem retorno".format(symbol['name']))
                    break

        if symbol['token'] == 'func':
            # se existe retorno
            if 'retorno' in symbol:
                # se retorno eh var, verifica se var existe
                if symbol['retorno'] != 'inteiro' and symbol['retorno'] != 'flutuante' and symbol['retorno'] != 'NUM_INTEIRO' and symbol['retorno'] != 'NUM_PONTO_FLUTUANTE': 
                    existsVar = False 
                    for s in symbols_table:
                        if s['name'] == symbol['retorno']:
                            print(s['name'])
                            existsVar = True

                    if not existsVar:
                        print("Erro: Variavel '{}' nao declarada".format(symbol['retorno'])) 

                # retorno nao eh var:
                # funcao eh inteiro
                elif symbol['type'] == 'inteiro':
                    if 'retorno' in symbol:
                        if symbol['retorno'] != 'inteiro' and symbol['retorno'] != 'NUM_INTEIRO':
                            print("Erro: Funcao '{}' eh do tipo {}, mas retorna um {}".format(symbol['name'], symbol['type'], symbol['retorno']))
                
                # funcao eh flutuante
                elif symbol['type'] == 'flutuante':
                    if symbol['retorno'] != 'flutuante' and symbol['retorno'] != 'NUM_PONTO_FLUTUANTE':
                        print("Erro: Funcao '{}' eh do tipo {}, mas retorna um {}".format(symbol['name'], symbol['type'], symbol['retorno']))
    
    # VERIFICA CHAMADAS DE FUNCAO
    for node in LevelOrderIter(root):
        if node.name == 'chamada_funcao':
            functionCalled = node.children[0].children[0].name
            funcExists = False
            for symbol in symbols_table:
                if functionCalled == 'principal' and symbol['name'] == 'principal':
                    aux = node
                    # verifica em qual funcao esta a chamada para a principal
                    while aux.name != 'cabecalho':
                        aux = aux.parent
                        
                    if aux.children[0].children[0].name != 'principal':
                        print("Erro: Chamada para a funcao principal nao permitida")
                    else:
                        print("Aviso: Chamada recursiva para a funcao principal")
                
                # verifica se funcao chamada existe e ja muda seu estado
                if symbol['name'] == functionCalled:
                    symbol['state'] = 'utilizada'
                    funcExists = True

            if not funcExists:
                print("Erro: Chamada a funcao '{}' que nao foi declarada".format(functionCalled))
       

            n_params = 0
            aux = node.children[2]
            if aux.children[0].name != 'vazio':
                # se tem 1 param:
                if len(aux.children) == 1:
                    n_params = 1

                # tem mais de 1 param:
                else:
                    # conta o primeiro param
                    n_params = 1
                    # desce a arvore ate descobrir quantos params a funcao tem
                    while len(aux.children) != 1:
                        n_params += 1
                        aux = aux.children[0]


            # atribui o numero de parametro a funcao
            for symbol in symbols_table: 
                func_name = node.children[0].children[0].name
                if symbol['name'] == func_name and symbol['token'] == 'func':
                    symbol['real-params'] = n_params

            # verifica quantidade de parametros na funcao
            for symbol in symbols_table:
                if symbol['token'] == 'func':
                    if ('real-params' in symbol):
                        if (symbol['formal-params'] != 0) and (symbol['formal-params'] != symbol['real-params']):
                            print("Erro: Chamada a funcao '{}' com {} parametro(s), mas foram declarado(s) {}".format(symbol['name'], symbol['real-params'], symbol['formal-params']))

                        if (symbol['formal-params'] == 0) and (symbol['real-params'] > 0):
                            print("Erro: Chamada a funcao '{}' com {} parametro(s), mas foram declarado(s) {}".format(symbol['name'], symbol['real-params'], symbol['formal-params']))

                        break

    # verifica se funcao eh utilizada
    for symbol in symbols_table:
        if (symbol['token'] == 'func') and (symbol['name'] != 'principal') and (symbol['state'] != 'utilizada'):
            print("Aviso: Funcao '{}' declarada, mas nao utilizada".format(symbol['name']))





##################################################################################
##################################################################################
############################### verifica variaveis ###############################
##################################################################################
##################################################################################
def check_vars(root, symbols_table):
    # percorre toda a árvore e procura por variáveis que tiveram atribuições e muda seu estado
    for symbol in symbols_table:
        if symbol['token'] == 'ID':
            for node in LevelOrderIter(root):
                if node.name == 'atribuicao':
                    for node2 in LevelOrderIter(node):
                        if node2.name == 'var':
                            # if not node2.children[0]:
                            if symbol['name'] == node2.children[0].children[0].name:
                                symbol['state'] = 'utilizada'
            
            # se estado da var nao eh 'utilizada' (nao tem atribuicao), devolve aviso
            if symbol['state'] == 'declarada':
                print("Aviso: Variavel '{}' declarada e nao inicializada".format(symbol['name']))

    # verifica se variavel foi usada sem ser declarada
    for node in LevelOrderIter(root):
        if node.name == 'atribuicao':
            declared = False
            for symbol in symbols_table:
                # verifica se var declarada globalmente
                if (symbol['token'] == 'ID') and (symbol['name'] == node.children[0].children[0].children[0].name):
                    declared = True

            if not declared:
                print("Erro: A variavel '{}' foi utilizada porem nao foi definida".format(node.children[0].children[0].children[0].name))





##################################################################################
##################################################################################
################################ Verifica vetores ################################
##################################################################################
##################################################################################
def check_multi_dimensional_vars(root, symbols_table):
    for node_i in LevelOrderIter(root):
        if node_i.name == 'atribuicao':
            # verifica se tem indice (tem mais de uma dimensao)
            if len(node_i.children[0].children) == 2:
                varName = node_i.children[0].children[0].children[0].name
                if node_i.children[0].children[1].name == 'indice':
                    # percorre toda a subarvore indice
                    for node_j in LevelOrderIter(node_i.children[0].children[1]):
                        if node_j.name == 'numero':
                            indexNumber = node_j.children[0].children[0].name
                            if node_j.children[0].name == 'NUM_PONTO_FLUTUANTE':
                                print("Erro: índice de array '{}' nao inteiro".format(varName))
                            else:
                                for symbol in symbols_table:
                                    if (symbol['name'] == varName) and (indexNumber > symbol['index'] or indexNumber < 0):
                                        print("Erro: índice de array '{}' fora do intervalo".format(varName))
                                




##################################################################################
##################################################################################
################################# Verifica tipos #################################
##################################################################################
##################################################################################
def check_assignments(root, symbols_table):
    # VERIFICA OS TIPOS DAS VARIAVEIS UTILIZADAS EM ATRIBUICOES    
    for node in LevelOrderIter(root):
        if node.name == 'atribuicao':
            var_name = node.children[0].children[0].children[0].name
            var_name2 = ''
            typeAssigned = ''
            typeUsed = ''

            # define o tipo da variavel
            for symbol in symbols_table:
                if symbol['name'] == var_name:
                    typeAssigned = symbol['type']


            for node2 in LevelOrderIter(node.children[2]):
                # se ocorre atribuicao chamando funcao, seta o tipo usado igual o da funcao
                if node2.name == 'chamada_funcao':
                    functionName = node2.children[0].children[0].name
                    for s in symbols_table:
                        if s['name'] == functionName:
                            typeUsed = s['type']
                            var_name2 = functionName

                # se ocorre atribuicao passando numero diretamente, atribui o nome e o tipo usados
                if node2.name == 'numero':
                    typeUsed = node2.children[0].name
                    var_name2 = node2.children[0].children[0].name

                # se ocorre atribuicao passando uma variavel
                if node2.name == 'var':
                    varName = node2.children[0].children[0].name
                    existsVar = False
                    # verifica se variavel existe
                    for symbol in symbols_table:
                        if symbol['name'] == varName:
                            existsVar = True
                            if symbol['token'] == 'ID':
                                typeUsed = symbol['type']
                                var_name2 = varName
                    
                    if not existsVar:
                        print("Erro: Variavel '{}' nao declarada".format(varName))
                        

            if (typeAssigned == 'NUM_INTEIRO'): typeAssigned = 'inteiro'
            if (typeAssigned == 'NUM_PONTO_FLUTUANTE'): typeAssigned = 'flutuante'
            if (typeUsed == 'NUM_INTEIRO'): typeUsed = 'inteiro'
            if (typeUsed == 'NUM_PONTO_FLUTUANTE'): typeUsed = 'flutuante'

            if typeUsed == 'inteiro':
                if typeAssigned == 'flutuante':
                    print("Aviso: Atribuicao de tipos distintos, '{}' eh {} e recebe '{}' do tipo {}".format(var_name, typeAssigned, var_name2, typeUsed))
                
            if typeUsed == 'flutuante':
                if typeAssigned == 'inteiro':
                    print("Aviso: Atribuicao de tipos distintos, '{}' eh {} e recebe '{}' do tipo {}".format(var_name, typeAssigned, var_name2, typeUsed))





##################################################################################
##################################################################################
################################## poda arvore ###################################
##################################################################################
##################################################################################
def cut_tree(root):
    # percorre a arvore
    for node_i in LevelOrderIter(root):
        # se noh tem soh 1  filho
        if len(node_i.children) == 1:
            if node_i.children[0].children:
                node_name = node_i.name
                # se noh nao for noh programa
                if node_name != 'programa':
                    children = node_i.children
                    parent = node_i.parent
                    # pai do neto recebe pai do noh atual (corta o noh)
                    node_i.children[0].parent = node_i.parent
                    # preenche a lista de filhos do noh
                    parent.children = tuple(list(parent.children)[0:len(parent.children) - 1])
                    list_children = list(node_i.parent.children)

                    # percorre filhos e os atualiza a lista
                    for i in range(len(list_children)):
                        # se filho for noh atual
                        if list_children[i] == node_i:
                            # filho recebe pos 0 da lista de filhos
                            list_children[i] = children[0]
                            
                    # atualiza os filhos do noh
                    node_i.parent.children = tuple(list_children)

                    # chama func novamente ate percorrer toda arvore
                    cut_tree(root)
                    break





##################################################################################
##################################################################################
##################################### main #######################################
##################################################################################
##################################################################################
def main():
    # argv[1] = 'teste.tpp'
    aux = argv[1].split('.')
    if aux[-1] != 'tpp':
        raise IOError("Not a .tpp file!")

    if root and root.children != ():
        try:
            print()
            print("Realizando analise semantica...")
            print()
            
            symbols_table = create_symbols_table(root)
            check_main(symbols_table) 
            check_functions(root, symbols_table) 
            check_vars(root, symbols_table)   
            check_multi_dimensional_vars(root, symbols_table)
            check_assignments(root, symbols_table) 
            cut_tree(root)
            print()

            # for symbol in symbols_table:
            #     print('symbol: ', symbol)

            # print('Tabela de simbolos: ')
            # print(symbols_table)
            print()

            # print("Gerando arvore sintatica reduzida...")
            UniqueDotExporter(root).to_picture(argv[1] + ".cuttedTree.png")
            

        except:
            print("Nao foi possivel fazer a analise semantica")

        print('\n\n')
        
        try: 
            generate_i_code(root, symbols_table, aux[0])

        except:
            print("Não foi possível gerar o código")


if __name__ == "__main__":
    main()
