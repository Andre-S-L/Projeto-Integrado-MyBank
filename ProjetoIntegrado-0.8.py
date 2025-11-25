import mysql.connector
import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Rafaela@1103",
    database="MyBank"
)

print ('####  Bem-Vindo ao MyBank!  ####')
print ('\n')
print ('[1] - Já possuo uma conta, quero fazer LogIn.)
print ('[2] - Não possuo uma conta e quero me registrar.')
print ('\n')
entrada01 = input ('Escolha uma opção Valida: ')

if entrada01 == '1' or entrada01.lower() == 'login':
    print ('##DESCULPE CAMINHO INCOMPLETO!##')
elif entrada01 == '2' or entrada01.lower() == 'cadastro':
    print ('>Você selecionou a opção de Cadastro.')
    print ('\n')
    ponteiro = db.cursor ()
    CPF_Unico = False
    CPF_Inserido = str(input('Antes de começarmos, valide sua identidade inserindo seu CPF: '))
    ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")
    CPF_Duplicado_Resultados = ponteiro.fetchall ()
    if not CPF_Duplicado_Resultados:
        CPF_Unico = True
        ponteiro.execute("INSERT INTO tbl_cliente_conta (Cliente_CPF) VALUES ('"+str(CPF_Inserido)+"');")
        db.commit()
        print ('Muito bem, CPF validado! Estamos quase lá.')
        Nascimento_Inserido = input('>Para prosseguir com o seu cadastro, informe a sua data de nascimento. DD/MM/AAAA: ')
        Nascimento_Formatado = str(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9])+"-"+str(Nascimento_Inserido[3])+str(Nascimento_Inserido[4])+"-"+str(Nascimento_Inserido[0])+str(Nascimento_Inserido[1]))
        if len(Nascimento_Inserido) == 10 and (int(datetime.date.today().year) - int(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9]))) > 13:
            ponteiro.execute("UPDATE tbl_cliente_conta SET Cliente_Nasc = '"+str(Nascimento_Formatado)+"' WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")
            print ("Muito bem, validamos sua tentativa.")
            Nascimento_Valido = True
        else:
            print('Algo de errado ocorreu, lembresse que para fazer um registro no MyBank, é preciso ter mais de 13 anos, caso tenha, confira novamente de digitou seu aniversario corretamente em DD/MM/AAAA')
            ponteiro.execute("DELETE FROM tbl_cliente_conta WHERE Cliente_Conta_ID ="+str(Cliente_CPF)+";")
    else:
        print ('>Esse CPF já esta registrado, confira se checou errado ou se já possui uma conta.')
    if CPF_Unico = True and Nascimento_Valido = True:
        while True:
            Nome_Escolhido = str(input('Insira seu nome ou apelido.'))
            if len(Nome_Escolhido) > 0:
                Senha_Escolhida = str(input('Escolha uma senha com no minimo 8 digitos'))
                if len(Senha_Escolhida) > 0:
                    PIN_Escolhido = input('Escolha um PIN de segurança constituido 4 digitos numericos.')
                    if len(PIN_Escolhido) == 4 and type(PIN_Escolhido) == int:
                        ##AQUI VEM O CODIGO DE INSERÇÃO DE TUDO. COLOCAR QUANDO ABRIR O MYSQL##
                    else:
                        print ('Por favor, insira um PIN valido: 4 digitos numericos.')
                else:
                    print ('Por favor, escolha uma senha com no minimo 8 digitos.')
            else:
                print('Por favor, insira um nome ou apelido.')
    else:
        print ('Processo de cadastro não concluido. Por favor, verifique suas informações e tente novamente.')
else:
    print ('>Por favor insira um valor valido.')

