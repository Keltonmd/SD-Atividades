# LABORATÓRIO PRÁTICO: SOCKETs  
**Implementação de um Serviço de E-Mails Cliente-Servidor com Sockets**  

---

## 📝 Descrição  
Este projeto consiste em um protótipo de serviço de e-mails utilizando comunicação via sockets, seguindo os requisitos da disciplina de Sistemas Distribuídos. A aplicação é dividida em:  
- **Cliente**: Interface para usuários interagirem com o serviço (cadastro, autenticação, envio/recebimento de e-mails).  
- **Servidor**: Responsável por gerenciar contas, autenticação, armazenamento temporário de e-mails e logs de operações.  

---

## 🛠️ Requisitos  
### Bibliotecas e Ferramentas  
- Python 3.x  
- Biblioteca `bcrypt` (para hash de senhas):  
  ```bash
  pip install bcrypt
  ```  

### Funcionalidades Principais  
**Cliente:**  
1. Configurar IP/Porta do servidor.  
2. Cadastrar conta (nome, username único, senha com hash via bcrypt).  
3. Autenticação com username e senha.  
4. Enviar e-mails (destinatário, assunto, corpo).  
5. Receber e-mails (lista com remetente e assunto, visualização completa).  
6. Logout.  

**Servidor:**  
1. Cadastro e gerenciamento de contas.  
2. Autenticação segura.  
3. Armazenamento temporário de e-mails (excluídos após entrega).  
4. Logs em tempo real de operações.  

---

## ⚙️ Instalação e Execução  
1. Clone o repositório do projeto.  
2. Instale as dependências:  
   ```bash
   pip install bcrypt
   ```  
3. **Servidor:**  
   ```bash
   python servidor.py
   ```  
4. **Cliente:**  
   ```bash
   python cliente.py
   ```  

---

## 🔧 Configuração do Cliente  
1. Na tela inicial, selecione a opção **1 (Apontar Servidor)**.  
2. Insira o endereço do servidor (ex: `navalstrike.ddns.net`) e porta (ex: `8888`).  
3. Após confirmação de "Serviço Disponível", as opções 2 (Cadastrar) e 3 (Acessar) serão habilitadas.  

---

## 🖥️ Servidor de Teste  
Um servidor de teste está disponível em:  
**Endereço:** `navalstrike.ddns.net`  
**Porta:** `8888`  

⚠️ **Atenção:**  
- **Solicite autorização prévia** via e-mail ou contato direto antes de utilizar este servidor.  
- Qualquer servidor compatível com os requisitos da atividade pode ser utilizado.  

---

## 🧩 Exemplo de Uso  
### Tela Inicial do Cliente:  
```
Cliente E-mail Service BSI Online  
1) Apontar Servidor  
2) Cadastrar Conta  
3) Acessar E-mail  
```  

### Tela Após Autenticação:  
```
Seja Bem Vindo [NOME DO USUÁRIO]  
4) Enviar E-mail  
5) Receber E-mails  
6) Logout  
```  

### Envio de E-mail:  
- Campos obrigatórios: destinatário, assunto, corpo.  
- Mensagens de retorno: "E-mail enviado com sucesso", "Destinatário Inexistente" ou erro específico.  

---

## 📌 Observações  
- **Não há persistência de dados**: Contas e e-mails são armazenados apenas em memória.   

---

## 📧 Contato  
Para dúvidas ou acesso ao servidor de teste, entre em contato:  
**E-mail:** keltonm6@gmail.com 
``` 

---

**Desenvolvido por:** Kelton Martins Dias 
**Curso:** Bacharelado em Sistemas de Informação (BSI)  
**Disciplina:** Sistemas Distribuídos - 6º Período  
```