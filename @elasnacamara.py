# coding: utf-8

# In[ ]:

#Variáveis de datas
import datetime #importando biblioteca
hoje = datetime.date.today( ) 
ontem = hoje - datetime.timedelta(days=1)
anteontem = hoje + datetime.timedelta(days=-2)

import requests

url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={anteontem}&dataFim={ontem}&ordem=ASC&ordenarPor=id'
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
textos11 = []
textos12 = []
textos13 = []
textos14 = []
textos15 = []
textos16 = []
textos17 = []
textos18 = []
textos19 = []
textos20 = []
textos21 = []
textos22 = []
textos23 = []
textos24 = []
textos25 = []
textos26 = []
textos27 = []
textos28 = []
textos29 = []
textos30 = []
textos31 = []
textos32 = []
textos33 = []
textos34 = []
textos35 = []
textos36 = []
textos37 = []
textos38 = []
textos39 = []
textos40 = []
textos41 = []
textos42 = []
textos43 = []
textos44 = []
textos45 = []

# Captura quantas páginas tem esse intervalo de data na API
parametros = {'formato': 'json', 'itens': 100}
resposta = requests.get(url, parametros)
    
for vez in resposta.json()['links']:
	conta = {"rel": vez['rel'].strip(), "href": vez['href'].strip()}

# Para este item da API da Câmara sempre o último item link (last) tem o número de páginas
# Considerando 100 itens por página

# Isola o endereço de last
link_ultimo = str(conta['href'].strip())

# Encontra local exato onde termina o número de páginas
posicao = int(link_ultimo.find('&itens='))

# Com um fatiamento de lista, a partir da posição 139 onde sempre está o número, captura o número
# de caracteres que corresponde a "posicao"
# Exemplo: se "posicao" tiver 141 então vai ser [139:141]
# o que significa comprimento de 139 (inclusive) até 141 (exclusive)
# E adiciono mais 1 porque o range abaixo sempre vai um menos
ultima = int(link_ultimo[139:posicao]) + 1
print(ultima)

lista = range(1,ultima)

