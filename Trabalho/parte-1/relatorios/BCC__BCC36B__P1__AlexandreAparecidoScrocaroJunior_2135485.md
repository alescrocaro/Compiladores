# Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Léxica (Trabalho – 1ª parte)

**Autor:** Alexandre Aparecido Scrocaro Junior \
**email:** alescrocaro@gmail.com

**Professor:** Rogério Aparecido Gonçalves\
**Universidade Tecnológica Federal do Paraná (UTFPR)**

## Análise Léxica

### Resumo

A primeira parte do trabalho consiste na implementação de um analisador léxico - também chamado de _scanner_ ou sistema de varredura - para a linguagem TPP, para tanto, foi utilizada a documentação da linguagem disponibilizada pelo professor. A linguagem/ferramenta utilizada foi Python/PLY, além de fazer uso de expressões regulares para analisar os _tokens_.

---

### Especificação da linguagem de programação TPP

- Tipos básicos de dados suportados: **inteiro** e **flutuante**
- Suporte a arranjos uni e bidimensionais **(_arrays_)**
  - Exemplos:
    - tipo: identificador[dim]
    - tipo: identificador[dim][dim]
- Variáveis locais e globais devem ter um dos tipos especificados
- Tipos de funções podem ser omitidos (quando omitidos viram um procedimento e um tipo _void_ é devolvido explicitamente
- Linguagem quase fortemente tipificada: nem todos os erros são especificados mas sempre deve ocorrer avisos
- Operadores aritméticos: +, -, \* e /
- Operadores lógicos: e (&&), ou (||) e não (!)
- Operador de atribuição: recebe (:=).
- Operadores de comparação: maior (>), maior igual (>=), menor (<), menor igual (<=), igual (=).

---

### Especificação formal dos autômatos para a formação de cada classe de token da linguagem

#### Autômato de identificador:

Primeiramente, as classes mais simples:

- letra = [a-zA-Z]+
- digito = [0-9]+

Agora, podemos criar um autômato de um identificador da seguinte forma:\
![Autômato de identificador](https://user-images.githubusercontent.com/37521313/186780863-d8b8cd95-7605-4dfd-b328-0e45021ce625.png)

#### Autômato de número flutuante:

Primeiramente, as classes mais simples:

- sinal = [+-]\* (o sinal pode ter nada, é repassado com épsilon)
- digito = [0-9]+

Agora, podemos criar um autômato de um número flutuante da seguinte forma:\
![Autômato de número flutuante](https://user-images.githubusercontent.com/37521313/186780932-0bde9c74-76a7-405e-9bc2-4e0e75414622.png)

---

### Detalhes da implementação da varredura na LP e ferramenta (e/ou bibliotecas) escolhidas pelo projetista

O sistema de varredura, ou analisador léxico, é a fase do compilador na qual se lê o código-fonte como um arquivo de caracteres e o separa em um conjunto de _tokens_, os quais são reconhecidos através das expressões regulares. A implementação do analisador será explicada a seguir.\
Em primeiro lugar, define-se os _tokens_:

![image](https://user-images.githubusercontent.com/37521313/188000342-eb3ba115-b3e5-4d76-b94a-83c17837bf53.png)

Também define-se as palavras reservadas:

![image](https://user-images.githubusercontent.com/37521313/187549845-c14eac53-1005-4c68-ab5d-945ce54300ce.png)

Assim como os símbolos e operadores que serão utilizados para reconhecer as facilidades da linguagem TPP, e suas expressões regulares:

![image](https://user-images.githubusercontent.com/37521313/187550420-394c93fd-7d7a-4b89-b6a6-6707afd2772f.png)

![image](https://user-images.githubusercontent.com/37521313/187550032-3ad7d105-ca56-4181-b4d6-86a5c4d4c20e.png)

![image](https://user-images.githubusercontent.com/37521313/187550074-0d6f4d32-893f-4b25-96ec-64ae23db1550.png)

![image](https://user-images.githubusercontent.com/37521313/187550158-d302b3b0-616a-4e1e-9bd4-005ca16be981.png)

![image](https://user-images.githubusercontent.com/37521313/187550255-aaef67db-0d27-45c2-b78d-60595fb899ec.png)


Após isso, foram definidas as funções para reconhecer as classes (ID - que requer atenção especial para não coincidir com nenhuma palavra reservada, notação científica, número de ponto flutuante, número inteiro, comentários, novas linhas e colunas):

![image](https://user-images.githubusercontent.com/37521313/187550565-ab5da40d-dec5-4aa7-9511-a95a640408cf.png)

Além disso, também são reconhecidos erros de caracteres especiais que a linguagem não contém (como $ e ç) e é mostrada sua posição no código (linha e coluna):

![image](https://user-images.githubusercontent.com/37521313/187550641-1d024109-85a3-4d22-93b1-7826f115872d.png)

Por último, o código retorna a lista de tokens correspondentes ao arquivo escolhido por quem executa o comando para iniciá-lo, percorrendo todo o código TPP do arquivo selecionado.

![image](https://user-images.githubusercontent.com/37521313/187550743-d9df19e1-7174-4e0b-9879-d91d8b67f991.png)

A ferramenta utilizada foi o Python PLY, que é uma implementação do lex e yacc e utiliza LR-parsing - que é razoavelmente eficiente. O lex possui a facilidade na tokenização de uma _string_ de entrada, por exemplo:

**_String_ de entrada:**\
x = 3 + 42 \* (s - t)\

**_String_ após tokenização:**\
'x','=', '3', '+', '42', '\*', '(', 's', '-', 't', ')'

**_Tokens_ obtidos:**\
ID, IGUAL, INTEIRO, MAIS, INTEIRO, VEZES, ABRE_PARENTESE, ID, MENOS, ID, FECHA_PARENTESE

---

### Exemplos de saída do sistema de varredura (lista de tokens) para exemplos de entrada (código fonte)

#### Código para verificar valor 10:

**ENTRADA:**\
![Código para verificar valor 10](https://user-images.githubusercontent.com/37521313/186780341-c66544d5-b647-4b46-8987-1cc0538629b6.png)

**SAIDA:**\
INTEIRO\
ID\
ABRE_PARENTESE\
FECHA_PARENTESE\
INTEIRO\
DOIS_PONTOS\
ID\
ID\
ATRIBUICAO\
NUM_INTEIRO\
REPITA\
SE\
ID\
IGUAL\
NUM_INTEIRO\
ESCREVA\
ABRE_PARENTESE\
[6,12]: Caracter inválido ' " '\
ID\
NUM_INTEIRO\
[6,21]: Caracter inválido ' " '\
FECHA_PARENTESE\
FIM\
ID\
MAIS\
MAIS\
ID\
ID\
IGUAL\
NUM_INTEIRO\
ID\
ABRE_PARENTESE\
NUM_INTEIRO\
FECHA_PARENTESE\
FIM

#### Código de produto escalar:

**ENTRADA:**\
![Código de produto escalar](https://user-images.githubusercontent.com/37521313/186780450-6a1dd80e-e55e-4f00-9a01-4ffc39e74116.png)

**SAIDA:**\
INTEIRO\
ID\
ABRE_PARENTESE\
INTEIRO\
DOIS_PONTOS\
ID\
ABRE_COLCHETE\
FECHA_COLCHETE\
VIRGULA\
INTEIRO\
DOIS_PONTOS\
ID\
ABRE_COLCHETE\
FECHA_COLCHETE\
VIRGULA\
INTEIRO\
DOIS_PONTOS\
ID\
FECHA_PARENTESE\
INTEIRO\
DOIS_PONTOS\
ID\
ID\
ATRIBUICAO\
NUM_INTEIRO\
INTEIRO\
DOIS_PONTOS\
ID\
ID\
ATRIBUICAO\
NUM_INTEIRO\
SE\
ID\
MAIOR\
NUM_INTEIRO\
ID\
REPITA\
ID\
ATRIBUICAO\
ID\
MAIS\
ID\
ABRE_COLCHETE\
ID\
FECHA_COLCHETE\
MULTIPLICACAO\
ID\
ABRE_COLCHETE\
ID\
FECHA_COLCHETE\
ID\
ATRIBUICAO\
ID\
MAIS\
NUM_INTEIRO\
ID\
ID\
IGUAL\
ID\
RETORNA\
ABRE_PARENTESE\
ID\
FECHA_PARENTESE\
FIM

---

### Implemente uma função que imprima a lista de tokens, não utilize a saída padrão da ferramenta de implementação de Analisadores Léxicos

Para tanto, basta tokenizar o arquivo de entrada e imprimir todos os _tokens_ obtidos, que é feito na função a seguir.

![Função para imprimir tokens](https://user-images.githubusercontent.com/37521313/186780246-ccf764e7-cc6e-4012-8d51-273d82de167c.png)
