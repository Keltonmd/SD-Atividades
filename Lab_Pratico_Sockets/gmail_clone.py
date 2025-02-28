import socket
import json
import os
import time
import bcrypt

def limpar_Tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def interface_Principal(tipo):
    login = "1) Apontar Servidor\n2) Cadastrar Conta\n3) Acessar E-mail\n0) Sair\nDigite a opçao: "
    home = "4) Enviar E-mail\n5) Receber E-mails\n6) Logout\nDigite a opçao: "
    if tipo == "login":
        while True:
            try:
                opc = int(input(login))
                if opc >= 0 and opc <= 3:
                    return opc
                else:
                    limpar_Tela()
                    print("Opção invalida")
                    time.sleep(2)
                    limpar_Tela()
            except ValueError:
                limpar_Tela()
                print("Erro: Digite um número inteiro válido.")
                time.sleep(2)
                limpar_Tela()

    if tipo == "home":
        while True:
            try:
                opc = int(input(home))
                if opc > 3 and opc <= 6:
                    return opc
                else:
                    limpar_Tela()
                    print("Opção invalida")
                    time.sleep(2)
                    limpar_Tela()
            except ValueError:
                limpar_Tela()
                print("Erro: Digite um número inteiro válido.")
                time.sleep(2)
                limpar_Tela()

def interface_Conxecao():
    global conexao

    if conexao:
        verf = input("Você já esta conectado a um servidor! Tem certeza que quer conectar outro? (Digite 0 para sair ou qualquer outra tecla para continuar):  ")

        if verf == '0':
            limpar_Tela()
            return

    while True:
        try:
            endereco = input("Digite o Endereco ou IP do Servidor: ")
            socket.inet_aton(endereco)
        except socket.error:
            try:
                socket.gethostbyname(endereco)
            except socket.error:
                print("Endereco não é valido!")
                continue

        try:
            porta = int(input("Digite a porta de conexao do Servidor: "))
            if 1 > porta and porta > 65535:
                print("Porta não é valida!")
                continue
        except Exception as e:
            print("Porta não é valida!")
            continue

        conexao = conectar_Servidor(endereco, porta)
        if conexao:
            print("Serviço Disponível!")
            time.sleep(2)
            limpar_Tela()
            break
        else:
            print("Conexão falhou!")

def desconectar_servidor():
    global cliente_Conexao
    if cliente_Conexao:
        try:
            cliente_Conexao.close()
            print("Conexão encerrada com o servidor.")
            time.sleep(2)
            limpar_Tela()
        except Exception as e:
            print(f"Erro ao desconectar: {e}")
            time.sleep(2)
            limpar_Tela()
        finally:
            cliente_Conexao = None 

def conectar_Servidor(endereco, porta):
    global cliente_Conexao
    ENDPOINT = (endereco, porta)
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente_socket.connect(ENDPOINT)
        cliente_Conexao = cliente_socket
    except Exception as e:
        print(f"Erro ao conectar no servidor: {e}! Tente novamente.")
        return False
    
    return teste_conexao()

def teste_conexao():
    global cliente_Conexao
    try:
        #enviar mensagem teste
        msg = json.dumps({"msgTeste": "Hellow"})
        cliente_Conexao.send(msg.encode())
        #receber mensagem de teste
        mensagem_servidor = json.loads(cliente_Conexao.recv(1024).decode())
        return mensagem_servidor['msgTeste'] == "Hellow"
    except Exception as e:
        print(f"Erro ao conectar no servidor: {e}! Tente novamente.")
        return False
    
