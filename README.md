# Solução apresentada por Adrian Dalle Grave #

## Execução do app

* Clone o projeto e vá para a pasta dele no linux
* `python3 -m venv venv`
* `. venv/bin/activate`
* `pip install Flask`
* `pip install Flask-Session`
* `export FLASK_APP=app.py`
* `flask run`
* Acesse o site em http://127.0.0.1:5000/

## Planejamento

* Fazer o app em Flask
* Utilizar todos os métodos propostos
* Versionar corretamente


updating...


# Desafio estágio dev CDV #

Bem-vindo ao teste técnico do processo seletivo do Clube do Valor.

## Instruções ##

* Faça o Fork desse repositório e responda o desafio em um projeto com o seguinte nome: cdv-estagio-investimentos-nome-sobrenome;
* Assim que concluir o seu desafio, publique o mesmo em sua conta do bitbucket ou github e mande o link do projeto para o recrutador, informando que finalizou.
* Não se esqueça de deixar o projeto como público para que possamos avaliá-lo
* Você pode utilizar linguagem, componentes e frameworks que ficarem mais confortáveis para você. Caso saiba Python ou PHP dê preferência para essas linguagens. 
* A entrega deve seguir o prazo orientado pelo recrutador no e-mail
* Não esqueça de documentar o processo necessário para rodar a aplicação.

## IMPORTANTE! ## 

Soluções parciais serão aceitas. 
Esse testé é feito para avaliar suas forças e fraquezas técnicas. Aproveite seus pontos fortes e não tenha medo de errar no que não tem certeza. 
Caso algo não seja implementado, utilize constantes ou stubs para simular comportamentos necessários e adicione um comentário no email ou README.md do repositório para nos avisar.

O tempo previsto para desenvolvimento desse teste é de 3-6horas.

## Desafio ##

Como você já sabe, o Clube do Valor é uma gestora de patrimonio. Quando um cliente está entrando para nossa gestão ele passa por várias etapas no que chamamos de 'onboarding'. 
Essas etapas são:

* Aguardando assinatura de documentos
* Aguardando transferência de recursos
* Gestão de patrimônio ativa

Os dados que guardamos dos nossos clientes são:

* Nome
* CPF
* Etapa atual

Sua tarefa hoje é desenvolver uma aplicação web (frontend e backend) para gerenciar o cadastro de clientes. Você pode fazer a aplicação 

### Quais são as funcionalidade necessárias? ###

Frontend:

Aqui você pode fazer quantas telas quiser.

* Visualizar a lista de clientes cadastrados
* Adicionar/Remover/Editar clientes
* Atualizar etapa do cliente

Backend:

* Dados de clientes devem ser salvo em um banco de dados
* Chamada GET de api que retorna a lista de clientes e suas etapas em formato JSON.
* Chamada PUT de api que atualiza a etapa de um cliente
* Chamada POST de api que cria um novo cliente
* Caso ache relevante ou necessário, crie outras chamadas de API.


## O que será avaliado ##

* Estrutura de código e banco de dados.
* O histórico de commits também será avaliado.
* Interface (Design e estrutura do código)
* Caso relevante, explique melhorias que poderiam ser feitas.

## Diferenciais ##

* Funcionalidades extras
* Testes do código.
* Liberação da aplicação utilizando Docker.
* Boa documentação de código.
* Utilização de boas práticas.
* Adaptar frontend para dispositivos móveis.
