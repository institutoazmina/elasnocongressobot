
# coding: utf-8

# In[ ]:


import datetime
hoje = datetime.date.today( )
ontem = hoje - datetime.timedelta(days=1)
anteontem = hoje + datetime.timedelta(days=-2)

import requests

url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={ontem}&dataFim={ontem}'
print(url)

textos = []
textos2 = []
textos3 = []
textos4 = []
textos5 = []
textos6 = []
textos7 = []
textos8 = []
textos9 = []
textos10 = []

lista = range(1,10)
for pagina in lista:
    print(pagina)
    parametros = {'formato': 'json', 'itens': 15, 'pagina': pagina} 
    resposta = requests.get(url, parametros)
    for proposicao in resposta.json()['dados']:
        proposicao_id = proposicao['id']
        proposicao_numero = proposicao['numero']
        proposicao_ano = proposicao['ano']
        proposicao_tipo = proposicao['siglaTipo']
        proposicao_link = proposicao['uri']
        parametros = {'formato': 'json'} 
        response = requests.get(proposicao_link, parametros) 
        dados = response.json()['dados']
        endereco = dados['urlInteiroTeor']
        situacoes = dados['statusProposicao']
        for situacao in situacoes:
            tramitacao = situacoes['descricaoTramitacao']
            status = situacoes['descricaoSituacao']
        proposicao_ementa = proposicao['ementa']
        proposicoes = {'id': proposicao_id, 'tipo': proposicao_tipo, 'ementa': proposicao_ementa}
        
        proposicao_link = proposicao['uri']
        parametros = {'formato': 'json'} 
        response = requests.get(proposicao_link, parametros) 
        if 'jornada de trabalho' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            texto3 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre jornada de trabalho para mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos3.append(texto3)
            print(texto3)
        elif 'jornada de trabalho' in proposicao_ementa and 'mulher' in proposicao_ementa:
            texto3 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre jornada de trabalho para mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos3.append(texto3)
            print(texto3)
        elif 'violência contra a mulher' in proposicao_ementa:
            texto4 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre violência contra a mulher e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos4.append(texto4)
            print(texto4)
        elif 'violência doméstica' in proposicao_ementa:
            texto4 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre violência doméstica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos4.append(texto4)
            print(texto4)
        elif 'aborto' in proposicao_ementa:
            texto5 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre aborto e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos5.append(texto5)
            print(texto5)
        elif 'violência sexual' in proposicao_ementa:
            texto6 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre violência sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos6.append(texto6)
            print(texto6)
        elif 'feminicídio' in proposicao_ementa:
            texto7 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre feminicídio e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos7.append(texto7)
            print(texto7)
        elif 'assédio sexual' in proposicao_ementa:
            texto8 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre assédio sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos8.append(texto8)
            print(texto8)
        elif 'estupro' in proposicao_ementa:
            texto9 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre estupro e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos9.append(texto9)
            print(texto9)
        elif 'licença maternidade' in proposicao_ementa:
            texto10 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre licença maternidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos10.append(texto10)
            print(texto10)
        elif 'mulheres' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos.append(texto)
            print(texto)
        elif 'mulher' in proposicao_ementa:
            texto2 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos2.append(texto2)
            print(texto2)


# In[2]:


import tweepy, time, sys 
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'SaDHnhFDYoEnsTh9qxkF8ILTG'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'OZp4KL7NKnA5aDfkX2Z6uh4U2PyGCDxs3iX6EYtyt3g02mbyCq'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '953313103026016257-dxLOBrexc986UcyW1AsbQoagYc9mOlP'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'Oo6e9rCO6x4wtatXSlyO7ZHuqWFRUOEeNWwOTNYwGt1ml'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
for texto in textos:
    api.update_status(f'#elasnacamara: {texto}')
for texto2 in textos2:
    api.update_status(f'#elasnacamara: {texto2}')
for texto3 in textos3:
    api.update_status(f'#elasnacamara: {texto3}')
for texto4 in textos4:
    api.update_status(f'#elasnacamara: {texto4}')
for texto5 in textos5: 
    api.update_status(f'#elasnacamara: {texto5}')