def cadastrar_conta():
    global cliente_Conexao

    while True:
        while True:
            try:
                nome = input("Digite seu Nome Completo: ")
                partes = nome.split()
                if len(partes) >= 2 and all(len(palavra) >= 2 for palavra in partes):
                    break
                else:
                    print("Nome invalido! Digite pelo menos o nome e sobrenome!")
                    time.sleep(2)
                    limpar_Tela()
            except Exception:
                print("Erro! Tente Novamente!")
                time.sleep(2)
                limpar_Tela()
        
        while True:
            try:
                username = input("Digite seu Username sem espaços: ").strip()

                #Verifica se não tem espaço
                if " " in username:
                    print("O username não pode conter espaços!")
                    time.sleep(2)
                    limpar_Tela()
                    continue     

                msg = json.dumps({'tipo': 'Veri_User', 'username': username})

                #Envia username para verificao
                cliente_Conexao.send(msg.encode()+b'\n')

                #Recebe verificacao
                resposta = json.loads(cliente_Conexao.recv(1024).decode())

                if resposta['validacao'] == 'False':
                    break
                else:
                    if resposta['validacao'] == 'True':
                        print("Username já existe!")
                        time.sleep(2)
                        limpar_Tela()
                    else:
                        print("Username invalido!") 
                        time.sleep(2)
                        limpar_Tela()

            except json.JSONDecodeError:
                print("Erro: Resposta inválida do servidor.")
                time.sleep(2)
                limpar_Tela()
            except ConnectionError:
                print("Erro: Conexão perdida com o servidor.")
                time.sleep(2)
                limpar_Tela()
                return
            except Exception as e:
                print(f"Erro inesperado: {e}")
                time.sleep(2)
                limpar_Tela()

        while True:
            try:
                senha = input("Digite sua Senha: ").strip()

                if len(senha) < 6:
                    print("Erro: A senha deve ter pelo menos 6 caracteres.")
                    time.sleep(2)
                    limpar_Tela()
                    continue
                
                salt = bcrypt.gensalt()
                senha_hash = bcrypt.hashpw(senha.encode(), salt).decode()
                break

            except Exception as e:
                print(f"Erro inesperado ao processar a senha: {e}")
                time.sleep(2)
                limpar_Tela()
                continue
        
        #Enviando dados
        try:
            msg = json.dumps({'Nome': nome, 'Username': username, 'Senha': senha_hash, 'tipo': 'Cadastro'})
            cliente_Conexao.send(msg.encode()+b'\n')
            resposta = json.loads(cliente_Conexao.recv(1024).decode())
            if resposta['notificacao'] == 'True':
                print('Cadastro realizado com Sucesso!')
                time.sleep(2)
                limpar_Tela()
                break

            print("Cadastro não realizado!")
            time.sleep(2)
            limpar_Tela()
            continue
        except Exception as e:
            print(f"Erro ao enviar os dados ao servidor: {e}")
            time.sleep(2)
            limpar_Tela()
    
def acessar_conta():
    global cliente_Conexao, tipo, username

    while True:   
        while True:
            try:
                userName = input("Digite seu Username sem espaços: ").strip()

                #Verifica se não tem espaço
                if " " in userName:
                    print("O username não pode conter espaços!")
                    time.sleep(2)
                    limpar_Tela()
                    continue     

                break

            except json.JSONDecodeError:
                print("Erro: Resposta inválida do servidor.")
                time.sleep(2)
                limpar_Tela()
            except ConnectionError:
                print("Erro: Conexão perdida com o servidor.")
                time.sleep(2)
                limpar_Tela()
                return
            except Exception as e:
                print(f"Erro inesperado: {e}")
                time.sleep(2)
                limpar_Tela()

        while True:
            try:
                senha = input("Digite sua Senha: ").strip()

                if len(senha) < 6:
                    print("Erro: A senha deve ter pelo menos 6 caracteres.")
                    time.sleep(2)
                    limpar_Tela()
                    continue
                
                break

            except Exception as e:
                print(f"Erro inesperado ao processar a senha: {e}")
                time.sleep(2)
                limpar_Tela()
                continue

        #Enviando dados
        try:
            msg = json.dumps({'Username': userName, 'Senha': senha, 'tipo': 'Login'})
            #Enviado dados
            cliente_Conexao.send(msg.encode()+b'\n')
            #esperando resposta
            resposta = json.loads(cliente_Conexao.recv(1024).decode())
            if resposta['validacao'] == 'True':
                limpar_Tela()
                print(f'Seja bem vindo {resposta["Nome"]}!\n')
                tipo = 'home'
                username = userName
                break
            else:
                print(f"Login negado! {resposta['erro']}")
                time.sleep(2)
                limpar_Tela()
            continue
        except Exception as e:
            print(f"Erro ao enviar os dados ao servidor: {e}")
            time.sleep(2)
            limpar_Tela()

