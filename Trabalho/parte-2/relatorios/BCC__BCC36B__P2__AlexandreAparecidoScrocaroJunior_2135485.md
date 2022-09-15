# Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Sintática (Trabalho – 2ª parte)

**Autor:** Alexandre Aparecido Scrocaro Junior \
**email:** alescrocaro@gmail.com

**Professor:** Rogério Aparecido Gonçalves\
**Universidade Tecnológica Federal do Paraná (UTFPR)**

## Análise Sintática

### Resumo

TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

---

### Descrição da gramática

#### Regras

##### programa

##### declaracao

##### declaracao_variaveis

##### inicializacao_variaveis

##### var

##### tipo

##### declaracao_funcao

##### cabecalho

##### parametro

##### corpo

##### acao

##### se

##### repita

##### atribuicao

##### leia

##### escreva

##### retorna

##### expressao

##### expressao_simples

##### expressao_aditiva

##### expressao_multiplicativa

##### expressao_unaria

##### operador_relacional

##### operador_soma

##### operador_logico

##### operador_negacao

##### operador_multiplicacao

##### fator

##### numero

##### chamada_funcao

---

### Formato da análise sintática

O formato utilizado é o LALR(1), ele tem vantagem sobre o LR(1) pois diminui o número de estados e gera uma tabela consideravelmente menor. Além de que é suportado pela ferramenta utilizada, o PLY.

---

### Utilização da ferramenta Yacc e implementação do parser

O Yacc é um gerador automático de Analisadores sintáticos LALR(1). Ele possui extensos recursos de depuração e relatório de erros, nós o utilizamos para construir o _parser_, como pode ser visto abaixo.
![Yacc build parser](https://user-images.githubusercontent.com/37521313/190282781-5931edf0-20fe-4d8d-ab6f-2ef942874786.png)

Seguindo para a implementação, foi feita uma função para cada regra gramatical com seu respectivo nome, seguindo o padrão "p_regra(p)". Esse "p" passado por parâmetro corresponde a uma sequência contendo os valores de cada símbolo da gramática na regra correspondente. Além disso, os valores de p[i] (observados na imagem abaixo) são mapeados nos símbolos da gramática.\
Para exemplificar, observa-se o código abaixo da regra "repita".

![regra repita](https://user-images.githubusercontent.com/37521313/190283852-9b4de4cb-6efc-4546-81ce-e10a2f4d0139.png)

Primeiro, define-se em um comentário a regra que executará a função se for encontrada (repita: REPITA corpo ATE expressao). Isso é implementado como uma árvore criando nós da classe MyNode (criada no arquivo _mytree.py_) de forma que o p[0] é a própria regra repita e se torna o pai da subárvore, o p[1] é a palavra **REPITA**, p[2] é o **corpo** dentro de repita, p[3] é a palavra **ATE** que identifica o que irá 'quebrar' a regra, enfim o p[4] será a expressão que 'quebra' a repetição.

![erro regra repita](https://user-images.githubusercontent.com/37521313/190283896-0cb2d28c-70a1-4271-a632-9fd4de19fdaa.png)

As regras também terão excessões, definidas em funções com o mesmo nome da regra com a adição de "\_error" ao fim. \
Assim como na regra, há um comentário definindo quando a excessão será executada, nesse caso é quando há erro nos tokens **REPITA** ou **ATE**. Mostrando ao usuário através de um _print_ no _console_.

---

### Implementação da árvore sintática

Para a árvore foi utilizada a biblioteca _Anytree_ para o auxílio da implementação de nós, extendendo uma classe Python para um nó de árvore (NodeMixin). Cada nó contém um identificador, nome, rótulo, tipo e uma referência para seu pai. As regras e cada expressão ou corpo são subárvores dentro da árvore maior que constitui o programa todo.\
Abaixo está a implementação do nó da árvore utilizando o NodeMixin do _Anytree_.

![Implementação arvore](https://user-images.githubusercontent.com/37521313/190286658-fc62ab76-573d-4a1a-bfc9-4636dc8e214d.png)

---

### Exemplo de Entrada e Saída. Impressão da Árvore.

fazer exemplo sem e com erro
TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

---

### Referências

[Documentação do anytree](https://anytree.readthedocs.io/en/latest/)\
[Documentação do PLY (e Yacc)](https://www.dabeaz.com/ply/ply.html)
