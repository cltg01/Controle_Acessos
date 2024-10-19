## Detalhes técnicos:

Sistema sendo desenvolvido em PHP 7.4+, usando a arquitetura MVC (POO), CoffeeCode DataLayer como ORM, banco de dados MySQL, seguindo as melhores práticas de programação (separação de camadas, separação de responsabilidades, nomes de variáveis e métodos com coerência).

- Estou implementando o framework de testes PHPUnit, e adaptando algumas funções para serem testáveis.

Necessário para o funcionamento do sistema: PHP 7.4+, MySQL, Composer, GIT (para clonar o repositório, caso queira).

## Procedimentos para instalação local:

- Baixe o projeto em uma pasta
  - Com o GIT instalado, use o comando <code>git clone https://github.com/rotognin/portaria.git</code>
  - Será criada a pasta <code>portaria</code>
- Acesse a pasta via linha de comando
- Execute o comando: <code>composer update</code> para baixar as dependências do projeto
- No MySQL crie um banco com o nome <code>portaria_db</code>
- Rode o script <code>docs/tabelas.sql</code> no banco para criar as tabelas do sistema
  - Será criado o usuário "admin" no banco, senha "123", com acesso ao ambiente administrativo.
- Ajuste as configurações de acesso ao banco de dados no arquivo <code>src/config.php</code>
- Crie o arquivo <code>src/configemail.php</code> para ajustar as configurações de envio de e-mail, caso queira utilizar essa opção
  - Neste arquivo deverão ser informadas as segunites configurações:
  - <code>$email_remetente = 'remetente@email.com';</code> <i> Remetente do e-mail </i>
  - <code>$email_servidor = 'smtp.servidor.com';</code> <i> Host, endereço do servidor de disparo de e-mails (SMTP) </i>
  - <code>$email_usuario = 'login@email.com';</code> <i> Login da conta de e-mail </i>
  - <code>$email_senha = '123456';</code> <i> Senha da conta de e-mail </i>

### Considerações

O projeto está em constante atualização, sendo adicionadas funcionalidades e melhorias. Sugestões serão muito bem vindas.

### Melhorias sendo desenvolvidas e futuras

- Geração de relatórios em PDF
- <b>OK</b> - Envio de e-mails para a empresa quando o visitante der entrada
- <b>OK</b> - Criação de parâmetros:
  - Acompanhante pode sair antes?
  - Atribuir crachás específicos para acompanhantes
  - <b>OK</b> Previsão de saída (exibirá mensagem ao passar do horário previsto)
  - <b>OK</b> Limitar o número de acompanhantes
- <b>OK</b> - Ao criar uma Unidade nova (matriz ou filial), criar um registro com valores iniciais
- <b>OK</b> - Exibir mais informações nos detalhes de uma movimentação
- Geração de gráficos
- Envio de mensagens entre os ambientes
- Na administração:
  - verificar quais portarias estão ativas no momento (monitoramento de visitas)
  - exibir movimentações não finalizadas de dias anteriores
- <b>OK</b> No cadastro das portarias de uma unidade, informar se será entrada/saída de veículos, pessoas ou ambos
- Criação de especificações para rodar o projeto usando Docker e Docker-compose.
