
# coding: utf-8

# In[1]:


import requests

url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes'

textos = []
textos2 = []
for pagina in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]:
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
        proposicao_ementa = proposicao['ementa']
        proposicoes = {'id': proposicao_id, 'tipo': proposicao_tipo, 'ementa': proposicao_ementa}
        if 'mulheres' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação nos últimos 30 dias: {endereco}'
            textos.append(texto)
            print(texto)
        elif 'mulher' in proposicao_ementa:
            texto2 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação nos últimos 30 dias: {endereco}'
            textos2.append(texto2)
            print(texto2)
        else:
            print(f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} não fala sobre mulheres. Link: {endereco}')


# In[3]:


textos2


# In[11]:


import tweepy, time, sys
 
argfile = str(sys.argv[1])
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'b6xN9f8zFs59S9c0oPyIZMWVM'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'E3msxSiDIBo98TrVmsbwrbqGPbIm5iC1lTrGQtuAwIudr4J64U'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '953313103026016257-dxLOBrexc986UcyW1AsbQoagYc9mOlP'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'Oo6e9rCO6x4wtatXSlyO7ZHuqWFRUOEeNWwOTNYwGt1ml'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
for texto in textos:
    api.update_status(f'#elasnacamara: {texto}')
for texto2 in textos2:
    api.update_status(f'#elasnacamara: {texto2}')

