{Condicional}
inteiro: a
inteiro: z

inteiro principal()
	inteiro: ret

	a := 25    
	se a > 5 então
		se a < 20 então
			ret := 1
		senão
			ret := 2
		fim
	senão
		ret := 0
  fim

	z := 4
  retorna(ret)
fim
