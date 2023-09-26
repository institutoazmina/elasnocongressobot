import scrapy
from scrapy.spiders import XMLFeedSpider
from scrapy.exporters import CsvItemExporter
import redis
# import datetime
from datetime import datetime, timedelta
from .theme_assert import assert_theme

class CamaraSpider(XMLFeedSpider):
    # Captura o dia, mês e ano de ontem
    dia_anterior = (datetime.now() - timedelta(1)).strftime('%d')
    mes_anterior = (datetime.now() - timedelta(1)).strftime('%m')
    ano_anterior = (datetime.now() - timedelta(1)).strftime('%Y')

    # Captura o dia, mês e ano de amanha (assim nao preciso mudar o codigo para remover o parametro data_ate)
    now = datetime.now()
    dia_hoje = (datetime.now() + timedelta(1)).strftime('%d')
    mes_hoje = (datetime.now() + timedelta(1)).strftime('%m')
    ano_hoje = (datetime.now() + timedelta(1)).strftime('%Y')

    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio=%s-%s-%s&dataFim=%s-%s-%s&ordem=ASC&ordenarPor=id&itens=100" % (ano_anterior, mes_anterior, dia_anterior, ano_hoje, mes_hoje, dia_hoje)

    name = 'camara'
    allowed_domains = ['dadosabertos.camara.leg.br']
    start_urls = [url]
    iterator = 'iternodes'
    itertag = 'proposicao_'

    def __init__(self):
        self.file = open("camara.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
        self.redis = redis.Redis(host='redis', port=6379, db=0)

    def parse_node(self, response, node):
        tries = 1
        try:
            item = dict()
            item['id'] = node.xpath('id/text()').extract_first()
            item['uri'] = node.xpath('uri/text()').extract_first()
            item['siglaTipo'] = node.xpath('siglaTipo/text()').extract_first()
            item['codTipo'] = node.xpath('codTipo/text()').extract_first()
            item['numero'] = node.xpath('numero/text()').extract_first()
            item['ano'] = node.xpath('ano/text()').extract_first()
            item['ementa'] = node.xpath('ementa/text()').extract_first()

            current_date = datetime.now().isoformat()
            self.redis.set(f'savepoint_camara', f'{item["id"]}, {current_date}, {item["uri"]}')

            row_request = scrapy.Request(item['uri'], callback=self.parse_row_data)
            row_request.meta['item'] = item
            yield row_request

            next_page_url = response.xpath('//link[rel="next"]/href/text()').extract_first()
            if next_page_url:
                yield scrapy.Request(next_page_url, callback=self.parse_next_page)

        except:
            print(f'Erro ao processar linha, tentativa: {tries}')
            self.redis.set(f'savepoint_camara_erro:{item["id"]}', f'{current_date}, {item["uri"]}')
            if (tries < 3):
                tries += 1
                yield scrapy.Request(response.url, callback=self.parse_node, dont_filter=True)

    def parse_row_data(self, response): 
        item = response.meta['item']
        
        item['dataApresentacao'] = response.xpath('//dados/dataApresentacao/text()').extract_first()
        item['uriOrgaoNumerador'] = response.xpath('//dados/uriOrgaoNumerador/text()').extract_first()
        item['uriAutores'] = response.xpath('//dados/uriAutores/text()').extract_first()
        item['descricaoTipo'] = response.xpath('//dados/descricaoTipo/text()').extract_first()
        item['ementaDetalhada'] = response.xpath('//dados/ementaDetalhada/text()').extract_first()
        item['keywords'] = response.xpath('//dados/keywords/text()').extract_first()
        item['uriPropPrincipal'] = response.xpath('//dados/uriPropPrincipal/text()').extract_first()
        item['uriPropAnterior'] = response.xpath('//dados/uriPropAnterior/text()').extract_first()
        item['uriPropPosterior'] = response.xpath('//dados/uriPropPosterior/text()').extract_first()
        item['urlInteiroTeor'] = response.xpath('//dados/urlInteiroTeor/text()').extract_first()
        item['urnFinal'] = response.xpath('//dados/urnFinal/text()').extract_first()
        item['texto'] = response.xpath('//dados/texto/text()').extract_first()
        item['justificativa'] = response.xpath('//dados/justificativa/text()').extract_first()

        ## Dados de tramitação
        item['dataHora'] = response.xpath('//dados/statusProposicao/dataHora/text()').extract_first()
        item['sequencia'] = response.xpath('//dados/statusProposicao/sequencia/text()').extract_first()
        item['siglaOrgao'] = response.xpath('//dados/statusProposicao/siglaOrgao/text()').extract_first()
        item['uriOrgao'] = response.xpath('//dados/statusProposicao/uriOrgao/text()').extract_first()
        item['uriUltimoRelator'] = response.xpath('//dados/statusProposicao/uriUltimoRelator/text()').extract_first()
        item['regime'] = response.xpath('//dados/statusProposicao/regime/text()').extract_first()
        item['descricaoTramitacao'] = response.xpath('//dados/statusProposicao/descricaoTramitacao/text()').extract_first()
        item['codTipoTramitacao'] = response.xpath('//dados/statusProposicao/codTipoTramitacao/text()').extract_first()
        item['descricaoSituacao'] = response.xpath('//dados/statusProposicao/descricaoSituacao/text()').extract_first()
        item['codSituacao'] = response.xpath('//dados/statusProposicao/codSituacao/text()').extract_first()
        item['despacho'] = response.xpath('//dados/statusProposicao/despacho/text()').extract_first()
        item['url'] = response.xpath('//dados/statusProposicao/url/text()').extract_first()
        item['ambito'] = response.xpath('//dados/statusProposicao/ambito/text()').extract_first()
        item['apreciacao'] = response.xpath('//dados/statusProposicao/apreciacao/text()').extract_first()

        theme_assertion = assert_theme({"ementa": item['ementa'], "ementaDetalhada": item['ementaDetalhada']})
        if theme_assertion['row_relevant']:
            item['temas'] = ', '.join(theme_assertion['temas'])

            authors_request = scrapy.Request(item['uriAutores'], callback=self.parse_authors)
            authors_request.meta['item'] = item
            return authors_request

    def parse_authors(self, response):
        item = response.meta['item']

        item['nome'] = response.xpath('//autor/nome/text()').extract_first()
        item['tipo'] = response.xpath('//autor/tipo/text()').extract_first()

        self.exporter.export_item(item)
        return item

    def parse_next_page(self, response):
        for node in response.xpath('//proposicao_'):
            yield from self.parse_node(response, node)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()