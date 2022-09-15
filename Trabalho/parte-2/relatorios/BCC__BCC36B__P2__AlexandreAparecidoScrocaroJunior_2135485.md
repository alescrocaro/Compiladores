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

As regras sintáticas da gramática da linguagem TPP estão no padrão BNF (Backus-Naur Form) definidas da seguinte forma:\
simbolo ::= expressao\
Onde simbolo é um não terminal e expressao consiste em uma sequencia de simbolos e/ou sequencias separadas por '|' simbolizando um 'ou'.\
Abaixo estão listadas todas as regras sintáticas da linguagem.

#### programa

programa ::= lista_declaracoes

![image](https://user-images.githubusercontent.com/37521313/190294086-4df9c786-37c5-46ee-8bad-953de381c03b.png)


#### lista_declaracoes

lista_declaracoes ::= lista_declaracoes declaracao | declaracao

![image](https://user-images.githubusercontent.com/37521313/190294547-53e9a2e1-330d-4651-8019-09bf8329b394.png)


#### declaracao

declaracao ::= declaracao_variaveis | inicializacao_variaveis | declaracao_funcao

![image](https://user-images.githubusercontent.com/37521313/190294378-7b20810e-1d62-4db0-9a9a-18ab44494f92.png)


#### declaracao_variaveis

declaracao_variaveis ::= tipo DOIS_PONTOS lista_variaveis


![image](https://user-images.githubusercontent.com/37521313/190294427-06fb8463-909a-4f5c-96ad-155f3c00ff20.png)


#### inicializacao_variaveis

inicializacao_variaveis ::= atribuicao

![image](https://user-images.githubusercontent.com/37521313/190294639-6cb8b7df-cd54-45fd-a47b-500e3e6646da.png)


#### lista_variaveis

lista_variaveis ::= lista_variaveis VIRGULA var | var

![image](https://user-images.githubusercontent.com/37521313/190294831-1764226d-5646-4bd5-9a9b-8b89bac72f46.png)


##### var

var ::= ID | ID indice

![image](https://user-images.githubusercontent.com/37521313/190294912-af7ded01-ea2c-4d33-a6a3-be00ae3f70d6.png)


#### indice

indice ::= indice ABRE_COLCHETE expressao FECHA_COLCHETE | ABRE_COLCHETE expressao FECHA_COLCHETE

![image](https://user-images.githubusercontent.com/37521313/190295023-6db02f70-20b7-4237-a677-8993349a96a5.png)


#### tipo

tipo ::= INTEIRO | FLUTUANTE

![image](https://user-images.githubusercontent.com/37521313/190296793-3f90551a-1d4c-4615-bade-3c6f56720d63.png)


#### declaracao_funcao

declaracao_funcao ::= tipo cabecalho | cabecalho

![image](https://user-images.githubusercontent.com/37521313/190295118-87f0c49b-5db3-4465-a155-1b09689906af.png)


#### cabecalho

cabecalho ::= ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE corpo FIM

![image](https://user-images.githubusercontent.com/37521313/190295193-ce6cab7e-fe04-42d4-81e9-44528368419b.png)


#### lista parametros

lista_parametros ::= lista_parametros VIRGULA parametro | parametro | vazio

![image](https://user-images.githubusercontent.com/37521313/190295263-7484911e-b0ea-492e-a74c-78ce9e4bb237.png)


#### parametro

parametro ::= tipo DOIS_PONTOS ID |  parametro ABRE_COLCHETE FECHA_COLCHETE

![image](https://user-images.githubusercontent.com/37521313/190295308-f245d774-3a6b-4c4a-9101-0f4a6b369fe2.png)


#### corpo

corpo ::= corpo acao | vazio 

![image](https://user-images.githubusercontent.com/37521313/190295353-0b9a381d-06e3-474c-9aa6-a1f0348c2a60.png)


#### acao

acao ::= expressao | declaracao_variaveis | se | repita | leia | escreva | retorna | erro

![image](https://user-images.githubusercontent.com/37521313/190295425-347e34c3-c418-4881-8796-51fc59a5fc31.png)


#### se

se ::= SE expressao ENTAO corpo FIM | SE expressao ENTAO corpo SENAO corpo FIM

![image](https://user-images.githubusercontent.com/37521313/190295491-eb0c93e0-118e-495c-aca6-5ef713b300f2.png)


#### repita

repita ::= REPITA corpo ATE expressao

![image](https://user-images.githubusercontent.com/37521313/190295552-061558f1-d1ed-4fbc-bd9c-dfb16722384f.png)


#### atribuicao

atribuicao ::= var ATRIBUICAO expressao

![image](https://user-images.githubusercontent.com/37521313/190295586-283993f5-e14d-4c7b-b897-59f04864e906.png)


#### leia

leia ::= LEIA ABRE_PARENTESE var FECHA_PARENTESE

![image](https://user-images.githubusercontent.com/37521313/190295634-efb1f997-b9dc-4ddf-af27-469cbde77fe7.png)


#### escreva

escreva ::= ESCREVA ABRE_PARENTESE expressao FECHA_PARENTESE

![image](https://user-images.githubusercontent.com/37521313/190295690-61ad6ce6-5de8-4a8a-9421-e85f9f08b52c.png)


#### retorna

retorna ::= RETORNA ABRE_PARENTESE expressao FECHA_PARENTESE

![image](https://user-images.githubusercontent.com/37521313/190295723-529edc8a-6872-4b9c-a563-8f67e584e85c.png)


#### expressao

expressao ::= expressao_logica | atribuicao


![image](https://user-images.githubusercontent.com/37521313/190295756-227eb903-3e15-4551-86c6-b44e9dc28109.png)

#### expressao_logica

expressao_logica ::= expressao_simples | expressao_logica operador_logico expressao_simples

![image](https://user-images.githubusercontent.com/37521313/190295837-454b46be-697c-42ec-ae12-d00a04478cfc.png)


#### expressao_simples

expressao_simples ::= expressao_aditiva | expressao_simples operador_relacional expressao_aditiva

![image](https://user-images.githubusercontent.com/37521313/190295859-45e5ab5d-556b-4e58-af3b-aa0f74f9cd31.png)


#### expressao_aditiva

expressao_aditiva ::= expressao_multiplicativa | expressao_aditiva operador_soma expressao_multiplicativa

![image](https://user-images.githubusercontent.com/37521313/190295935-aadf63bb-59ce-439b-abbe-5286f983fa35.png)


#### expressao_multiplicativa

expressao_multiplicativa ::= expressao_unaria | expressao_multiplicativa operador_multiplicacao expressao_unaria

![image](https://user-images.githubusercontent.com/37521313/190295969-30cc4768-4b2a-4b64-bc61-7e2c1bfd804c.png)


#### expressao_unaria

expressao_unaria ::= fator | operador_soma fator | operador_negacao fator

![image](https://user-images.githubusercontent.com/37521313/190296007-5e7cfbe4-b543-4a57-a75f-d01b98436afd.png)


#### operador_relacional

operador_relacional ::= MENOR | MAIOR | IGUAL | DIFERENTE | MENOR_IGUAL | MAIOR_IGUAL

![image](https://user-images.githubusercontent.com/37521313/190296052-d154641b-d19c-43c6-8635-11291ebc2eea.png)


#### operador_soma

operador_soma ::= MAIS | MENOS

![image](https://user-images.githubusercontent.com/37521313/190296069-fa9dfe65-8a85-4571-ba0d-0da55f85ee91.png)


#### operador_logico

operador_logico ::= E | OU

![image](https://user-images.githubusercontent.com/37521313/190296127-3860353c-4b84-470f-8559-d9a1306c900b.png)


#### operador_negacao

operador_negacao ::= NAO

![image](https://user-images.githubusercontent.com/37521313/190296149-cb58521b-9b42-436d-99fc-3a2038be69b3.png)


#### operador_multiplicacao

operador_multiplicacao ::= VEZES | DIVIDE

![image](https://user-images.githubusercontent.com/37521313/190296220-2f8b2dd7-7fda-4d82-9d62-07c514fda071.png)


#### fator

fator ::= ABRE_PARENTESE expressao FECHA_PARENTESE | var | chamada_funcao | numero

![image](https://user-images.githubusercontent.com/37521313/190296245-3a94cbf9-f872-47b5-ab53-3311a769c8e3.png)


#### numero

numero ::= NUM_INTEIRO | NUM_PONTO_FLUTUANTE | NUM_NOTACAO_CIENTIFICA

![image](https://user-images.githubusercontent.com/37521313/190296280-12ece892-e2a8-49ec-b464-487ba3ec65a9.png)


#### chamada_funcao

chamada_funcao ::= ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE

![image](https://user-images.githubusercontent.com/37521313/190296356-eef447ea-ff53-4b89-8b4d-c15d50f1ab7b.png)


#### lista_argumentos

lista_argumentos  ::= lista_argumentos VIRGULA expressao | expressao | vazio 

![image](https://user-images.githubusercontent.com/37521313/190296425-a7bd6369-3036-4cda-b16b-e471e0f5fee8.png)


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