def enviar_email():
    global cliente_Conexao, username

    while True:
        while True:
            try:
                destinatario = input("Digite o Username do destinatário sem espaços: ").strip()

                #Verifica se não tem espaço
                if " " in destinatario:
                    print("O username não pode conter espaços!")
                    time.sleep(2)
                    limpar_Tela()
                    continue     

                break
            except Exception as e:
                print(f"Erro inesperado: {e}")
                time.sleep(2)
                limpar_Tela()

        assunto_email = input("Digite  o assunto do E-mail:\n")
        corpo_email = input("Digite o corpo do E-mail:\n")

        email = json.dumps({
            "Remetente": username,
            "Destinatario": destinatario,
            "Assunto": assunto_email,
            "Corpo": corpo_email,
            "Data": time.strftime("%d-%m-%Y", time.localtime(time.time())),
            "Hora": time.strftime("%H:%M:%S", time.localtime(time.time())),
            "tipo": "Receber"
        })

        try:
            cliente_Conexao.send(email.encode()+b'\n')
            #esperando resposta
            resposta = json.loads(cliente_Conexao.recv(1024).decode())
            if resposta['validacao'] == 'True':
                print("E-mail enviado com sucesso.")
                time.sleep(2)
                limpar_Tela()
                break
            else:
                print(resposta['erro'])
                time.sleep(2)
                limpar_Tela()
        except Exception as e:
            print(f"Falha no envio do email: {e}")
            time.sleep(2)
            limpar_Tela()

def receber_email():
    global cliente_Conexao, username, mensagens, indices

    print("Recebendo E-mails...")

    while True:
        try:
            msg = json.dumps({'Username': username, 'tipo': 'Enviar'})
            #Enviado dados
            cliente_Conexao.send(msg.encode()+b'\n')
            resposta = json.loads(cliente_Conexao.recv(1024).decode())
            if resposta['validacao'] == "False":
                print(resposta['erro'])
                continue
            
            resposta.pop("validacao")
            mensagens.update(resposta)
            break

        except Exception as e:
            print(e)

    for mensagem in mensagens:
        if not mensagem in indices:
            indices.append(mensagem)
    
    time.sleep(2)

def exibir_mensagens():
    global mensagens
    cont = 1

    limpar_Tela()
    print(f"{len(mensagens)} e-mails recebidos:\n")
    for mensagem in mensagens:
        print(f"[{cont}] {mensagens[mensagem]['Assunto']}")
        cont += 1

def escolher_mensagens():
    global mensagens

    while True:
        try:
            exibir_mensagens()
            opc = int(input("\nQual e-mail deseja ler (Digite 0 para sair): "))
            if opc > 0 and opc <= len(mensagens):
                abrir_mensagem(opc)
            if opc == 0:
                limpar_Tela()
                break
        except Exception as e:
            print(e)

def abrir_mensagem(indice):
    global indices, mensagens
    limpar_Tela()
    print("Mensagem Aberta!\n")

    print(f"Origem: {mensagens[indices[indice - 1]]['Remetente']}\nDestinatario: {mensagens[indices[indice - 1]]['Destinatario']}\nData: {mensagens[indices[indice - 1]]['Data']}    Hora: {mensagens[indices[indice - 1]]['Hora']}\nAssunto da Mensagem: \n{mensagens[indices[indice - 1]]['Assunto']}\nCorpo da Mensagem: \n{mensagens[indices[indice - 1]]['Corpo']}")

    input("\nDigite enter para escolher outra Mensagem! ")

conexao = False
cliente_Conexao = None
tipo = 'login'
username = None
mensagens = {}
indices = []

limpar_Tela()
print("Bem Vindo ao Serviço de E-mail!")
time.sleep(2)
limpar_Tela()

while True:
    opc = interface_Principal(tipo)
    limpar_Tela()
    if opc == 1:
        interface_Conxecao()
    elif opc == 2 and conexao:
        cadastrar_conta()
    elif opc == 3 and conexao:
        acessar_conta()
    elif opc == 4 and conexao:
        enviar_email()
    elif opc == 5 and conexao:
        receber_email()
        escolher_mensagens()
    elif opc == 6:
        username = None
        tipo = 'login'
    elif opc == 0:
        desconectar_servidor()
        break