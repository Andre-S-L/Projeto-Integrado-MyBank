print ('MyBank!')
Entrada01 = input ('[1] - Já possuo uma conta, quero fazer LogIn; [2] - Não possuo uma conta e quero me registrar.')


if Entrada01 == '1' or Entrada01.lower() == 'login':
    print ('sucesso I')
elif Entrada01 == 2 or Entrada01.lower() == 'cadastro':
    print ('sucesso II')
else:
    print ('Por favor insira um valor valido.')
