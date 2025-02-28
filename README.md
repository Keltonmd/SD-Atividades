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
