import os

for i in range(1, 18):
  if i < 10:
    file_number = '00{}'.format(i)
  else:
    file_number = '0{}'.format(i)

  print()
  print()
  print('executando o teste {}...'.format(file_number))
  os.system('python3 tppsemantic.py geracao-codigo-testes/gencode-{}.tpp'.format(file_number))
