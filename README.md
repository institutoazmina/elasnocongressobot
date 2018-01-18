# introducaoaopython
'Introdução à Programação: Python para Jornalistas'
Bot: https://twitter.com/elasnacamara

Essa aplicação em Python utiliza a API de proposições da Câmara dos Deputados, que retorna as proposições que tiveram alteração de tramitação nos últimos 30 dias ou em intervalo determinado. Ele reconhece, com uma busca por termos na ementa (no caso do bot, os termos 'mulher' e 'mulheres'), projetos de interesse e twitta as alterações de tramitação.

OBS: para intervalos pré-definidos, sempre menores do que 30 dias, é necessário gerar uma nova URL no site de Dados Abertos da Câmara, na API de Proposições:
https://dadosabertos.camara.leg.br/swagger/api.html

Os termos para a busca na ementa podem ser alterados.

