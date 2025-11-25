import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Rafaela@1103",
    database="MyBank"
)

print ('MyBank!')
entrada01 = input ('[1] - Já possuo uma conta, quero fazer LogIn; [2] - Não possuo uma conta e quero me registrar. Escolha uma opção Valida: ')

if entrada01 == '1' or entrada01.lower() == 'login':
    print ('##DESCULPE CAMINHO INCOMPLETO!##')
elif entrada01 == '2' or entrada01.lower() == 'cadastro':
    print ('Você selecionou a opção de Cadastro.')
    ponteiro = db.cursor ()
    Cliente_CPF = str(input('Antes de começarmos, valide sua identidade inserindo seu CPF: '))
    ponteiro.execute('SELECT * FROM tbl_cliente_tbl_conta WHERE Cliente_CPF ='+str(Cliente_CPF))
    CPF_Duplicado_Resultado = ponteiro.fetchall ()
    if not CPF_Duplicado:
        CPF_Unico = True
        ponteiro.execute('INSERT INTO tbl_cliente_tbl_conta (Cliente_CPF) VALUES (" +str(Cliente_CPF) ")')
        db.commit()
    else:
        print ('Esse CPF já esta registrado, confira se checou errado ou se já possui uma conta.')
    if CPF_Unico == True:
        print ('Concluido até aqui')
else:
    print ('Por favor insira um valor valido.')

