import mysql.connector
import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Rafaela@1103",
    database="MyBank"
)

ponteiro = db.cursor ()

Login_Valido = False

while Login_Valido == False:
 print ('####------------------------Bem-Vindo ao MyBank!------------------------####')
 print ('[1] - Já possuo uma conta, quero fazer LogIn.')
 print ('[2] - Não possuo uma conta e quero me registrar.')
 entrada01 = input ('>Escolha uma opção Valida: ')
 if entrada01 == '1' or entrada01[0].lower() == 'l':
    print (' ')
    print ('=Você selecionou a opção: Login')
    print ("<Em qualquer momento, digite 'Cancel' para cancelar>")
    while True:
        print (' ')
        Login_Usuario = str(input('>Insira seu CPF: '))
        if Login_Usuario == 'cancel':
            print ('Cancelando Login')
            print ('####--------------------------------------------------------------------####')
        else:
         ponteiro.execute("SELECT Conta_Senha FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
         Usuario_Validacao = ponteiro.fetchall ()
         if not Usuario_Validacao:
            print ('[x] - Usuario não encontrado, verifique se você inseriu seu CPF corretamente.')
            print ('\n')
         else:
            Usuario_Senha = str(input('>Digite sua senha: '))
            if Usuario_Senha.lower () == 'cancel':
                print ('Cancelando Login.')
                print ('####--------------------------------------------------------------------####')
                break
            elif str(Usuario_Validacao) == "[('"+Usuario_Senha+"',)]":
                print ('=Login concluido com sucesso!')
                print ('####--------------------------------------------------------------------####')
                ponteiro.execute("SELECT Cliente_Nome FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
                Nome_Mostrado = ponteiro.fetchone ()
                print ('\n')
                print ('####--------------------------------------------------------------------####')
                print ('Bem-Vindo de volta, '+str(Nome_Mostrado[0])+', a sua conta MyBank!') #Perguntar pro alan como tirar as aspas, tanto pra ficar bonito, e pra saber se tem como simplificar o (if str(Usuario_Validacao) == "[('"+Usuario_Senha+"',)]" )
                Login_Valido = True
                break
            else:
                print ('[x] - Senha incorreta ou login incorretos.')
 elif entrada01 == '2' or entrada01[0].lower() == 'c':
    print (' ')
    print ('=Você selecionou a opção: Cadastro.')
    print ("<Em qualquer momento, digite 'Cancel' para cancelar>")
    CPF_Unico = False
    PIN_Valido = False
    Senha_Valida = False
    Nome_Valido = False
    Nascimento_Valido = False
    print (' ')
    CPF_Inserido = str(input('>Antes de começarmos, confirme sua identidade. Insira seu CPF no formato(NNN.NNN.NNN-NN): '))
    Loop_Cad_1 = True
    while Loop_Cad_1 == True:
      if CPF_Inserido[0].lower () == 'c':
         print ('Cancelando Cadastro...')
         break
      elif len(CPF_Inserido) == 14:
       ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")
       CPF_Duplicado_Resultados = ponteiro.fetchall ()
       if not CPF_Duplicado_Resultados:
        CPF_Unico = True
        while True:
         Nascimento_Inserido = input('>Informe-nos a sua data de nascimento (DD/MM/AAAA): ')
         if Nascimento_Inserido[0].lower () == 'c':
            print ('Cancelando Cadastro...')
            Loop_Cad_1 = False
            break
         elif len(Nascimento_Inserido) == 10 and int(Nascimento_Inserido[0]+Nascimento_Inserido[1]) <= 31 and int(Nascimento_Inserido[3]+Nascimento_Inserido[4]) <= 12:
           Nascimento_Formatado = str(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9])+"-"+str(Nascimento_Inserido[3])+str(Nascimento_Inserido[4])+"-"+str(Nascimento_Inserido[0])+str(Nascimento_Inserido[1]))
           if len(Nascimento_Inserido) == 10 and (int(datetime.date.today().year) - int(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9]))) > 13:
             print ("Dados em ordem, preparações para criação de conta finalizadas!")
             print (' ')
             Nascimento_Valido = True
             Loop_Cad_1 = False
             break
           else:
             print (' ')
             print('[x] - Cadastro cancelado! Para fazer um registro no MyBank é preciso ter, legalmente, mais de 13 anos de idade.')
             print('\n')
             Loop_Cad_1 = False
             break
         else:
             print ('[x] - Data invalida, por favor confira se digitou corretamente. Lembresse de usar DD/MM/AAAA.')
             print (' ')
         break 
       else:
         print (' ')
         print ('[x] - Esse CPF já esta registrado, confira se checou errado ou se já possui uma conta.')
         Loop_Cad_1 = False
      else:
        Loop_Cad_1 = True
        print ('[x] - Por favor, insira um CPF valido. ')
        print (' ')
        CPF_Inserido = str(input('>Tente novamente, insira seu CPF com o formato (NNN.NNN.NNN-NN): '))
    if CPF_Unico == True and Nascimento_Valido == True:
        Loop_Cad_2 = True
        while Loop_Cad_2 == True:
            if PIN_Valido == True:
                print (' ')
                print ('Registro concluido com sucesso.')
                print ('Bem-Vindo ao MyBank', str(Nome_Escolhido))
                print ('####--------------------------------------------------------------------####')
                print ('\n')
                ponteiro.execute("INSERT INTO tbl_cliente_conta (Cliente_Nome, Cliente_CPF, Cliente_Nasc, Conta_Senha, Conta_Pin, Conta_QntAtual) VALUES ('"+str(Nome_Escolhido)+"', '"+str(CPF_Inserido)+"', '"+str(Nascimento_Formatado)+"', '"+str(Senha_Escolhida)+"', '"+str(PIN_Escolhido)+"', '0.00');")
                db.commit()
                break
            else:
                pass
            if Senha_Valida == True:
                PIN_Escolhido = str(input('>Insira um PIN de segurança de 4 digitos numericos: '))
                if PIN_Escolhido.lower () == 'cancel':
                    print ('Cancelando Cadastro...')
                    print ('Operação de cadastro Cancelado.')
                    print ('####--------------------------------------------------------------------####')
                    print ('\n')
                    Loop_Cad_2 = False
                    break
                elif len(PIN_Escolhido) == 4 and str.isdigit(PIN_Escolhido):
                    PIN_Valido = True
                else:
                    print ("[x] - Por favor, insira um PIN adequado feito de 4 digitos numericos! ")
                    print (' ')
            else:
                pass
            if Nome_Valido == True and PIN_Valido == False: #Tive que colocar que o PIN precisa ser falso aqui pra ele não perguntar a senha duas vezes, sei que fica estranho mas funciona.
                Senha_Escolhida = str(input('>Crie uma senha com no minimo 8 digitos: '))
                if Senha_Escolhida.lower () == 'cancel':
                    print ('Cancelando Cadastro...')
                    print ('Operação de cadastro Cancelado.')
                    print ('####--------------------------------------------------------------------####')
                    print ('\n')
                    Loop_Cad_2 = False
                    break
                elif len(Senha_Escolhida) >= 8:
                    Senha_Valida = True
                else:
                    print ('[x] - Por favor, insira uma senha de pelo menos 8 digitos!')
                    print (' ')
            else:
                pass
            if Nome_Valido == False:
                Nome_Escolhido = str(input('>Escolha um nome de usuario: '))
                if Nome_Escolhido.lower () == 'cancel':
                    print ('Cancelando Cadastro...')
                    print ('Operação de cadastro Cancelado.')
                    print ('####--------------------------------------------------------------------####')
                    print ('\n')
                    Loop_Cad_2 = False
                    break
                elif len(Nome_Escolhido) > 0:
                    Nome_Valido = True
                else:
                    print ('[x] - Por favor, insira seu nome!')
                    print (' ')
        else:
            pass
        
    else:
        print ('Operação de cadastro Cancelado.')
        print ('####--------------------------------------------------------------------####')
        print ('\n')
 else:
    print ('>Você selecionou uma opção não existente.')
    print ('=Por favor insira um valor valido.')
    print ('\n')