for pagina in lista: #configurando função para cada página
    parametros = {'formato': 'json', 'itens': 100, 'pagina': pagina} 
    resposta = requests.get(url, parametros)
    print(pagina)
    for proposicao in resposta.json()['dados']: #pegando dados das proposições (id, número, ano, tipo, link, etc)
        proposicao_id = proposicao['id'] 
        proposicao_numero = proposicao['numero']
        proposicao_ano = proposicao['ano']
        proposicao_tipo = proposicao['siglaTipo']
        proposicao_link = proposicao['uri']
        parametros = {'formato': 'json'} 
        proposicao_ementa = proposicao['ementa'] #capturando a ementa das proposições
        response = requests.get(proposicao_link, parametros) 
        dados = response.json()['dados'] #pegando dados da proposição dentro do link dela (inteiro teor e status)
        endereco = dados['urlInteiroTeor']
        situacoes = dados['statusProposicao']
        autores = dados['uriAutores']
        response = requests.get(autores, parametros) 
        parametros = {'formato': 'json'} 
        dados = response.json()['dados'] 
        
        for dado in dados:
            nome = dado['nome']
        
        for situacao in situacoes: #procurando informações sobre o status da proposição (tramitação e situação) 
            tramitacao = situacoes['descricaoTramitacao']
            status = situacoes['descricaoSituacao']
                    
        if 'jornada de trabalho' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            texto3 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre jornada de trabalho para mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos3.append(texto3) #colocando textos dentro da lista do que será twittado
            print(texto3)
        elif 'jornada de trabalho' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print(texto3)
        elif 'violência contra a mulher' in proposicao_ementa:
            texto4 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência contra a mulher e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos4.append(texto4) #colocando textos dentro da lista do que será twittado
            print(texto4)
        elif 'violência doméstica' in proposicao_ementa:
            texto4 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência doméstica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos4.append(texto4) #colocando textos dentro da lista do que será twittado
            print(texto4)
        elif 'aborto' in proposicao_ementa:
            texto5 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre aborto e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos5.append(texto5) #colocando textos dentro da lista do que será twittado
            print(texto5)
        elif 'violência sexual' in proposicao_ementa:
            texto6 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos6.append(texto6) #colocando textos dentro da lista do que será twittado
            print(texto6)
        elif 'feminicídio' in proposicao_ementa:
            texto7 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre feminicídio e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos7.append(texto7) #colocando textos dentro da lista do que será twittado
            print(texto7)
        elif 'assédio sexual' in proposicao_ementa:
            texto8 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre assédio sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos8.append(texto8) #colocando textos dentro da lista do que será twittado
            print(texto8)
        elif 'estupro' in proposicao_ementa:
            texto9 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre estupro e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos9.append(texto9) #colocando textos dentro da lista do que será twittado
            print(texto9)
        elif 'licença maternidade' in proposicao_ementa:
            texto10 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre licença maternidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos10.append(texto10) #colocando textos dentro da lista do que será twittado
            print(texto10)
        elif 'mulheres' in proposicao_ementa or 'mulher' in proposicao_ementa or 'feminino' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos.append(texto) #colocando textos dentro da lista do que será twittado
            print(texto)
        elif 'trabalho doméstico' in proposicao_ementa:
            texto11 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre trabalho doméstico e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos11.append(texto11) #colocando textos dentro da lista do que será twittado
            print(texto11)
        elif 'maria da penha' in proposicao_ementa:
            texto12 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre Lei Maria da Penha e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos12.append(texto12) #colocando textos dentro da lista do que será twittado
            print(texto12)
        elif 'interrupção da gravidez' in proposicao_ementa or 'interrupção da gestação' in proposicao_ementa or 'interrupção de gestação' in proposicao_ementa or 'interrupção de gravidez' in proposicao_ementa:
            texto13 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre interrupção da gravidez e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos13.append(texto13) #colocando textos dentro da lista do que será twittado
            print(texto13)
        elif 'direitos reprodutivos' in proposicao_ementa or 'direito reprodutivo' in proposicao_ementa:
            texto14 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre direitos reprodutivos e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos14.append(texto14) #colocando textos dentro da lista do que será twittado
            print(texto14)
        elif 'direitos à vida' in proposicao_ementa or 'direito à vida' in proposicao_ementa:
            texto15 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre direito à vida e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos15.append(texto15) #colocando textos dentro da lista do que será twittado
            print(texto15)
        elif 'contracepção' in proposicao_ementa or 'contraceptivos' in proposicao_ementa:
            texto16 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre contracepção e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos16.append(texto16) #colocando textos dentro da lista do que será twittado
            print(texto16)
        elif 'violência obstétrica' in proposicao_ementa:
            texto17 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência obstétrica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos17.append(texto17) #colocando textos dentro da lista do que será twittado
            print(texto17)
        elif 'violência obstétrica' in proposicao_ementa:
            texto17 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência obstétrica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos17.append(texto17) #colocando textos dentro da lista do que será twittado
            print(texto17)
        elif 'misoprostol' in proposicao_ementa or 'mifepristone' in proposicao_ementa or 'cytotec' in proposicao_ementa:
            texto18 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre medicamentos abortivos e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos18.append(texto18) #colocando textos dentro da lista do que será twittado
            print(texto18)
        elif 'gestação' in proposicao_ementa or 'gravidez' in proposicao_ementa:
            texto19 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre gravidez e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos19.append(texto19) #colocando textos dentro da lista do que será twittado
            print(texto19)
        elif 'violência familiar' in proposicao_ementa:
            texto20 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência familiar e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos20.append(texto20) #colocando textos dentro da lista do que será twittado
            print(texto20)
        elif 'morte de mulher' in proposicao_ementa or 'morte de mulheres' in proposicao_ementa:
            texto21 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre morte de mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos21.append(texto21) #colocando textos dentro da lista do que será twittado
            print(texto21)
        elif 'homicídio de mulher' in proposicao_ementa or 'homicídio de mulheres' in proposicao_ementa:
            texto22 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre homicídio de mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos22.append(texto22) #colocando textos dentro da lista do que será twittado
            print(texto22)
        elif 'assédio' in proposicao_ementa:
            texto23 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre assédio e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos23.append(texto23) #colocando textos dentro da lista do que será twittado
            print(texto23)
        elif 'estupro de vulnerável' in proposicao_ementa:
            texto24 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre estupro de vulnerável e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos24.append(texto23) #colocando textos dentro da lista do que será twittado
            print(texto24)
        elif 'abuso sexual' in proposicao_ementa:
            texto25 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre abuso sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos25.append(texto25) #colocando textos dentro da lista do que será twittado
            print(texto25)
        elif 'mulher negra' in proposicao_ementa or 'mulheres negras' in proposicao_ementa:
            texto26 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre mulheres negras e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos26.append(texto26) #colocando textos dentro da lista do que será twittado
            print(texto26)
        elif 'maternidade' in proposicao_ementa or 'mãe' in proposicao_ementa:
            texto27 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre maternidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos27.append(texto27) #colocando textos dentro da lista do que será twittado
            print(texto27)
        elif 'amamentação' in proposicao_ementa or 'leite materno' in proposicao_ementa:
            texto28 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre amamentação e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos28.append(texto28) #colocando textos dentro da lista do que será twittado
            print(texto28)
        elif 'feminismo' in proposicao_ementa:
            texto29 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre feminismo e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos29.append(texto29) #colocando textos dentro da lista do que será twittado
            print(texto29)
        elif 'identidade de gênero' in proposicao_ementa:
            texto31 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre identidade de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos31.append(texto31) #colocando textos dentro da lista do que será twittado
            print(texto31)
        elif 'machismo' in proposicao_ementa:
            texto32 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome},fala sobre machismo e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos32.append(texto32) #colocando textos dentro da lista do que será twittado
            print(texto32)
        elif 'guarda de filhos' in proposicao_ementa or 'guarda dos filhos' in proposicao_ementa:
            texto33 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre guarda dos filhos e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'              
            textos33.append(texto33) #colocando textos dentro da lista do que será twittado
            print(texto33)
        elif 'igualdade de gênero' in proposicao_ementa:
            texto34 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre igualdade de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos34.append(texto34) #colocando textos dentro da lista do que será twittado 
            print(texto34)
        elif 'educação sexual' in proposicao_ementa:
            texto35 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre educação sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos35.append(texto35) #colocando textos dentro da lista do que será twittado
            print(texto35)
        elif 'ideologia de gênero' in proposicao_ementa:
            texto36 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre ideologia de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos36.append(texto36) #colocando textos dentro da lista do que será twittado
            print(texto36)
        elif 'transexualidade' in proposicao_ementa or 'transexual' in proposicao_ementa or 'mulher trans' in proposicao_ementa or 'mulheres trans' in proposicao_ementa:
            texto37 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre transexualidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos37.append(texto37) #colocando textos dentro da lista do que será twittado
            print(texto37)
        elif 'mudança de sexo' in proposicao_ementa or 'readequação sexual' in proposicao_ementa:
            texto38 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre readequação sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos38.append(texto38) #colocando textos dentro da lista do que será twittado
            print(texto38)
        elif 'exploração sexual' in proposicao_ementa:
            texto39 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre exploração sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos39.append(texto39) #colocando textos dentro da lista do que será twittado
            print(texto39)
        elif 'prostituição' in proposicao_ementa:
            texto40 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre prostituição e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos40.append(texto40) #colocando textos dentro da lista do que será twittado
            print(texto40)
        elif 'racismo' in proposicao_ementa and 'mulher' in proposicao_ementa:
            texto41 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre racismo e mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos41.append(texto41) #colocando textos dentro da lista do que será twittado
            print(texto41)
        elif 'racismo' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print(texto41)
        elif 'sexualidade' in proposicao_ementa:
            texto42 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre sexualidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos42.append(texto42) #colocando textos dentro da lista do que será twittado
            print(texto42)
        elif 'sexo' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print(texto42)
        elif 'sexo' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print(texto42)
        elif 'Deus' in proposicao_ementa and 'mulher' in proposicao_ementa:
            texto43 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre religiosidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos43.append(texto43) #colocando textos dentro da lista do que será twittado
            print(texto43)
        elif 'Deus' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print(texto43)
        elif 'educação religiosa' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print(texto43)
        elif 'educação religiosa' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print(texto43)
        elif 'religião' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print(texto43)
        elif 'religião' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print(texto43)
        elif 'violênchttps://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio=2020-02-04&dataFim=2020-02-05&ordem=ASC&ordenarPor=idia de gênero' in proposicao_ementa:
            texto44 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos44.append(texto44) #colocando textos dentro da lista do que será twittado
            print(texto44)
        elif 'parto' in proposicao_ementa:
            texto45 = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre parto e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            textos45.append(texto45) #colocando textos dentro da lista do que será twittado
            print(texto45)
            

