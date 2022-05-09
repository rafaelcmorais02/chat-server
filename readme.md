# Descrição do projeto
Aplicação para a troca de mensagens entre usuários, utilizando nginx, gunicorn, django e postgres, **image-01**. Ambiente de produção "dockerizado" criado em uma instância EC2 na AWS. 
## Setup do projeto:
O desenvolvimento no Dajngo REST framework consistiu em modelar a relação entre usuários (entidade "users") e mensagens (entidade "messages") seguindo o Diagrama Entidade Relacional que faz referência a **image-02**. Além disso, para consumo do serviço por uma aplicação web terceira foram expostos endpoints que serão detalhados no decorrer do texto.  
### Aplicação para gerenciamento de usuários
- Para registro de usuários foi desenvolvida uma aplicação "user" customizada (não o form "user" padrão do Django), ver [documentação](https://docs.djangoproject.com/en/4.0/topics/auth/customizing/); 
- Criado token para cada usuário através de "signals", ver [documentação](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) 
- Criados endpoints para:
    - Obtenção de token, <url>/api/v1/users/token
    - Busca de todos os usuários, <url>/api/v1/users/all
    - Registro de um usuário, <url>/api/v1/users/register
- Nos endpoints com autenticação, a autenticação usada foi "Bearer Token", e a permissão "IsAuthenticated"
- No endpoint <url>/api/v1/users/all, todos os usuários exceto o autenticado são obtidos (ver regra de negócio em user/services.py) 
### Aplicação para gerenciamento de mensagens
- Criada aplicação "message"
- Criados endpoints para:
  - Registro de mensagens, <url>/api/v1/messages/register 
  - Busca de mensagens, <url>/api/v1/messages/all
- Nos endpoints com autenticação, a autenticação usada foi "Bearer Token", e a permissão "IsAuthenticated"
- No registro de mensagens, foi implementada uma regra para associar o user_sender ao id do usuário autenticado (ver regra de negócio em user/services.py)
- Na busca de mensagens, foi implementada uma regra para retornar apenas as mensagens do usuário autenticado (ver regra de negócio em user/services.py)
- No serializer, foi criado uma validação para impedir a criação de mensagens em que um usuário é o remetente e também o destinatário

## Ambiente de desenvolvimento local
Para testes locais da aplicação, foram criados dois containers docker definidos no docker-compose.yml. Um para o PostgreSQL, e um para o pgAdmin. Ver [arigo](https://renatogroffe.medium.com/postgresql-pgadmin-4-docker-compose-montando-rapidamente-um-ambiente-para-uso-55a2ab230b89). As variáveis de ambiente usadas pelas imagens estão no arquivo "env.dev" Dentro do aquivo settings.py.

## Ambiente remoto
O ambiente remoto consiste em um servidor web, nginx, servindo arquivos estáticos e fazendo proxy reverso com o gunicorn, que por usa ver se comunica com as aplicações Django através do protocolo WSGI. Também foi utilizada uma imagem do certbot para gerar um certificado ssl (e renovação do mesmo) para conexão https (ver [artigo](https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71)). Abaixo um delhamento de cada um desses containers.

### Serviço Django
Serviço nomeado de "chat-server" dentro do arquivo docker-compose.prod.yml, com um diretório de trabalho /home/app/web e volume para aquivos estáticos. Ele expões a porta 8000 (sem publicá-la para o host) e depende da execução do postgres. A execução do container se faz pelo comando gunicorn config.wsgi:application --bind 0.0.0.0:8000
obs: para coletar os aquivos estáticos, usar o comando *python manage.py collectstatic*

### Serviço nginx
O arquivo de configurações do servidor web está no diretório nginx/nginx-certbot.conf. Nele estão detalhadas as especificações dos servidores http (porta 80) e https (porta 443). Além de servir os arquivos estáticos o nginx funciona como um proxy reverso, redirecionando as chamadas na porta 443 para "chat-server:8000". Para isso o container do serviço está configurado com as portas 80:80 e 443:443. Além disso, no docker-compose.prod.yml são declarados três volumes: um igual ao do serviço chat-server, para os arquivos estáticos, e outros dois para comunicação com o certbot (uso de certificado ssl). 

### Serviço certbot
O serviço certbot é o responsável por gerar e renovar um certificado ssl para conexões https. Dessa forma, o nginx irá requerer a validação do domínio pelo Let's Encrypt, e caso o certificado seja válido, o domínio também será considerado válido. Para isso funcionar, foi criado o executável init-letsencrypt.sh, que irá:
* Criar um certificado "dummy"  
* Iniciar o nginx (se o mesmo não encontrar nenhum certificado, o container irá parar)
* Deletar o certificado falso, e 
* Pedir o certificado verdadeiro
Após isso, todo o ecossistema poderá ser iniciada através do comando: docker-compose -f docker-compose.prod.yml up -d