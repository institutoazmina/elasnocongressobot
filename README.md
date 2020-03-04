# Elas no Congresso 

O Elas no Congresso é um projeto da Revista AzMina que usa dados públicos para monitorar avanços e retrocessos nos direitos das mulheres no Congresso Nacional. Ele foi selecionado entre mais de 300 iniciativas, pelo Google News Initiative na América Latina, programa de incentivo ao jornalismo na era digital. O projeto se desdobra nesse robô, em um ranking dos parlamentares de acordo com sua atuação nas temáticas de gênero, e na produção de conteúdos no site da Revista AzMina e em newsletters temáticas. 

# o robô (https://twitter.com/elasnocongresso)

Essa aplicação em Python utiliza a API de proposições da Câmara dos Deputados e do Senado para monitorar projetos de interesse que tratam sobre direito das mulheres. 

Primeiro, AzMina selecionou uma lista ampla de palavras-chave frequentemente relacionadas aos direitos das mulheres. O robô busca nas APIs da Câmara dos Deputados e do Senado as roposições que tiveram alteração de tramitação no último dia. Ele reconhece os projetos de interesse com uma busca por termos ("mulher", "mulheres", "aborto", "licença maternidade", "estupro", "feminicídio", etc) nas ementas das proposições.

Por fim, ele publica em uma conta no Twitter os detalhes dessa proposição: a casa legislativa onde ela se encontra, o tipo e número da matéria, o autor, o tema principal, o status atual de tramitação e também o link para o texto do projeto.

# links de referência

Elas no Congresso no Twitter: https://twitter.com/elasnocongresso

API da Câmara dos Deputados: https://dadosabertos.camara.leg.br/swagger/api.html (Proposições).

API do Senado: https://www12.senado.leg.br/dados-abertos/conjuntos?grupo=projetos-e-materias&portal=legislativo

# instalando dependencias

> Primeiro verificar se o pip para o python3 está instalado (sudo apt install python3-pip em debian-like)

    $ python3 -m pip --version

Deve exibir: `pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)` ou semelhante

    $ python3 -m pip install -r requirements.txt

# executando

Para baixar as proposições, basta executar o arquivo `elasnocongresso.py`, o resultado dos tweets será salvo em ./dados/tweets.json, você pode visualizar este arquivo para conferir o contéudo.

Caso esteja tudo OK com o conteudo, você deve executar o script `enviar_tweets.py` para fazer o envio.

Para executar `enviar_tweets.py`, será necessário configurar o arquivo .env com a chave do twitter:

    $ cp .env.sample .env

Edite o conteudo do .env com a chave, e então poderá ser possível executar o envio.

A cada envio de tweet, um arquivo cujo nome é o hash do tweet, ficará salvo em ./dados/tweets-enviados/$HASH, dentro dentro deste arquivo, tem informações sobre o tweet.
