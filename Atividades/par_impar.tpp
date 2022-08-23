inteiro parOuImpar(inteiro: n)  
  inteiro: resultadoDivisao, verificacao

  resultadoDivisao := n/2
  verificacao := resultadoDivisao * 2

  se verificacao = n então 
    retorna(0)
  senão
    retorna(1)
  fim
fim

inteiro principal()
  inteiro: n
  leia(n)
  
  se parOuImpar(n) = 0 então

    escreva("O numero eh par.")
  senao
    escreva("O numero eh impar.")
  fim  
fim