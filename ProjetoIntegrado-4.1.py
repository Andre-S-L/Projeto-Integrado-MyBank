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

while True:
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
            print ('\n')
            break
        else:
          ponteiro.execute("SELECT Cliente_ID FROM tbl_cliente WHERE Cliente_CPF = '"+str(Login_Usuario)+"';")
          ID_Usuario = ponteiro.fetchone ()
          if not ID_Usuario:
            print ('[x] - Usuario não encontrado, verifique se você inseriu seu CPF corretamente.')
            print ('\n')
          else:
            ponteiro.execute("SELECT Conta_Senha FROM tbl_conta WHERE fk_Conta_Cliente_ID ='"+str(ID_Usuario[0])+"';")
            Usuario_Validacao = ponteiro.fetchall ()
            Usuario_Senha = str(input('>Digite sua senha: '))
            if Usuario_Senha.lower () == 'cancel':
                print ('Cancelando Login.')
                print ('####--------------------------------------------------------------------####')
                break
            elif str(Usuario_Validacao) == "[('"+Usuario_Senha+"',)]":
                print ('=Login concluido com sucesso!')
                print ('####--------------------------------------------------------------------####')
                ponteiro.execute("SELECT Cliente_Nome FROM tbl_cliente WHERE Cliente_ID = '"+str(ID_Usuario[0])+"';")
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
    print ('Antes de começarmos, confirme sua identidade.')
    CPF_Inserido = str(input('>Insira seu CPF no formato(NNN.NNN.NNN-NN): '))
    Loop_Cad_1 = True
    while Loop_Cad_1 == True:
      if CPF_Inserido[0].lower () == 'c':
         print ('Cancelando Cadastro...')
         break
      elif len(CPF_Inserido) == 14:
       ponteiro.execute("SELECT * FROM tbl_cliente WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")
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
                print ('Bem-Vindo(a) ao MyBank', str(Nome_Escolhido))
                print ('####--------------------------------------------------------------------####')
                print ('\n')
                ponteiro.execute("INSERT INTO tbl_cliente (Cliente_Nome, Cliente_CPF, Cliente_Nasc, Cliente_Admin, Cliente_Registro) VALUES ('"+str(Nome_Escolhido)+"', '"+str(CPF_Inserido)+"', '"+str(Nascimento_Formatado)+"', '0', '"+str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'))+"');")
                db.commit()
                ponteiro.execute("SELECT Cliente_ID FROM tbl_cliente WHERE Cliente_CPF = '"+str(CPF_Inserido)+"';")   
                ID_Cliente_Conta = ponteiro.fetchone ()
                ponteiro.execute("INSERT INTO tbl_conta (Conta_Senha, Conta_Pin, Conta_QntAtual, Conta_Ativa, fk_Conta_Cliente_ID) VALUES ('"+str(Senha_Escolhida)+"', '"+str(PIN_Escolhido)+"', '0.00', '1', '"+str(ID_Cliente_Conta[0])+"');")
                db.commit ()
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
    while Escolha_Valida01 == False:
        db.commit ()
        ponteiro.execute("SELECT Conta_QntAtual FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
        VALOR_Lista = ponteiro.fetchone ()
        VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
        ponteiro.execute("SELECT * FROM tbl_emprestimo WHERE Emprestimo_Ativo = 1 AND fk_Emprestimo_Conta_ID = "+str(ID_Usuario[0])+";")
        Emprestimo_Calculo = ponteiro.fetchone ()
        if not Emprestimo_Calculo:
            pass
        else:
            Tempo_Ativo = (datetime.date.today() - Emprestimo_Calculo[4])
            J = (float(Emprestimo_Calculo[1]) * float(Emprestimo_Calculo[2]/100) * Tempo_Ativo.days//28)
            Emprestimo_Valor_Atualizado = (float(Emprestimo_Calculo[1]) + J)
            ponteiro.execute("UPDATE tbl_emprestimo SET Emprestimo_ValorAPagar = '"+str(Emprestimo_Valor_Atualizado)+"' WHERE Emprestimo_ID = "+str(Emprestimo_Calculo[0])+";")
            db.commit()
            pass
        print ('#ID do usuario:', str(ID_Usuario[0]))
        print ('#Seu atual saldo é de R$'+str(VALOR_Conta_Usuario))
        if not Emprestimo_Calculo:
            pass
        else:
            print ('#Você atualmente possui uma pendencia ativa de R$'+str(Emprestimo_Calculo[7])+', com uma taxa de aumento de', str(Emprestimo_Calculo[2])+'% a cada 28 dias.')
        print (' ')
        print ('Selecione uma opção abaixo:')
        print ('[1] - Transferencia.')
        print ('[2] - Obter Emprestimo.')
        print ('[3] - Pagar Emprestimo.')
        print ('[4] - Configurações')
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
                ponteiro.execute("SELECT Conta_QntAtual FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
                VALOR_Lista = ponteiro.fetchone ()
                VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
                print (' ')
                print ('#Seu saldo atual é de R$'+str(VALOR_Conta_Usuario))
                print ("<Digite 'cancel' para cancelar>")
                Destinatario = input (">Por favor, insira ou o CPF (em formato NNN.NNN.NNN-NN), ou ID do destinatario: ")
                if Destinatario == str(ID_Usuario[0]) or Destinatario == Login_Usuario:
                    print (' ')
                    print ('[x] - Transferencia Cancelada. Não é possivel transferir um valor para si mesmo.')
                    print ('\n')
                    Escolha_Valida01 = False
                    break
                elif len(Destinatario) == 14:
                    db.commit ()
                    ponteiro.execute("SELECT * FROM tbl_cliente WHERE Cliente_CPF = '"+str(Destinatario)+"';")
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
                    ponteiro.execute("SELECT * FROM tbl_cliente WHERE Cliente_ID = '"+str(Destinatario)+"';")
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
                ponteiro.execute("SELECT Conta_QntAtual FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
                VALOR_Lista = ponteiro.fetchone ()
                VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
                print ('\n')
                print ('#Seu saldo atual é de: R$'+str(VALOR_Conta_Usuario)+'.')
                print ("<Digite 'Cancel' para cancelar>")
                Transferencia_Valor = input (">Insira o valor a ser transferido, use '.' para separar centavos: R$")
                if Transferencia_Valor[0].lower () == 'c':
                    print ('Cancelando Operação.')
                    Escolha_Valida01 = False
                    break
                elif not str.isdigit(Transferencia_Valor) and not Transferencia_Valor[-3] == '.':
                    print ('[x] - Transferencia Cancelada. Insira um valor valido')
                    print ('\t')
                    Escolha_Valida01 = False
                    break
                elif float(Transferencia_Valor) > float(VALOR_Conta_Usuario):
                    print ('[x] - Transferencia Cancelada. Saldo Insuficiente.')
                    print ('\t')
                    Escolha_Valida01 = False
                    break
                elif float(Transferencia_Valor) <= float(VALOR_Conta_Usuario):
                    db.commit ()
                    ponteiro.execute("SELECT Conta_PIN FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
                    PIN_Correto = ponteiro.fetchone ()
                    while PIN_Valido == False:
                      PIN_Tentativa = input('Insira seu PIN: ')
                      if str(PIN_Correto) == "('"+PIN_Tentativa+"',)":
                        PIN_Valido = True
                        print ('(Atenção!) Você esta transferindo R$'+str(Transferencia_Valor)+' para '+str(Destinatario_Valido[1])+', ID '+str(Destinatario_Valido[0])+'. Seu saldo restante após a transferencia será de R$'+str(float(VALOR_Conta_Usuario)-float(Transferencia_Valor))+'.')
                        Confirmacao_Transferencia_2 = str(input ('>Deseja prosseguir? [Y/N]: '))
                        if Confirmacao_Transferencia_2.lower () == 'y':
                            db.commit ()
                            ponteiro.execute("SELECT * FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(Destinatario_Valido[0])+"';")
                            Quantia_Atual_Receptor = ponteiro.fetchone()
                            Quantia_Nova_Receptor = float(str(Quantia_Atual_Receptor[3])) + float(Transferencia_Valor)
                            ponteiro.execute("UPDATE tbl_conta SET Conta_QntAtual = "+str(Quantia_Nova_Receptor)+" WHERE fk_Conta_Cliente_ID ="+str(Destinatario_Valido[0])+";")
                            db.commit ()
                            ponteiro.execute("SELECT * FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
                            Quantia_Atual_Emissor = ponteiro.fetchone()
                            Quantia_Nova_Emissor = float(str(Quantia_Atual_Emissor[3])) - float (Transferencia_Valor)
                            ponteiro.execute("UPDATE tbl_conta SET Conta_QntAtual = "+str(Quantia_Nova_Emissor)+" WHERE fk_Conta_Cliente_ID ="+str(ID_Usuario[0])+";")
                            ponteiro.execute("INSERT INTO tbl_transferencia (Transferencia_Qnt, fk_Transferencia_Conta_Emissor_ID, fk_Transferencia_Conta_Receptor_ID, Transferencia_Data) VALUES ('"+str(Transferencia_Valor)+"','"+str(ID_Usuario[0])+"','"+str(Destinatario_Valido[0])+"','"+str(datetime.datetime.today())+"');")
                            db.commit ()
                            Escolha_Valida01 = False
                            print ('Transferencia concluida.')
                            print ('####--------------------------------------------------------------------####')
                            print ('\n')
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
            Escolha_Valida01 = True
            Emprestimo_Valido = False
            print ('=Você selecionou a opção: Emprestimo')
            if not Emprestimo_Calculo:
             print (' ')
             ponteiro.execute("SELECT Conta_Senha FROM tbl_conta WHERE fk_Conta_Cliente_ID = "+str(ID_Usuario[0])+";")
             Senha_Correto = ponteiro.fetchone ()
             print ('Antes de começar, valide sua identidade')
             Senha_Validacao = str(input('>Insira sua senha novamente: '))
             if str(Senha_Correto) == "('"+Senha_Validacao+"',)":
                print ('=Identidade Confirmado.')
                print (' ')
                print ("<Caso deseje, digite 'Cancel' para cancelar a operação.>")
                while Emprestimo_Valido == False:
                    Emprestimo_Quantia = input(">Insira a quantia desejada, use '.' para identificar centavos: R$")
                    print ("Digite 'Cancel' para sair.>")
                    if Emprestimo_Quantia[0].lower () == 'c':
                        print ('Cancelando Operação... ')
                        Escolha_Valida01 = False
                        Emprestimo_Valido = False
                        break
                    elif not str.isdigit(Emprestimo_Quantia) and not Emprestimo_Quantia[-3] == '.' or float(Emprestimo_Quantia) <= 0:
                        print ('[x]- Valor invalido. Por favor, insira um valor possivel.')
                        print ('\t')
                    elif float(Emprestimo_Quantia) > 0:
                        print (' ')
                        print ('=Você pretende obter um emprestimo no valor de R$'+str(Emprestimo_Quantia)+'.')
                        ponteiro.execute ("SELECT Agencia_Dinheiro_Total, Agencia_Juros_Atual, Agencia_Devolucao_Prazo_Maximo FROM tbl_agencia WHERE Agencia_ID = 1;")
                        Info_Agencia = ponteiro.fetchone ()
                        print ("(*IMPORTANTE!): Você receberá um emprestimo de "+str(Emprestimo_Quantia)+" com uma taxa de aumento de "+str(Info_Agencia[1])+"% na hora da devolução a cada 28 dias.")
                        print ('(*IMPORTANTE!): O modelo atual MyBank permite um prazo maximo de devolução em até '+str(Info_Agencia[2])+' meses. ')
                        print ('(*IMPORTANTE!): A falha em devolver no prazo estipulado, ou anteriormente, pode levar a repercussões legais na falta de justificativa.')
                        while True:
                            print (' ')
                            Confirmacao_Emprestimo_1 = input('>Deseja prosseguir? [Y/N] ')
                            if Confirmacao_Emprestimo_1.lower () == 'y':
                                ponteiro.execute("SELECT Conta_PIN FROM tbl_conta WHERE fk_Conta_Cliente_ID = "+str(ID_Usuario[0])+";")
                                PIN_Correto = ponteiro.fetchone ()
                                Confirmacao_Emprestimo_2 = input('>Digite seu PIN de segurança: ')
                                if Confirmacao_Emprestimo_2[0].lower () == 'c':
                                    print ('Cancelando Operação...')
                                    print ('####--------------------------------------------------------------------####')
                                    print ('\n')
                                    Escolha_Valida01 = False
                                    Emprestimo_Valido = True
                                    break
                                elif Confirmacao_Emprestimo_2 == str(PIN_Correto[0]):
                                    db.commit()
                                    ponteiro.execute("SELECT Conta_QntAtual FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
                                    Antigo_Valor_Quantia = ponteiro.fetchone ()
                                    Novo_Valor_Quantia = float(Antigo_Valor_Quantia[0]) + float(Emprestimo_Quantia)
                                    ponteiro.execute("INSERT INTO tbl_emprestimo (Emprestimo_Valor, Emprestimo_Taxa_Juros, Emprestimo_Ativo, Emprestimo_Data_Obti, Emprestimo_ValorAPagar, fk_Emprestimo_Conta_ID) VALUES ('"+str(Emprestimo_Quantia)+"', '"+str(Info_Agencia[1])+"', '1', '"+str(datetime.datetime.today())+"', '"+str(Emprestimo_Quantia)+"', '"+str(ID_Usuario[0])+"')")
                                    ponteiro.execute("UPDATE tbl_conta SET Conta_QntAtual = "+str(Novo_Valor_Quantia)+" WHERE fk_Conta_Cliente_ID ="+str(ID_Usuario[0])+";")
                                    db.commit
                                    Agencia_Novo_Valor = float(str(Info_Agencia[0])) - float(Emprestimo_Quantia)
                                    ponteiro.execute("UPDATE tbl_agencia SET Agencia_Dinheiro_Total = '"+str(Agencia_Novo_Valor)+"' WHERE Agencia_ID = 1;")
                                    db.commit
                                    print ('Operação Concluida!')
                                    print ('####--------------------------------------------------------------------####')
                                    print ('\n')
                                    Escolha_Valida01 = False
                                    Emprestimo_Valido = True
                                    break
                                else:
                                    print ('[x] - PIN Incorreto, cancelando operação')
                                    print ('####--------------------------------------------------------------------####')
                                    print ('\n')
                                    Escolha_Valida01 = False
                                    Emprestimo_Valido = True
                                    break
                            elif Confirmacao_Emprestimo_1.lower () == 'n':
                                print (' ')
                                break
                            else:
                                print ('[x] - Digite um valor valido, Y ou N.')
                    else:
                        print ('[x] - Sinto muito, não entendi seu comando, por favor tente novamente.')
                        print ("você pode digitar 'cancel' para sair.")
             else:
                print ('[x] - Operação cancelada, Senha Incorreto.')
                print ('\t')
            else:
                print('\t')
                print('[x] - Operação não autorizada. Atenção, não e possivel obter um emprestimo enquanto outro esta ativo.')
                print('\n')
        elif entrada02 == '3':
            Escolha_Valida01 = True
            print ('=Você selecionou a opção: Devolução de Emprestimo')
            print ("<Caso deseje, digite 'Cancel' para cancelar a operação>")
            print (' ')
            ponteiro.execute("SELECT * FROM tbl_emprestimo WHERE Emprestimo_Ativo = 1 AND fk_Emprestimo_Conta_ID = "+str(ID_Usuario[0])+";")
            Emprestimo_Existente = ponteiro.fetchone ()
            if not Emprestimo_Existente:
                print ('[x] - Você não possui emprestimos ativos.')
                Escolha_Valida01 = False
                print ('\t')
            else:
                print ("Você atualmente possui um emprestimo no valor de R$"+str(Emprestimo_Existente[7])+".")
                db.commit ()
                ponteiro.execute("SELECT Conta_QntAtual FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
                Quantia_Atual = ponteiro.fetchone ()
                print ("Seu saldo atual e de R$"+str(Quantia_Atual[0])+".")
                Quantia_Nova = (float(str(Quantia_Atual[0])) - float(str(Emprestimo_Existente[7])))
                print ("Você ficará com apenas R$"+str(Quantia_Nova)+".")
                Devolucao_Loop = True
                while Devolucao_Loop == True:
                    Confirmacao_Devolucao1 = input(">Você deseja efetuar a devoluçaõ do emprestimo? [Y/N] ")
                    if Confirmacao_Devolucao1[0].lower() == 'n' or Confirmacao_Devolucao1[0].lower() == 'c':
                        print ('Cancelando operação... ')
                        print ('####--------------------------------------------------------------------####')
                        print ('\n')
                        Escolha_Valida01 = False
                        break
                    elif Confirmacao_Devolucao1[0].lower() == 'y':
                      while True:
                            if float(str(Emprestimo_Existente[7])) <= float(str(Quantia_Atual[0])):
                                ponteiro.execute("SELECT Conta_PIN FROM tbl_conta WHERE fk_Conta_Cliente_ID = "+str(ID_Usuario[0])+";")
                                PIN_Correto = ponteiro.fetchone ()
                                Confirmacao_Devolucao2 = input (">Digite seu PIN de segurança: ")
                                if Confirmacao_Devolucao2[0].lower() == 'c':
                                    print ('Cancelando Operação... ')
                                    Escolha_Valida01 = False
                                    Devolucao_Loop = False
                                    break
                                elif Confirmacao_Devolucao2 == str(PIN_Correto[0]):
                                    Tempo_Corrido = str(datetime.date.today() - Emprestimo_Existente[4])
                                    db.commit
                                    ponteiro.execute("UPDATE tbl_conta SET Conta_QntAtual = "+str(Quantia_Nova)+" WHERE fk_Conta_Cliente_ID ="+str(ID_Usuario[0])+";")
                                    ponteiro.execute("UPDATE tbl_emprestimo SET Emprestimo_Ativo = '0', Emprestimo_Data_Devol = '"+str(datetime.date.today())+"', Emprestimo_Tempo_Corrido_Dias = '"+str(Tempo_Corrido[0])+"' WHERE Emprestimo_ID = '"+str(Emprestimo_Existente[0])+"';")
                                    db.commit
                                    ponteiro.execute("SELECT Agencia_Dinheiro_Total FROM tbl_agencia WHERE Agencia_ID = 1;")
                                    Agencia_Velha_Quantia = ponteiro.fetchone()
                                    Agencia_Nova_Quantia = Agencia_Velha_Quantia[0] + Emprestimo_Existente[7]
                                    ponteiro.execute("UPDATE tbl_agencia SET Agencia_Dinheiro_Total = '"+str(Agencia_Nova_Quantia)+"' WHERE Agencia_ID = 1;")
                                    db.commit
                                    print ('Emprestimo Pago com Sucesso!')
                                    print ('####--------------------------------------------------------------------####')
                                    print ('\n')
                                    Devolucao_Loop = False
                                    Escolha_Valida01 = False
                                    break
                                else:
                                    print ('[x] - PIN Invalido.')
                            else:
                                print (' ')
                                print ('[x] - Devolução impossivel. Saldo insuficiente.')
                                print ('\n')
                                Devolucao_Loop = False
                                Escolha_Valida01 = False
                                break
                    else:
                        print ('[x] - Comando invalido.')
        elif entrada02 == '4':
            print ('\n')
            Escolha_Valida01 = True
            db.commit()
            ponteiro.execute("SELECT Conta_PIN FROM tbl_conta WHERE fk_Conta_Cliente_ID = "+str(ID_Usuario[0])+";")
            PIN_Validacao = ponteiro.fetchone()
            print ('=Você selecionou a opção: Configurações')
            while True:
                print ('Selecione uma opção valida abaixo:')
                print ('[1] - Alterar nome.')
                print ('[2] - Alterar senha.')
                print ('[3] - Alterar PIN.')
                print ('[4] - Deletar conta.')
                print ('[5] - Cancelar')
                entrada03 = input('>Escolha uma operação valida: ')
                print ('\t')
                if entrada03[0] == '1':
                    print ('=Você escolheu a opção: Alterar nome.')
                    print ('\t')
                    print ('Confirme sua identidade')
                    Confirmacao_Alteracao1 = input('Insira seu CPF: ')
                    Confirmacao_Alteracao2 = input('Insira sua senha: ')
                    if Confirmacao_Alteracao1 == str(Login_Usuario) and "[('"+Confirmacao_Alteracao2+"',)]" == str(Usuario_Validacao):
                        Mudanca = input ('Identidade validada! Insira um nome novo: ')
                        if Mudanca.lower() == 'cancel':
                            print ('Cancelando alteração...')
                        elif Mudanca.isdigit() or len(Mudanca) < 2:
                            print ('\t')
                            print('[x] - Operação cancelada. Nome invalido.')
                            print ('\t')
                        elif Mudanca == Nome_Mostrado[0]:
                            print ('\t')
                            print ('[x] - Operação cancelada. O novo nome não pode ser o mesmo que o anterior.')
                            print ('\t')
                        else:
                            ponteiro.execute("UPDATE tbl_cliente SET Cliente_Nome = '"+Mudanca+"' WHERE Cliente_ID = "+str(ID_Usuario[0])+";")
                            db.commit()
                            print ('Alteração feita com sucesso! Ficamos feliz em te ter como cliente', Mudanca+'!')
                            print ('####--------------------------------------------------------------------####')
                            print ('\n')
                            break
                    else:
                        print ('[x] - CPF ou Senha incorretos, alteração não autorizada')
                        print ('\t')
                elif entrada03[0] == '2':
                    print ('=Você escolheu a opção: Alterar senha.')
                    print ('\t')
                    print ('Confirme sua identidade')
                    Confirmacao_Alteracao1 = input('Insira seu CPF: ')
                    Confirmacao_Alteracao2 = input('Insira seu PIN: ')
                    if Confirmacao_Alteracao1 == str(Login_Usuario) and Confirmacao_Alteracao2 == PIN_Validacao[0]:
                        Mudanca = input ('Identidade validada! Insira sua nova senha, com no minimo 8 caracteres: ')
                        if Mudanca.lower() == 'cancel':
                            print ('Cancelando alteração...')
                        elif Mudanca == "[('"+Usuario_Senha+"',)]":
                            print ('\t')
                            print ('[x] - Operação cancelada. Nova senha não pode ser a mesma que a anterior.')
                            print ('\t')
                        elif len(Mudanca) < 8:
                            print ('\t')
                            print ('[x] - Operação cancelada. Sua senha deve conter no minimo 8 caracteres.')
                            print ('\t')
                        else:
                            ponteiro.execute("UPDATE tbl_conta SET Conta_Senha = '"+str(Mudanca)+"' WHERE fk_Conta_Cliente_ID = "+str(ID_Usuario[0])+";")
                            db.commit()
                            print ('Alteração feita com sucesso! Você já pode fazer Login usando sua nova senha.')
                            print ('####--------------------------------------------------------------------####')
                            print ('\n')
                            break
                    else:
                        print ('[x] - CPF ou PIN incorretos, alteração não autorizada')
                        print ('\t')
                elif entrada03[0] == '3':
                    print ('=Você escolheu a opção: Alterar PIN.')
                    print ('\t')
                    print ('Confirme sua identidade')
                    Confirmacao_Alteracao1 = input('Insira seu CPF: ')
                    Confirmacao_Alteracao2 = input('Insira sua senha: ')
                    if Confirmacao_Alteracao1 == str(Login_Usuario) and "[('"+Confirmacao_Alteracao2+"',)]" == str(Usuario_Validacao):
                        Mudanca = input ('Identidade validada! Insira um PIN: ')
                        if Mudanca.lower() == 'cancel':
                            print ('Cancelando alteração...')
                        elif not Mudanca.isdigit() or len(Mudanca) != 4:
                            print ('\t')
                            print('[x] - Operação cancelada. PIN invalido.')
                            print ('\t')
                        elif Mudanca == PIN_Validacao[0]:
                            print ('\t')
                            print ('[x] - Operação cancelada. O novo PIN não pode ser o mesmo que o anterior.')
                            print ('\t')
                        else:
                            ponteiro.execute("UPDATE tbl_conta SET Conta_PIN = '"+Mudanca+"' WHERE fk_Conta_Cliente_ID = "+str(ID_Usuario[0])+";")
                            db.commit()
                            print ('Alteração feita com sucesso! Lembre-se bem do seu novo PIN!')
                            print ('####--------------------------------------------------------------------####')
                            print ('\n')
                            break
                    else:
                        print ('[x] - CPF ou Senha incorretos, alteração não autorizada')
                        print ('\t')
                elif entrada03[0] == '4':
                    if not Emprestimo_Calculo:
                        print ('\t')
                        print ('(ATENÇÃO!) =Você escolheu a opção: Deletar Conta. Essa ação é irreversivel caso você decida prosseguir!')
                        print ('Confirme sua identidade')
                        Confirmacao_Alteracao1 = input('Insira seu CPF: ')
                        Confirmacao_Alteracao2 = input('Insira sua senha: ')
                        if Confirmacao_Alteracao1 == str(Login_Usuario) and "[('"+Confirmacao_Alteracao2+"',)]" == str(Usuario_Validacao):
                            print ('(ATENÇÃO!) Novamente: Você esta prestes a deletar sua conta. Tem certeza que deseja prosseguir?')
                            Confirmacao_Alteracao3 = input ('Insira seu PIN caso tenha certeza.')
                            if Confirmacao_Alteracao3 == PIN_Validacao[0]:
                                while True:
                                    print ('Ao digitar <Confirmo> você esta concordando que:')
                                    print ('1. Você esta ciente de que o seu dinheiro atualmente guardado no MyBank se tornará inacessivel para você, mesmo que digite sua senha ou CPF corretamnete')
                                    print ('2. Você não será mais capaz de usar sua conta MyBank para fazer ou receber transferencia bancarias.')
                                    print ('3. O MyBank não se sujeita a nenhuma obrigação de restaurar sua conta a um estado anterior funcional.')
                                    Confirmacao_Final = input ('Confirma? ')
                                    if Confirmacao_Final.lower()[0] == 'c':
                                        print ('Sua conta MyBank foi excluida. Foi bom o(a) ter como cliente, '+str(Nome_Mostrado[0])+'Esperamos que um dia possamos trabalhar juntos novamente.')
                                        db.commit ()
                                        ponteiro.execute("SELECT Conta_QntAtual FROM tbl_conta WHERE fk_Conta_Cliente_ID = '"+str(ID_Usuario[0])+"';")
                                        ponteiro.fetchone
                                        VALOR_Lista = ponteiro.fetchone ()
                                        VALOR_Conta_Usuario = float(str(VALOR_Lista[0]))
                                        db.commit()
                                        ponteiro.execute ("SELECT Agencia_Dinheiro_Total FROM tbl_agencia WHERE Agencia_ID = 1;")
                                        Info_Agencia = ponteiro.fetchone ()
                                        Agencia_Novo_Valor = VALOR_Conta_Usuario + float(str(Info_Agencia[0]))
                                        ponteiro.execute("UPDATE tbl_agencia SET Agencia_Dinheiro_Total = '"+str(Agencia_Novo_Valor)+"' WHERE Agencia_ID = 1;")
                                        db.commit
                                        ponteiro.execute("DELETE FROM tbl_conta WHERE fk_Conta_Cliente_ID = "+str(ID_Usuario[0])+";")
                                    else:
                                        print ('[x] - Exclusão da conta cancelada.')
                                        break
                            else:
                                Escolha_Valida01 = False
                                Login_Valido = False
                                print ('[x] - CPF ou Senha Incorretos em operação delicada. Fazendo LogOff por questoes de segurança.')
                                print ('####--------------------------------------------------------------------####')
                                print ('\n')
                                break
                        else:
                            Escolha_Valida01 = False
                            Login_Valido = False
                            print ('[x] - CPF ou Senha Incorretos em operação delicada. Fazendo LogOff por questoes de segurança.')
                            print ('####--------------------------------------------------------------------####')
                            print ('\n')
                            break
                    else:
                        print ('[x] - ATENÇÃO! Você atualmente possui uma pendencia ativa de R$'+str(Emprestimo_Calculo[7])+', Não e possivel apagar sua conta enquanto há um emprestimo ativo.')
                elif entrada03[0] == '5':
                    break
                else:
                    print ('[x] - Por favor, escolha uma operação valida valido.')
        elif entrada02 == '5':
            Escolha_Valida01 = True
            print ('\t')
            print ('=Saindo da conta.')
            print ('\n')
            Login_Valido = False
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