if Login_Valido == True:
    Escolha_Valida01 = False
    ponteiro.execute("SELECT Cliente_Conta_ID FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
    ID_Usuario = ponteiro.fetchone ()
    while Escolha_Valida01 == False:
        db.commit ()
        ponteiro.execute("SELECT Conta_QntAtual FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
        VALOR_Lista = ponteiro.fetchone ()
        VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
        print ('#ID do usuario:', str(ID_Usuario[0]))
        print ('#Seu atual saldo é de R$'+str(VALOR_Conta_Usuario))
        print (' ')
        print ('Selecione uma opção abaixo:')
        print ('[1] - Transferencia.')
        print ('[2] - Obter Emprestimo.')
        print ('[3] - Pagar Emprestimo.')
        print ('[4] - Opções')
        print ('[5] - LogOff')
        print ('[0] - Recarregar')
        entrada02 = input('>Escolha uma operação valida: ')
        if entrada02 == '1':
            Escolha_Valida01 = True
            Destin_Localizado = False
            Saldo_Suficiente = False
            PIN_Valido = False
            print ('=Você selecionou a opção: Transferencia')
            print (' ')
            while Destin_Localizado == False:
                db.commit ()
                ponteiro.execute("SELECT Conta_QntAtual FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
                VALOR_Lista = ponteiro.fetchone ()
                VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
                print (' ')
                print ('#Seu saldo atual é de R$'+str(VALOR_Conta_Usuario))
                print ("[Digite 'cancel' para cancelar]")
                Destinatario = input (">Por favor, insira ou o CPF (em formato NNN.NNN.NNN-NN), ou ID do destinatario: ")
                if Destinatario == str(ID_Usuario[0]) or Destinatario == Login_Usuario:
                    print (' ')
                    print ('[x] - Transferencia Cancelada. Não é possivel transferir um valor para si mesmo.')
                    print ('\n')
                    Escolha_Valida01 = False
                    break
                elif len(Destinatario) == 14:
                    db.commit ()
                    ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Destinatario)+"';")
                    Destinatario_Valido = ponteiro.fetchone ()
                    if not Destinatario_Valido:
                        print ('Usuario não encontrado, verifique se você digitou o CPF corretamente e tente mais uma vez.')
                        print ('\n')
                    else:
                        print (' ')
                        print ('=O destinatario de sua transferencia é o usuario: '+str(Destinatario_Valido[1])+', Usuario de ID '+str(Destinatario_Valido[0])+', CPF ('+str(Destinatario_Valido[2])+').')
                        while True:
                            Confirmacao_Transferencia_1 = str(input ('>Isto esta correto? [Y/N]: '))
                            if Confirmacao_Transferencia_1.lower () == 'y':
                                Destin_Localizado = True
                                break
                            elif Confirmacao_Transferencia_1.lower () == 'n':
                                break
                            else:
                                print ('Por Favor, insira um valor valido.')
                elif Destinatario == 'cancel':
                    print ('Operação cancelada')
                    print ('\n')
                    Escolha_Valida01 = False
                    break
                else:
                    db.commit ()
                    ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_Conta_ID = '"+str(Destinatario)+"';")
                    Destinatario_Valido = ponteiro.fetchone ()
                    if not Destinatario_Valido:
                        print ('Usuario não encontrado, verifique se você digitou o ID corretamente e tente mais uma vez.')
                        print ('\n')
                    else:
                        print ('O destinatario de sua transferencia é o usuario: '+str(Destinatario_Valido[1])+', Usuario de ID '+str(Destinatario_Valido[0])+'.')
                        while True:
                            Confirmacao_Transferencia_1 = str(input('>Isto esta correto? [Y/N]: '))
                            if Confirmacao_Transferencia_1.lower () == 'y':
                                Destin_Localizado = True
                                break
                            elif Confirmacao_Transferencia_1.lower () == 'n':
                                break
                            else:
                                print ('Por Favor, insira um valor valido.')
            if Destin_Localizado == True:
             while Saldo_Suficiente == False:
                db.commit ()
                ponteiro.execute("SELECT Conta_QntAtual FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
                VALOR_Lista = ponteiro.fetchone ()
                VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
                print ('\n')
                print ('#Seu saldo atual é de: R$'+str(VALOR_Conta_Usuario)+'.')
                print ("[Digite 'Cancel' para cancelar]")
                Transferencia_Valor = input (">Insira o valor a ser transferido, use '.' para separar centavos: R$")
                if Transferencia_Valor[0].lower () == 'c':
                    print ('Cancelando Operação.')
                    Escolha_Valida01 = False
                    break
                elif float(Transferencia_Valor) > float(VALOR_Conta_Usuario):
                    print ('[x] - Transferencia Cancelada. Saldo Insuficiente.')
                    break
                elif float(Transferencia_Valor) <= float(VALOR_Conta_Usuario):
                    db.commit ()
                    ponteiro.execute("SELECT Conta_PIN FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
                    PIN_Correto = ponteiro.fetchone ()
                    while PIN_Valido == False:
                      PIN_Tentativa = input('Insira seu PIN: ')
                      if str(PIN_Correto) == "("+PIN_Tentativa+",)":
                        PIN_Valido = True
                        print ('(Atenção!) Você esta transferindo R$'+str(Transferencia_Valor)+' para '+str(Destinatario_Valido[1])+', ID '+str(Destinatario_Valido[0])+'. Seu saldo restante após a transferencia será de R$'+str(float(VALOR_Conta_Usuario)-float(Transferencia_Valor))+'.')
                        Confirmacao_Transferencia_2 = str(input ('>Deseja prosseguir? [Y/N]: '))
                        if Confirmacao_Transferencia_2.lower () == 'y':
                            db.commit ()
                            ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_Conta_ID = '"+str(Destinatario_Valido[0])+"';")
                            Quantia_Atual_Receptor = ponteiro.fetchone()
                            Quantia_Nova_Receptor = float(str(Quantia_Atual_Receptor[5])) + float(Transferencia_Valor)
                            ponteiro.execute("UPDATE tbl_cliente_conta SET Conta_QntAtual = "+str(Quantia_Nova_Receptor)+" WHERE Cliente_Conta_ID ="+str(Destinatario_Valido[0])+";")
                            db.commit ()
                            ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_Conta_ID = '"+str(ID_Usuario[0])+"';")
                            Quantia_Atual_Emissor = ponteiro.fetchone()
                            Quantia_Nova_Emissor = float(str(Quantia_Atual_Emissor[5])) - float (Transferencia_Valor)
                            ponteiro.execute("UPDATE tbl_cliente_conta SET Conta_QntAtual = "+str(Quantia_Nova_Emissor)+" WHERE Cliente_Conta_ID ="+str(ID_Usuario[0])+";")
                            ponteiro.execute("INSERT INTO tbl_transferencia (Transferencia_Qnt, Transferencia_Conta_Emissor_ID, Transferencia_Conta_Receptor_ID, Transferencia_Data) VALUES ('"+str(Transferencia_Valor)+"','"+str(ID_Usuario[0])+" ',' "+str(Destinatario_Valido[0])+" ',' "+str(datetime.datetime.today())+" '); ")
                            db.commit()
                            print ('Transferencia concluida.')
                            print ('####--------------------------------------------------------------------####')
                        elif Confirmacao_Transferencia_2.lower () == 'n':
                            break
                        else:
                            print ('Por Favor, insira um valor valido.')
                      else:
                         print ('[x] - Transferencia Cancelada. PIN Incorreto.')
                         break
                    Saldo_Suficiente = True
                else:
                    print ('Por favor, insira um comando valido.')
            else:
                pass
        elif entrada02 == '2':
            Emprestimo_Valido = False
            print ('=Você selecionou a opção: Emprestimo')
            print (' ')
            ponteiro.execute("SELECT Conta_PIN FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
            PIN_Correto = ponteiro.fetchone ()
            PIN_Validacao = str(input('>Antes de começarmos, insira seu PIN, para confirmarmos sua identidade: '))
            if str(PIN_Correto) == "("+PIN_Validacao+",)":
                print ('=PIN confirmado.')
                print (' ')
                while Emprestimo_Valido == False:
                    Emprestimo_Quantia = float(input('Insira a quantia qual deseja obter: '))
            else:
                print ('[x] - Operação cancelada, PIN incorreto.')
        elif entrada02 == '3':
            print ('\n')
            print ('##EM CONSTRUÇÃO##')
        elif entrada02 == '4':
            print ('\n')
            print ('##EM CONSTRUÇÃO##')
        elif entrada02 == '5':
            Escolha_Valida01 = True
            print ('\n')
            print ('=Saindo da conta.')
            break
        elif entrada02 == '0':
            Escolha_Valida01 = False
            print (' ')
            print ('#----------------#')
            print ('Recarregando...')
            print ('#----------------#')
            print ('\n')
            
        else:
            print('[x] - Por favor, escolha uma operação valida valido.')
else:
    pass

ponteiro.close
db.close
