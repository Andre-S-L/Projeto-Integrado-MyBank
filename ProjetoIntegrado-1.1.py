import mysql.connector
import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Rafaela@1103",
    database="MyBank"
)

ponteiro = db.cursor ()

print ('####  Bem-Vindo ao MyBank!  ####')
print ('\n')
print ('[1] - Já possuo uma conta, quero fazer LogIn.')
print ('[2] - Não possuo uma conta e quero me registrar.')
entrada01 = input ('Escolha uma opção Valida: ')

if entrada01 == '1' or entrada01.lower() == 'login':
    print ('##DESCULPE CAMINHO INCOMPLETO!##')
elif entrada01 == '2' or entrada01.lower() == 'cadastro':
    print ('>Você selecionou a opção de Cadastro.')
    print ('\n')
    CPF_Unico = False
    PIN_Valido = False
    Senha_Valida = False
    Nome_Valido = False
    Nascimento_Valido = False
    CPF_Inserido = str(input('Antes de começarmos, confirme sua identidade. Insira seu CPF: '))
    ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")
    CPF_Duplicado_Resultados = ponteiro.fetchall ()
    if not CPF_Duplicado_Resultados:
        CPF_Unico = True
        print ('Muito bem! identidade validada!')
        Nascimento_Inserido = input('Para iniciar seu cadastro, informe a sua data de nascimento. (DD/MM/AAAA): ')
        Nascimento_Formatado = str(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9])+"-"+str(Nascimento_Inserido[3])+str(Nascimento_Inserido[4])+"-"+str(Nascimento_Inserido[0])+str(Nascimento_Inserido[1]))
        if len(Nascimento_Inserido) == 10 and (int(datetime.date.today().year) - int(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9]))) > 13:
            print ("Dados em ordem, preparações para criação de conta finalizadas!")
            Nascimento_Valido = True
        else:
            print ('\n')
            print('Algo de errado ocorreu! Lembresse que para fazer um registro no MyBank, é preciso ter mais de 13 anos, caso tenha, confira novamente de digitou seu aniversario corretamente em DD/MM/AAAA')
    else:
        print ('\n')
        print ('(ATENÇÃO!) Esse CPF já esta registrado, confira se checou errado ou se já possui uma conta.')
    if CPF_Unico == True and Nascimento_Valido == True:
        while True:
            if PIN_Valido == True:
                print ('Registro concluido com sucesso, Bem-Vindo', str(Nome_Escolhido), 'ao MyBank!')
                ponteiro.execute("INSERT INTO tbl_cliente_conta (Cliente_Nome, Cliente_CPF, Cliente_Nasc, Conta_Senha, Conta_Pin, Conta_QntAtual) VALUES ('"+str(Nome_Escolhido)+"', '"+str(CPF_Inserido)+"', '"+str(Nascimento_Formatado)+"', '"+str(Senha_Escolhida)+"', '"+str(PIN_Escolhido)+"', '0.00');")
                db.commit()
                break
            else:
                pass
            if Senha_Valida == True:
                PIN_Escolhido = str(input('>Insira um PIN de segurança de 4 digitos numericos: '))
                if len(PIN_Escolhido) == 4 and str.isdigit(PIN_Escolhido):
                    PIN_Valido = True
                else:
                    print ("Por favor, insira um PIN adequado feito de 4 digitos numericos! ")
                    print ('\n')
            else:
                pass
            if Nome_Valido == True and PIN_Valido == False: #Tive que colocar que o PIN precisa ser falso aqui pra ele não perguntar a senha duas vezes, sei que fica estranho mas é assim.
                Senha_Escolhida = str(input('>Crie uma senha: '))
                if len(Senha_Escolhida) >= 8:
                    Senha_Valida = True
                else:
                    print ('Por favor, insira uma senha de pelo menos 8 digitos!')
                    print ('\n')
            else:
                pass

            if Nome_Valido == False:
                Nome_Escolhido = str(input('>Insira seu usuario: '))
                if len(Nome_Escolhido) > 0:
                    Nome_Valido = True
                else:
                    print ('Por favor, insira seu nome')
                    print ('\n')
            else:
                pass
    else:
        print ('(ATENÇÃO!) Processo de cadastro não concluido. Por favor, verifique suas informações e tente novamente.')
else:
    print ('>Por favor insira um valor valido.')


ponteiro.close
db.close
