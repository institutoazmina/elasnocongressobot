# Elas no Congresso Bot

O **Elas no Congresso Bot** é um robô de coleta automática de dados que integra o projeto [**Elas no Congresso**](https://elasnocongresso.com.br) da [Revista AzMina](https://azmina.com.br/). Ele foi desenvolvido para monitorar e organizar informações legislativas relevantes aos direitos das meninas, mulheres e comunidades LGBTQIAP+, e à igualdade de gênero no Brasil.

Este robô é responsável por alimentar os dados que servem como base para a [**QuitérIA-IA-Feminista Elas no Congresso**](https://github.com/indgris/ia-feminista-elas-no-congresso), uma solução de inteligência artificial voltada para a classificação e análise automática de proposições legislativas com foco em gênero, feminismo e direitos das mulheres.

---

## 📌 Sumário

- [📚 Sobre o Projeto Elas no Congresso](#-sobre-o-projeto-elas-no-congresso)
- [⚙️ Funcionalidades](#-funcionalidades)
- [🧠 Integração com a IA-Feminista](#-integração-com-a-ia-feminista)
- [🚀 Requisitos de Instalação](#-requisitos-de-instalação)
- [🛠️ Instalação](#-instalação)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)

---

## 📚 Sobre o Projeto Elas no Congresso

O projeto **Elas no Congresso** usa dados públicos para monitorar avanços e retrocessos nos direitos das meninas, mulheres e pessoas LGBTQIA+ no Congresso Nacional brasileiro. Em 2020, ele foi selecionado entre mais de 300 iniciativas pela **Google News Initiative**, programa de incentivo ao jornalismo na era digital.

Criado pelo Instituto AzMina, o projeto nasceu diante do crescimento da disputa pelas pautas ligadas à mulher no Congresso, com o objetivo de tornar o monitoramento legislativo mais acessível para a sociedade, imprensa e organizações que advogam por esses temas.

O projeto se desdobra em:

- Este robô (scraper) de coleta automatizada de dados legislativos;
- Um **ranking de parlamentares** baseado em sua atuação nas temáticas de gênero, inspirado no projeto "Ruralômetro" da ONG Repórter Brasil;
- A **produção de conteúdos** no site da AzMina e em newsletters semanais de análise da movimentação legislativa do período sobre os temas de interesse.
- A **QuitérIA**, um Large Language Model (LLM) em operação desde fevereiro de 2025, lançada oficialmente para o público em novembro de 2025. Essa ferramenta de inteligência artificial classifica proposições legislativas sobre direitos de gênero por temas e, em seguida, quão favoráveis elas são aos direitos das meninas, mulheres e pessoas LGBTQIA+ numa escala de 0 a 1, onde 0 é extremamente favorável e 1 extremamente desfavorável. 

A primeira fase foi lançada em 8 de março de 2020, com a robô @elasnocongresso no Twitter, que permitia acompanhar as tramitações diárias de projetos sobre temas de gênero (descontinuada em junho de 2023 devido ao fechamento do acesso gratuito à API do Twitter).

A segunda fase, em junho de 2020, foi o lançamento do site com a primeira edição do ranking de parlamentares segundo sua atuação em temáticas de gênero, com atualizações em novembro/2020, junho/2021, setembro/2022 e junho/2024, contemplando dados de projetos apresentados entre janeiro/2019 e dezembro/2023.

Hoje, em meados de 2025, nos preparamos para lançar mais uma atualização do ranking Elas no Congresso com dados de 788 proposições legislativas sobre gênero apresentadas entre 1/1/2024 e 30/6/2025.

---

## ⚙️ Funcionalidades

O scraper faz a busca por palavras-chave relacionadas a questões de gênero e mulheres nos portais da Câmara dos Deputados e do Senado Federal.  
Ele extrai informações como título do projeto, autor, data de apresentação, status do projeto, última movimentação legislativa, entre outros.  
Os dados coletados são organizados e salvos em arquivos no formato CSV para fácil análise.

---

## 🧠 Integração com a IA-Feminista

Os dados coletados por este scraper são utilizados para treinar e alimentar os modelos da [**QuitérIA-IA-Feminista Elas no Congresso**](https://github.com/institutoazmina/ia-feminista-congresso). Essa IA analisa e rotula as proposições legislativas automaticamente, identificando seus temas e se são favoráveis ou desfavoráveis aos direitos das mulheres.

Além disso:

- **Modelos hospedados no Hugging Face** são usados para classificar a ementa dos projetos;
- Uma **LLM open-source via API (Replicate)** classifica o inteiro teor das propostas.

---

## 🚀 Requisitos de Instalação

- Docker  
- Docker Compose

---

## 🛠️ Instalação

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

---

## 🤝 Contribuição

Contribuições são muito bem-vindas!  
Se você tiver sugestões de melhorias, encontrar bugs ou quiser propor novas funcionalidades:

- Abra uma [issue](https://github.com/institutoazmina/elasnocongressobot/issues)
- Ou envie um [pull request](https://github.com/institutoazmina/elasnocongressobot/pulls)

Vamos construir uma ferramenta mais poderosa para a defesa dos direitos das mulheres? 💜

---

## 📄 Licença

Este projeto está licenciado sob a [Licença AGPL-3.0](https://github.com/institutoazmina/elasnocongressobot/blob/master/LICENSE.txt).
