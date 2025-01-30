![GitHub](https://img.shields.io/github/license/institutoazmina/elasnocongressobot)

# Elas no Congresso 

O Elas no Congresso é um projeto da Revista AzMina que usa dados públicos para monitorar avanços e retrocessos nos direitos das mulheres no Congresso Nacional. Ele foi selecionado entre mais de 300 iniciativas, pelo Google News Initiative na América Latina, programa de incentivo ao jornalismo na era digital. O projeto se desdobra nesse robô, em um ranking dos parlamentares de acordo com sua atuação nas temáticas de gênero, e na produção de conteúdos no site da Revista AzMina e em newsletters temáticas. 

## Funcionalidades
- O scraper faz a busca por palavras-chave relacionadas a questões de gênero e mulheres nos portais da Câmara dos Deputados e do Senado Federal.
- Ele extrai informações como título do projeto, autor, data de apresentação, status do projeto e etc.
- Os dados coletados são organizados e salvos em planilhas no formato CSV para fácil análise.
- Modelos de código-aberto no HuggingFace são utilizados para fazer a classificação da ementa do projeto.
- Uma LLM de código-aberto é usada via API (Replicate) para fazer a classificação do inteiro teor do projeto.

## Requisitos de Instalação
- Docker e Docker compose

## Instalação
1. Clone o repositório para o seu ambiente local:
    ```
    git clone https://github.com/institutoazmina/elasnocongressobot
    ```
2. Navegue até o diretório do projeto;
3. Copie o arquivo de variável de ambientes e preencha-os:
    ```
    cp .env.sample .env
    ```
4. Execute o Docker Compose para criar e iniciar os contêineres:
    ```
   docker compose up -d --build
    ```
5. Execute o scraper:
    ```
   docker exec elasnacamera ./run.sh
    ```
## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença
Este projeto está licenciado sob a [Licença AGPL-3.0](https://github.com/institutoazmina/elasnocongressobot/blob/master/LICENSE.txt).