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
    print ('>Você selecionou a opção de Cadastro.')
    ponteiro = db.cursor ()
    CPF_Unico = False
    Inserir_CPF = str(input('>Antes de começarmos, valide sua identidade inserindo seu CPF: '))
    ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Inserir_CPF)+"';")
    CPF_Duplicado_Resultados = ponteiro.fetchall ()
    if not CPF_Duplicado_Resultados:
        CPF_Unico = True
        ponteiro.execute("INSERT INTO tbl_cliente_conta (Cliente_CPF) VALUES ('"+str(Inserir_CPF)+"');")
        db.commit()
    else:
        print ('Esse CPF já esta registrado, confira se checou errado ou se já possui uma conta.')
    if CPF_Unico == True:
        print ('CPF Cadastrado. Demo Finalizada.')
    else:
        print ('CPF Não cadastrado. Demo Finalizada.')
else:
    print ('Por favor insira um valor valido.')