import tweepy, time, sys 
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'XXXXXXXXXX'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'XXXXXXXXXX'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'XXXXXXXXXX'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'XXXXXXXXXX'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
for texto in textos:
    api.update_status(f'{texto}')
for texto2 in textos2:
    api.update_status(f'{texto2}')
for texto3 in textos3:
    api.update_status(f'{texto3}')
for texto4 in textos4:
    api.update_status(f'{texto4}')
for texto5 in textos5: 
    api.update_status(f'{texto5}')
for texto6 in textos6: 
    api.update_status(f'{texto6}')
for texto7 in textos7: 
    api.update_status(f'{texto7}')
for texto8 in textos8: 
    api.update_status(f'{texto8}')
for texto9 in textos9: 
    api.update_status(f'{texto9}')
for texto10 in textos10: 
    api.update_status(f'{texto10}')
for texto11 in textos11: 
    api.update_status(f'{texto11}')
for texto12 in textos12: 
    api.update_status(f'{texto12}')
for texto13 in textos13: 
    api.update_status(f'{texto13}')
for texto14 in textos14: 
    api.update_status(f'{texto14}')
for texto15 in textos15: 
    api.update_status(f'{texto15}')
for texto16 in textos16: 
    api.update_status(f'{texto16}')
for texto17 in textos17: 
    api.update_status(f'{texto17}')
