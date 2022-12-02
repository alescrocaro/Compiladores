def find_scope(node):
    # se o pai do declaracao variaveis eh o node 'declaracao', entao o escopo eh global ----> padrao da arvore
    if(node.parent.name == 'declaracao'):
        return 'global'

    # se escopo n eh global, ta dentro de funcao, entao sobe ate o cabecalho pra pegar o nome da funcao, que sera usado como o q define o escopo
    else:
        scope = node
        while(scope.name != 'cabecalho'):
            scope = scope.parent

        return scope.children[0].children[0].name
