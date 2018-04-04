
# coding: utf-8

# In[ ]:

#Variáveis de datas
import datetime #importando biblioteca
hoje = datetime.date.today( ) 
ontem = hoje - datetime.timedelta(days=1)
anteontem = hoje + datetime.timedelta(days=-2)

import requests

url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={ontem}&dataFim={ontem}'
print(url) #URL pode ser personalizado com ontem, anteontem ou datas específicas

textos = [] #Criando listas dos textos que serão twittados pelo robô
textos2 = []
textos3 = []
textos4 = []
textos5 = []
textos6 = []
textos7 = []
textos8 = []
textos9 = []
textos10 = []

lista = range(1,50) #páginas que a API retorna
for pagina in lista: #configurando função para cada página
    print(pagina)
    parametros = {'formato': 'json', 'itens': 15, 'pagina': pagina} 
    resposta = requests.get(url, parametros)
    for proposicao in resposta.json()['dados']: #pegando dados das proposições (id, número, ano, tipo, link, etc)
        proposicao_id = proposicao['id'] 
        proposicao_numero = proposicao['numero']
        proposicao_ano = proposicao['ano']
        proposicao_tipo = proposicao['siglaTipo']
        proposicao_link = proposicao['uri']
        parametros = {'formato': 'json'} ]
        proposicao_ementa = proposicao['ementa'] #capturando a ementa das proposições
        response = requests.get(proposicao_link, parametros) 
        dados = response.json()['dados'] #pegando dados da proposição dentro do link dela (inteiro teor e status)
        endereco = dados['urlInteiroTeor']
        situacoes = dados['statusProposicao']
        for situacao in situacoes: #procurando informações sobre o status da proposição (tramitação e situação) 
            tramitacao = situacoes['descricaoTramitacao']
            status = situacoes['descricaoSituacao']
 
        if 'jornada de trabalho' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            texto3 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre jornada de trabalho para mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos3.append(texto3) #colocando textos dentro da lista do que será twittado
            print(texto3)
        elif 'jornada de trabalho' in proposicao_ementa and 'mulher' in proposicao_ementa:
            texto3 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre jornada de trabalho para mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos3.append(texto3) #colocando textos dentro da lista do que será twittado
            print(texto3)
        elif 'violência contra a mulher' in proposicao_ementa:
            texto4 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre violência contra a mulher e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos4.append(texto4) #colocando textos dentro da lista do que será twittado
            print(texto4)
        elif 'violência doméstica' in proposicao_ementa:
            texto4 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre violência doméstica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos4.append(texto4) #colocando textos dentro da lista do que será twittado
            print(texto4)
        elif 'aborto' in proposicao_ementa:
            texto5 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre aborto e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos5.append(texto5) #colocando textos dentro da lista do que será twittado
            print(texto5)
        elif 'violência sexual' in proposicao_ementa:
            texto6 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre violência sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos6.append(texto6) #colocando textos dentro da lista do que será twittado
            print(texto6)
        elif 'feminicídio' in proposicao_ementa:
            texto7 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre feminicídio e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos7.append(texto7) #colocando textos dentro da lista do que será twittado
            print(texto7)
        elif 'assédio sexual' in proposicao_ementa:
            texto8 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre assédio sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos8.append(texto8) #colocando textos dentro da lista do que será twittado
            print(texto8)
        elif 'estupro' in proposicao_ementa:
            texto9 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre estupro e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos9.append(texto9) #colocando textos dentro da lista do que será twittado
            print(texto9)
        elif 'licença maternidade' in proposicao_ementa:
            texto10 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre licença maternidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos10.append(texto10) #colocando textos dentro da lista do que será twittado
            print(texto10)
        elif 'mulheres' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos.append(texto) #colocando textos dentro da lista do que será twittado
            print(texto)
        elif 'mulher' in proposicao_ementa:
            texto2 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano} fala sobre mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos2.append(texto2) #colocando textos dentro da lista do que será twittado
            print(texto2)


# In[2]:
#criando o bot no Twitter

import tweepy, time, sys 
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'XXXXXXXXXXXXXXX'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'XXXXXXXXXXXXX'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'XXXXXXXXXX'#keep the quotes, replace this with your access token
ACCESS_SECRET = XXXXXXXXXXX'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
for texto in textos:
    api.update_status(f'#elasnacamara: {texto}') #twittando 
for texto2 in textos2:
    api.update_status(f'#elasnacamara: {texto2}')#twittando 
for texto3 in textos3:
    api.update_status(f'#elasnacamara: {texto3}') #twittando 
for texto4 in textos4:
    api.update_status(f'#elasnacamara: {texto4}') #twittando 
for texto5 in textos5: 
    api.update_status(f'#elasnacamara: {texto5}') #twittando 
   for texto6 in textos6: 
    api.update_status(f'#elasnacamara: {texto6}') #twittando 
for texto7 in textos7: 
    api.update_status(f'#elasnacamara: {texto7}') #twittando 
for texto8 in textos8: 
    api.update_status(f'#elasnacamara: {texto8}') #twittando 
for texto9 in textos9: 
    api.update_status(f'#elasnacamara: {texto9}') #twittando 
for texto10 in textos10: 
    api.update_status(f'#elasnacamara: {texto10}') #twittando 

