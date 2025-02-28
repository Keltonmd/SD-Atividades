import socket
import json
import concurrent.futures
import bcrypt

def teste_conexao(conexao, cliente):
    
    try:
        teste_conexao = json.loads(conexao.recv(1024).decode())
        print(f"Teste de conexão com Cliente: {cliente}. Realizada com Sucesso!")
    
        if teste_conexao["msgTeste"] == "Hellow":
            conexao.send(json.dumps({"msgTeste": "Hellow"}).encode())
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return False

def validar_username(conexao, mensagem, cliente):
    global usuarios
    try:
        username = mensagem["username"]
        print(f"Validando username {username}, para o cliente: {cliente}")
        
        if not username:
            conexao.send(json.dumps({"validacao": "Username inválido"}).encode())
            print(f"Validando username {username}, para o cliente: {cliente}: Username Invalido")
            return
            
        if username in usuarios:
            conexao.send(json.dumps({"validacao": "True"}).encode())
            print(f"Validando username {username}, para o cliente: {cliente}: Username Inalido")
        else:
            conexao.send(json.dumps({"validacao": "False"}).encode())
            print(f"Validando username {username}, para o cliente: {cliente}: Username Valido")

    except Exception as e:
        print(f"Erro ao validar username: {e}")

def cadastro(conexao, mensagem, cliente):
    global usuarios
    
    usuarios[mensagem['Username']] = {'Nome': mensagem['Nome'], 
                                      'Senha': mensagem['Senha'].encode(),
                                      'Email_recebidos': {}
                                     }
    conexao.send(json.dumps({"notificacao": "True"}).encode())
    print(f"Realizando cadastro para o cliente {cliente}: {mensagem['Username']}. Cadastro com Sucesso.")

def login(conexao, mensagem, cliente):
    global usuarios

    username = mensagem['Username']
    senha = mensagem['Senha']

    if not username in usuarios:
        conexao.send(json.dumps({"validacao": "False", 'erro': "Username não existe!"}).encode())
        print(f"Realizando Login para o cliente {cliente}: {username}. Falha no login")
        return

    senha_hash = usuarios[username].get('Senha')

    if bcrypt.checkpw(senha.encode(), senha_hash):
        conexao.send(json.dumps({"validacao": "True"}).encode())
        print(f"Realizando Login para o cliente {cliente}: {username}. Login Com Sucesso")
    else:
        conexao.send(json.dumps({"validacao": "False", 'erro': "Senha incorreta!"}).encode())
        print(f"Realizando Login para o cliente {cliente}: {username}. Falha no login")

def receber_email(conexao, mensagem, cliente):
    global usuarios

    destinatario = mensagem['Destinatario']

    if not destinatario in usuarios:
        conexao.send(json.dumps({"validacao": "False", 'erro': "Destinatario Inexistente!"}).encode())
        print(f"Recebendo email do cliente {cliente} para o cliente {destinatario}: {mensagem}. Falha no recebimento")
        return

    username = mensagem['Remetente']
    assunto = mensagem['Assunto']
    corpo = mensagem['Corpo']
    data = mensagem['Data']
    hora = mensagem['Hora']
    chave_email = f"{data}_{hora}"

    usuarios[destinatario]['Email_recebidos'][chave_email] = {
        "Remetente": username,
        "Destinatario": destinatario,
        "Assunto": assunto,
        "Corpo": corpo,
        "Data": data,
        "Hora": hora,
    }

    conexao.send(json.dumps({"validacao": "True"}).encode())
    print(f"Recebendo email do cliente {cliente} para o destino {destinatario}: {mensagem}. Sucesso no recebimento")

def enviar_email(conexao, mensagem, cliente):
    global usuarios

    username = mensagem['Username']
    
    if not username in usuarios:
        conexao.send(json.dumps({"validacao": "False", 'erro': "Destinatario Inexistente!"}).encode())
        print(f"Enviando email para o cliente {cliente}: {mensagem}. Falha no envio")
        return

    mensagens_recebidas = usuarios[username]['Email_recebidos']
    mensagens_recebidas["validacao"] = "True"

    conexao.send(json.dumps(mensagens_recebidas).encode())
    
    usuarios[username]['Email_recebidos'].clear()
    print(f"Enviando email para o cliente {cliente}: {mensagem}. Sucesso no envio")

    
def handle_client(conexao, cliente):
    tipos = ['Cadastro', 'Login', 'Receber', 'Enviar', 'Veri_User']
    try:
        print(f"Cliente: {cliente} acaba de se conectar!")
        if not teste_conexao(conexao, cliente):
            return

        while True:
            mensagens_cliente = conexao.recv(1024).decode().split('\n')
            mensagens_cliente.pop()
            for mensagem in mensagens_cliente:
                mensagem = json.loads(mensagem)
                print(f"Cliente: {cliente}\nRequisção: {mensagem['tipo']}")
                if mensagem['tipo'] in tipos:
                    if mensagem['tipo'] == tipos[0]:
                        cadastro(conexao, mensagem, cliente) #cadastrar
                    elif mensagem['tipo'] == tipos[1]:
                        login(conexao, mensagem, cliente) #validar
                    elif mensagem['tipo'] == tipos[2]:
                        receber_email(conexao, mensagem, cliente) #receber
                    elif mensagem['tipo'] == tipos[3]:
                        enviar_email(conexao, mensagem, cliente)# Enviar
                    elif mensagem['tipo'] == tipos[4]:
                        validar_username(conexao, mensagem, cliente) #autenticar_username

    except Exception as e:
        print(f'Erro com o cliente {endereco}: {e}')


usuarios = {}
ENDPOINT = ('0.0.0.0', 8888)
print("Iniciando")

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as endpoint:
    endpoint.bind(ENDPOINT)
    endpoint.listen()
    with concurrent.futures.ThreadPoolExecutor(20) as workers:
        while True:
            conexao,endereco = endpoint.accept()
            print(f'novo cliente conectado: {endereco}')
            workers.submit(handle_client,conexao, endereco)