for texto18 in textos18: 
    api.update_status(f'{texto18}')
for texto19 in textos19: 
    api.update_status(f'{texto19}')
for texto20 in textos20: 
    api.update_status(f'{texto20}')
for texto21 in textos21: 
    api.update_status(f'{texto21}')
for texto22 in textos22: 
    api.update_status(f'{texto22}')
for texto23 in textos23: 
    api.update_status(f'{texto23}')
for texto24 in textos24: 
    api.update_status(f'{texto24}')
for texto25 in textos25: 
    api.update_status(f'{texto25}')
for texto26 in textos26: 
    api.update_status(f'{texto26}')
for texto27 in textos27: 
    api.update_status(f'{texto27}')
for texto28 in textos28: 
    api.update_status(f'{texto28}')
for texto29 in textos29: 
    api.update_status(f'{texto29}')
for texto30 in textos30: 
    api.update_status(f'{texto30}')
for texto31 in textos31: 
    api.update_status(f'{texto31}')
for texto32 in textos32: 
    api.update_status(f'{texto32}')
for texto33 in textos33: 
    api.update_status(f'{texto33}')
for texto34 in textos34: 
    api.update_status(f'{texto34}')
for texto35 in textos35: 
    api.update_status(f'{texto35}')
for texto36 in textos36: 
    api.update_status(f'{texto36}')
for texto37 in textos37: 
    api.update_status(f'{texto37}')
for texto38 in textos38: 
    api.update_status(f'{texto38}')
for texto39 in textos39: 
    api.update_status(f'{texto39}')
for texto40 in textos40: 
    api.update_status(f'{texto40}')
for texto41 in textos41: 
    api.update_status(f'{texto41}')
for texto42 in textos42: 
    api.update_status(f'{texto42}')
for texto43 in textos43: 
    api.update_status(f'{texto43}')
for texto44 in textos44: 
    api.update_status(f'{texto44}')
for texto45 in textos45: 
    api.update_status(f'{texto45}')    
            
