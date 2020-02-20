# coding: utf-8

# In[ ]:

#importando bibliotecas
import datetime # datas
import requests # http
import shelve   # cache em disco de dicionarios
import json     # escrever JSON
import os.path  # paths do sistema

if not os.path.exists('dados/.dummy'):
    print("Faltando pasta ./dados/ (arquivo .dummy nao existe)")
    raise

#Variáveis de datas
hoje = datetime.date.today( )
ontem = hoje - datetime.timedelta(days=1)
anteontem = hoje + datetime.timedelta(days=-2)

url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={anteontem}&dataFim={ontem}&ordem=ASC&ordenarPor=id'
print(url) #URL pode ser personalizado com ontem, anteontem ou datas específicas

textos = [] #Criando listas dos textos que serão twittados pelo robô

autores_cache = shelve.open('dados/autores.shelf')

pagina = 0
while True:
    pagina += 1 # soma um no contador da pagina
    #configurando função para cada página
    parametros = {'formato': 'json', 'itens': 100, 'pagina': pagina}
    print("Buscando página", pagina, "...")

    resposta_json = requests.get(url, parametros).json()

    if (len(resposta_json['dados']) == 0):
        print ("Nenhuma nova proposicao na pagina", pagina)
        break;

    for proposicao in resposta_json['dados']: #pegando dados das proposições (id, número, ano, tipo, link, etc)
        proposicao_id = proposicao['id']
        proposicao_numero = proposicao['numero']
        proposicao_ano = proposicao['ano']
        proposicao_tipo = proposicao['siglaTipo']
        proposicao_link = proposicao['uri']
        parametros = {'formato': 'json'}
        proposicao_ementa = proposicao['ementa'] #capturando a ementa das proposições

        print ("Buscando proposicao", proposicao_id, f'GET {proposicao_link}')
        response = requests.get(proposicao_link, parametros)
        dados = response.json()['dados'] #pegando dados da proposição dentro do link dela (inteiro teor e status)
        endereco = dados['urlInteiroTeor']
        situacoes = dados['statusProposicao']
        autores = dados['uriAutores']

        if autores in autores_cache:
            print ("author ja existe no cache!")
            nome = autores_cache[autores]
        else:
            parametros = {'formato': 'json'}
            response = requests.get(autores, parametros)
            print ("-> GET", autores)
            dados = response.json()['dados']
            for dado in dados:
                nome = dado['nome']
            autores_cache[autores] = nome

        for situacao in situacoes: #procurando informações sobre o status da proposição (tramitação e situação)
            tramitacao = situacoes['descricaoTramitacao']
            status = situacoes['descricaoSituacao']

        tweets_proposicao = []

        if 'jornada de trabalho' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre jornada de trabalho para mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto) #colocando textos dentro da lista do que será twittado
        elif 'jornada de trabalho' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print("tweet nao configurado: 'jornada de trabalho' & 'mulher'")
        elif 'violência contra a mulher' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência contra a mulher e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'violência doméstica' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência doméstica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'aborto' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre aborto e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'violência sexual' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'feminicídio' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre feminicídio e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'assédio sexual' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre assédio sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'estupro' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre estupro e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'licença maternidade' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre licença maternidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'mulheres' in proposicao_ementa or 'mulher' in proposicao_ementa or 'feminino' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'trabalho doméstico' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre trabalho doméstico e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'maria da penha' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre Lei Maria da Penha e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'interrupção da gravidez' in proposicao_ementa or 'interrupção da gestação' in proposicao_ementa or 'interrupção de gestação' in proposicao_ementa or 'interrupção de gravidez' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre interrupção da gravidez e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'direitos reprodutivos' in proposicao_ementa or 'direito reprodutivo' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre direitos reprodutivos e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'direitos à vida' in proposicao_ementa or 'direito à vida' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre direito à vida e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'contracepção' in proposicao_ementa or 'contraceptivos' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre contracepção e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'violência obstétrica' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência obstétrica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'violência obstétrica' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência obstétrica e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'misoprostol' in proposicao_ementa or 'mifepristone' in proposicao_ementa or 'cytotec' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre medicamentos abortivos e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'gestação' in proposicao_ementa or 'gravidez' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre gravidez e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'violência familiar' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência familiar e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'morte de mulher' in proposicao_ementa or 'morte de mulheres' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre morte de mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'homicídio de mulher' in proposicao_ementa or 'homicídio de mulheres' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre homicídio de mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'assédio' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre assédio e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'estupro de vulnerável' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre estupro de vulnerável e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'abuso sexual' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre abuso sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'mulher negra' in proposicao_ementa or 'mulheres negras' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre mulheres negras e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'maternidade' in proposicao_ementa or 'mãe' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre maternidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'amamentação' in proposicao_ementa or 'leite materno' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre amamentação e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'feminismo' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre feminismo e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'identidade de gênero' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre identidade de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'machismo' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome},fala sobre machismo e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'guarda de filhos' in proposicao_ementa or 'guarda dos filhos' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre guarda dos filhos e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'igualdade de gênero' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre igualdade de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'educação sexual' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre educação sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'ideologia de gênero' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre ideologia de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'transexualidade' in proposicao_ementa or 'transexual' in proposicao_ementa or 'mulher trans' in proposicao_ementa or 'mulheres trans' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre transexualidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'mudança de sexo' in proposicao_ementa or 'readequação sexual' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre readequação sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'exploração sexual' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre exploração sexual e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'prostituição' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre prostituição e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'racismo' in proposicao_ementa and 'mulher' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre racismo e mulheres e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'racismo' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print("tweet nao configurado: 'racismo' & 'mulheres'")
        elif 'sexualidade' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre sexualidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'sexo' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print("tweet nao configurado: 'sexo' & 'mulher'")
        elif 'sexo' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print("tweet nao configurado: 'sexo' & 'mulheres'")
        elif 'Deus' in proposicao_ementa and 'mulher' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre religiosidade e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'Deus' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print("tweet nao configurado: 'Deus' & 'mulheres'")
        elif 'educação religiosa' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print("tweet nao configurado: 'educação' religiosa '&' mulher")
        elif 'educação religiosa' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print("tweet nao configurado: 'educação' religiosa '&' mulheres")
        elif 'religião' in proposicao_ementa and 'mulher' in proposicao_ementa:
            print("tweet nao configurado: 'religião' & 'mulher'")
        elif 'religião' in proposicao_ementa and 'mulheres' in proposicao_ementa:
            print("tweet nao configurado: 'religião' & 'mulheres'")
        elif 'violência de gênero' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre violência de gênero e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)
        elif 'parto' in proposicao_ementa:
            texto = f'{proposicao_tipo} {proposicao_numero}/{proposicao_ano}, de autoria de {nome}, fala sobre parto e sofreu alterações em sua tramitação. Tramitação: {tramitacao}. Situação: {status}. {endereco}'
            tweets_proposicao.append(texto)

        if (len(tweets_proposicao) > 0):
            print("tweets para proposicao ID=", proposicao_id)
            for tweet in tweets_proposicao:
                print("Novo tweet:", tweet)
                textos.append( { "tweet": tweet, "proposicao_id": proposicao_id} )

print ("Total de proposicoes: ", str(len(textos)))

with open('dados/tweets.json', 'w') as outfile:
    json.dump(textos, outfile)

print ("Arquivo dados/tweets.json atualizado com sucesso")