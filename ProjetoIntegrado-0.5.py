import mysql.connector
import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Rafaela@1103",
    database="MyBank"
)

print ('####  MyBank!  ####')
print ('>[1] - Já possuo uma conta, quero fazer LogIn; [2] - Não possuo uma conta e quero me registrar.<')
entrada01 = input (' >Escolha uma opção Valida: ')

if entrada01 == '1' or entrada01.lower() == 'login':
    print ('##DESCULPE CAMINHO INCOMPLETO!##')
elif entrada01 == '2' or entrada01.lower() == 'cadastro':
    print ('>Você selecionou a opção de Cadastro.')
    ponteiro = db.cursor ()
    CPF_Unico = False
    CPF_Inserido = str(input(' >Antes de começarmos, valide sua identidade inserindo seu CPF: '))
    ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")
    CPF_Duplicado_Resultados = ponteiro.fetchall ()
    if not CPF_Duplicado_Resultados:
        CPF_Unico = True
        ponteiro.execute("INSERT INTO tbl_cliente_conta (Cliente_CPF) VALUES ('"+str(CPF_Inserido)+"');")
        db.commit()
        print ('>Muito bem, CPF validado! Estamos quase lá.')
        Nascimento_Inserido = input('>Para prosseguir com o seu cadastro, informe a sua data de nascimento. DD/MM/AAAA: ')
        Nascimento_Formatado = str(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9])+"-"+str(Nascimento_Inserido[3])+str(Nascimento_Inserido[4])+"-"+str(Nascimento_Inserido[0])+str(Nascimento_Inserido[1]))
    else:
        print ('>Esse CPF já esta registrado, confira se checou errado ou se já possui uma conta.')
else:
    print ('>Por favor insira um valor valido.')

