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
print ('[1] - Já possuo uma conta, quero fazer LogIn.')
print ('[2] - Não possuo uma conta e quero me registrar.')
entrada01 = input ('Escolha uma opção Valida: ')

Login_Valido = False

if entrada01 == '1' or entrada01.lower() == 'login':
    print ('\n')
    print ('>Você selecionou a opção: Login')
    while True:
        Login_Usuario = str(input('=Insira seu CPF: '))
        ponteiro.execute("SELECT Conta_Senha FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
        Usuario_Validacao = ponteiro.fetchall ()
        if not Usuario_Validacao:
            print ('Usuario não encontrado, verifique se você inseriu seu CPF corretamente.')
            print ('\n')
        else:
            Usuario_Senha = str(input('Digite sua senha: '))
            if str(Usuario_Validacao) == "[('"+Usuario_Senha+"',)]":
                print ('Login concluido com sucesso!')
                ponteiro.execute("SELECT Cliente_Nome FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
                Nome_Mostrado = ponteiro.fetchone ()
                print ('\n')
                print ('Bem-Vindo de volta, '+str(Nome_Mostrado[0])+', a sua conta MyBank!') #Perguntar pro alan como tirar as aspas, tanto pra ficar bonito, e pra saber se tem como simplificar o (if str(Usuario_Validacao) == "[('"+Usuario_Senha+"',)]" )
                Login_Valido = True
                break
            else:
                print ('Senha incorreta ou login incorretos.')
elif entrada01 == '2' or entrada01.lower() == 'cadastro':
    print ('\n')
    print ('>Você selecionou a opção: Cadastro.')
    CPF_Unico = False
    PIN_Valido = False
    Senha_Valida = False
    Nome_Valido = False
    Nascimento_Valido = False
    CPF_Inserido = str(input('Antes de começarmos, confirme sua identidade. Insira seu CPF (NNN.NNN.NNN-NN): '))
    if len(CPF_Inserido) == 14:
     ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")
     CPF_Duplicado_Resultados = ponteiro.fetchall ()
     if not CPF_Duplicado_Resultados:
        CPF_Unico = True
        Nascimento_Inserido = input('Indentidade validada. Informe-nos a sua data de nascimento (DD/MM/AAAA): ')
        Nascimento_Formatado = str(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9])+"-"+str(Nascimento_Inserido[3])+str(Nascimento_Inserido[4])+"-"+str(Nascimento_Inserido[0])+str(Nascimento_Inserido[1]))
        if len(Nascimento_Inserido) == 10 and (int(datetime.date.today().year) - int(str(Nascimento_Inserido[6])+str(Nascimento_Inserido[7])+str(Nascimento_Inserido[8])+str(Nascimento_Inserido[9]))) > 13:
            print ("Dados em ordem, preparações para criação de conta finalizadas!")
            print ('\n')
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
                PIN_Escolhido = str(input('=Insira um PIN de segurança de 4 digitos numericos: '))
                if len(PIN_Escolhido) == 4 and str.isdigit(PIN_Escolhido):
                    PIN_Valido = True
                else:
                    print ("[x] - Por favor, insira um PIN adequado feito de 4 digitos numericos! ")
                    print ('\n')
            else:
                pass
            if Nome_Valido == True and PIN_Valido == False: #Tive que colocar que o PIN precisa ser falso aqui pra ele não perguntar a senha duas vezes, sei que fica estranho mas funciona.
                Senha_Escolhida = str(input('=Crie uma senha: '))
                if len(Senha_Escolhida) >= 8:
                    Senha_Valida = True
                else:
                    print ('[x] - Por favor, insira uma senha de pelo menos 8 digitos!')
                    print ('\n')
            else:
                pass

            if Nome_Valido == False:
                Nome_Escolhido = str(input('=Nos informe seu nome de usuario: '))
                if len(Nome_Escolhido) > 0:
                    Nome_Valido = True
                else:
                    print ('[x] - Por favor, insira seu nome!')
                    print ('\n')
            else:
                pass
     else:
         print ('Processo de cadastro não concluido. Por favor, verifique suas informações e tente novamente.')
    else:
       print ('[x] - Por favor, insira um CPF valido com o formato NNN.NNN.NNN-NN. ')
else:
    print ('>Você selecionou uma opção não existente. Por favor insira um valor valido.')

