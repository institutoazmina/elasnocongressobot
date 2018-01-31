
# coding: utf-8

# In[1]:


import datetime
hoje = datetime.date.today( )
ontem = hoje - datetime.timedelta(days=1)
anteontem = hoje + datetime.timedelta(days=-2)


# In[ ]:


import requests

url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={ontem}&dataFim={ontem}'
print(url)

textos = []
textos2 = []
textos3 = []
for pagina in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
    parametros = {'formato': 'json', 'itens': 100, 'pagina': pagina} 
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
        proposicao_ementa = proposicao['ementa']
        proposicoes = {'id': proposicao_id, 'tipo': proposicao_tipo, 'ementa': proposicao_ementa}
        if 'mulheres' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação nos últimos 30 dias. Status: {status}. {endereco}'
            textos.append(texto)
            print(texto)
        elif 'mulher' in proposicao_ementa:
            texto2 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação nos últimos 30 dias: {endereco}'
            textos2.append(texto2)
            print(texto2)
        else:
            print(f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} não fala sobre mulheres. Link: {endereco}')


# In[ ]:


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

