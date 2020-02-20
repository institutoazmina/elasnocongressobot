@elasnacamara
Bot: https://twitter.com/elasnacamara

Essa aplicação em Python utiliza a API de proposições da Câmara dos Deputados, que retorna as proposições que tiveram alteração de tramitação nos últimos 30 dias ou em intervalo determinado. Ele reconhece os projetos de interesse com uma busca por termos ("mulher", "mulheres", "aborto", "licença maternidade", "estupro", "feminicídio", etc).

API: https://dadosabertos.camara.leg.br/swagger/api.html (Proposições).

Os termos para a busca na ementa e a URL com data de início e fim da busca podem ser alterados.

Esse projeto foi elaborado como trabalho de conclusão de curso do MOOC "Introdução à programação: Python para jornalistas", oferecido pelo Centro Knight com o apoio do Google News Lab.

# instalando dependencias

> Primeiro verificar se o pip para o python3 está instalado (sudo apt install python3-pip em debian-like)

    $ python3 -m pip --version

Deve exibir: `pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)` ou semelhante

    $ python3 -m pip install -r requirements.txt

# executando

Para baixar as proposições, basta executar o arquivo `@elasnacamara.py`, o resultado dos tweets será salvo em ./dados/tweets.json

Caso esteja tudo OK com o conteudo, você pode deve executar o script `@elasnacamara_enviar_tweets.py` para fazer o envio.

Para executar `@elasnacamara_enviar_tweets.py`, será necessário configurar o arquivo .env com a chave do twitter:

    $ cp .env.sample .env

Edite o conteudo do .env com a chave, e então poderá ser possível executar o envio.

A cada envio de tweet, um arquivo cujo nome é o hash do tweet, ficará salvo em ./dados/tweets-enviados/$HASH, dentro dentro deste arquivo, tem informações sobre o tweet.