if Login_Valido == True:
    Escolha_Valida01 = False
    ponteiro.execute("SELECT Cliente_Conta_ID FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
    ID_Usuario = ponteiro.fetchone ()
    while Escolha_Valida01 == False:
        db.commit ()
        ponteiro.execute("SELECT Conta_QntAtual FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
        VALOR_Lista = ponteiro.fetchone ()
        VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
        print ('ID do usuario:', str(ID_Usuario[0]))
        print ('Seu atual saldo é de R$'+str(VALOR_Conta_Usuario))
        print ('#-----------------------------------------------#')
        print ('[1] - Transferencia.')
        print ('[2] - Obter Emprestimo.')
        print ('[3] - Pagar Emprestimo.')
        print ('[4] - Opções')
        print ('[5] - LogOff')
        print ('[0] - Recarregar')
        entrada02 = input('Escolha uma operação valida: ')
        if entrada02 == '1':
            Escolha_Valida01 = True
            Destin_Localizado = False
            Saldo_Suficiente = False
            PIN_Valido = False
            print ('>Você selecionou a opção: Transferencia')
            print ('\n')
            while Destin_Localizado == False:
                db.commit ()
                ponteiro.execute("SELECT Conta_QntAtual FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
                VALOR_Lista = ponteiro.fetchone ()
                VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
                print ('________________________________________________')
                print ('Seu saldo atual é de R$'+str(VALOR_Conta_Usuario))
                print ("Por favor, insira ou o CPF (em formato NNN.NNN.NNN-NN), ou ID do destinatario.")
                print ("[Digite 'cancel' para cancelar]")
                Destinatario = input ("= ")
                if len(Destinatario) == 14:
                    db.commit ()
                    ponteiro.execute("SELECT * FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Destinatario)+"';")
                    Destinatario_Valido = ponteiro.fetchone ()
                    if not Destinatario_Valido:
                        print ('Usuario não encontrado, verifique se você digitou o CPF corretamente e tente mais uma vez.')
                        print ('\n')
                    else:
                        print ('O destinatario de sua transferencia é o usuario: '+str(Destinatario_Valido[1])+', Usuario de ID '+str(Destinatario_Valido[0])+', CPF ('+str(Destinatario_Valido[2])+').')
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
                print ('________________________________________________')
                print ('Seu saldo atual é de: R$'+str(VALOR_Conta_Usuario)+'.')
                print ("Insira o valor a ser transferido, use '.' ao invês de virgula para separar centavos. [Digite 'Cancel' para cancelar]")
                Transferencia_Valor = input ('>R$: ')
                if Transferencia_Valor == 'Cancel':
                    print ('Cancelando Operação.')
                    Escolha_Valida01 = False
                elif float(Transferencia_Valor) > float(VALOR_Conta_Usuario):
                    print ('Atenção: Transferencia Cancelada.')
                    print ('Motivo: Saldo Insuficiente.')
                    break
                elif float(Transferencia_Valor) <= float(VALOR_Conta_Usuario):
                    db.commit ()
                    ponteiro.execute("SELECT Conta_PIN FROM tbl_cliente_conta WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
                    PIN_Correto = ponteiro.fetchone ()
                    while PIN_Valido == False:
                      PIN_Tentativa = input('Insira seu PIN: ')
                      if str(PIN_Correto) == "("+PIN_Tentativa+",)":
                        PIN_Valido = True
                        print ('Atenção. Você esta transferindo R$'+str(Transferencia_Valor)+' para '+str(Destinatario_Valido[1])+', ID '+str(Destinatario_Valido[0])+'. Seu saldo restante após a transferencia será de'+str(float(VALOR_Conta_Usuario)-float(Transferencia_Valor))+'.')
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
                        elif Confirmacao_Transferencia_2.lower () == 'n':
                            break
                        else:
                            print ('Por Favor, insira um valor valido.')
                      else:
                         print ('Atenção: Transferencia Cancelada.')
                         print ('Motivo: segurança, PIN Incorreto.')
                    Saldo_Suficiente = True
                else:
                    print ('Por favor, insira um comando valido.')
            else:
                pass
        elif entrada02 == '2':
            print ('\n')
            print ('##EM CONSTRUÇÃO##')
        elif entrada02 == '3':
            print ('\n')
            print ('##EM CONSTRUÇÃO##')
        elif entrada02 == '4':
            print ('\n')
            print ('##EM CONSTRUÇÃO##')
        elif entrada02 == '5':
            Escolha_Valida01 = True
            print ('\n')
            print ('Saindo da conta.')
            break
        elif entrada02 == '0':
            Escolha_Valida01 = False
            print ('Recarregando...')
            print ('\n')
            
        else:
            print('Por favor, escolha uma operação valida valido.')
else:
    pass

ponteiro.close
db.close
