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
Servidor:

bash
Copy
python servidor.py
Cliente:

bash
Copy
python cliente.py
🔧 Configuração do Cliente
Na tela inicial, selecione a opção 1 (Apontar Servidor).

Insira o endereço do servidor (ex: navalstrike.ddns.net) e porta (ex: 8888).

Após confirmação de "Serviço Disponível", as opções 2 (Cadastrar) e 3 (Acessar) serão habilitadas.

🖥️ Servidor de Teste
Um servidor de teste está disponível em:
Endereço: navalstrike.ddns.net
Porta: 8888

⚠️ Atenção:

Solicite autorização prévia via e-mail ou contato direto antes de utilizar este servidor.

Qualquer servidor compatível com os requisitos da atividade pode ser utilizado.

🧩 Exemplo de Uso
Tela Inicial do Cliente:
Copy
Cliente E-mail Service BSI Online  
1) Apontar Servidor  
2) Cadastrar Conta  
3) Acessar E-mail  
Tela Após Autenticação:
Copy
Seja Bem Vindo [NOME DO USUÁRIO]  
4) Enviar E-mail  
5) Receber E-mails  
6) Logout  
Envio de E-mail:
Campos obrigatórios: destinatário, assunto, corpo.

Mensagens de retorno:

E-mail enviado com sucesso

Destinatário Inexistente

Falha no envio do email: {exception}

📌 Observações
Não há persistência de dados: Contas e e-mails são armazenados apenas em memória.

Novas funcionalidades são bem-vindas! Contribuições podem ser enviadas via pull request.

📧 Contato
Para dúvidas ou acesso ao servidor de teste, entre em contato:
E-mail: [seu-email@exemplo.com]

Desenvolvido por: [Seu Nome]
Curso: Bacharelado em Sistemas de Informação (BSI)
Disciplina: Sistemas Distribuídos - 6º Período