import scrapy
from scrapy.spiders import XMLFeedSpider
from scrapy.exporters import CsvItemExporter
import redis
from datetime import datetime, timedelta
from .theme_assert import assert_theme

"""
This is the spider (https://docs.scrapy.org/en/latest/topics/spiders.html)
that scrapes the data for the Senado (upper chamber).
"""


class SenadoSpider(XMLFeedSpider):
    "Definition of basic configs of the Spider and the rules for its iterations"

    dia_anterior = (datetime.now() - timedelta(1)).strftime("%d")
    mes_anterior = (datetime.now() - timedelta(1)).strftime("%m")
    ano_anterior = (datetime.now() - timedelta(1)).strftime("%Y")
    url = "http://legis.senado.leg.br/dadosabertos/materia/tramitando?data=%s%s%s" % (
        ano_anterior,
        mes_anterior,
        dia_anterior,
    )
    name = "senado"
    allowed_domains = ["legis.senado.leg.br"]
    start_urls = [url]
    iterator = "iternodes"
    itertag = "Materia"

    def __init__(self):
        "Init using Redis for caching and savepoint, and also versioning the output file with the current YMD."
        current_date = datetime.now().strftime("%Y%m%d")
        self.file = open(f"senado_{current_date}.csv", "wb")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
        self.redis = redis.Redis(host="redis", port=6379, db=0)

    def parse_node(self, response, node):
        """
        The first endpoint required for scraping the Senado data.
        Using retries and redis.
        The Senado API uses XML.
        """
        tries = 1
        try:
            item = dict()
            item["CodigoMateria"] = node.xpath(
                "IdentificacaoMateria/CodigoMateria/text()"
            ).extract_first()
            item["SiglaCasaIdentificacaoMateria"] = node.xpath(
                "IdentificacaoMateria/SiglaCasaIdentificacaoMateria/text()"
            ).extract_first()
            item["NomeCasaIdentificacaoMateria"] = node.xpath(
                "IdentificacaoMateria/NomeCasaIdentificacaoMateria/text()"
            ).extract_first()
            item["SiglaSubtipoMateria"] = node.xpath(
                "IdentificacaoMateria/SiglaSubtipoMateria/text()"
            ).extract_first()
            item["NumeroMateria"] = node.xpath(
                "IdentificacaoMateria/NumeroMateria/text()"
            ).extract_first()
            item["AnoMateria"] = node.xpath(
                "IdentificacaoMateria/AnoMateria/text()"
            ).extract_first()
            item["IdentificacaoProcesso"] = node.xpath(
                "IdentificacaoMateria/IdentificacaoProcesso/text()"
            ).extract_first()
            item["NomedoProjeto"] = node.xpath(
                "IdentificacaoMateria/DescricaoIdentificacaoMateria/text()"
            ).extract_first()
            item["IndicadorTramitando"] = node.xpath(
                "IdentificacaoMateria/IndicadorTramitando/text()"
            ).extract_first()
            item["Ementa"] = node.xpath("Ementa/text()").extract_first()
            item["Autor"] = node.xpath("Autor/text()").extract_first()
            item["DataApresentacao"] = node.xpath(
                "DataApresentacao/text()"
            ).extract_first()
            item["DataDaTramitação"], item["HoraDaTramitação"] = (
                node.xpath("DataUltimaAtualizacao/text()")
                .extract_first(default="")
                .split(" ")
            )

            "Colunas/Dados construídos com concatenação"
            item["UrlTramitacao"] = (
                f"https://www25.senado.leg.br/web/atividade/materias/-/materia/{item['CodigoMateria']}"
            )

            theme_assertion = assert_theme({"Ementa": item["Ementa"]})
            if theme_assertion["row_relevant"]:
                item["temas"] = ", ".join(theme_assertion["temas"])

                current_date = datetime.now().isoformat()
                self.redis.set(
                    "savepoint_senado", f'{item["CodigoMateria"]}, {current_date}'
                )

                row_url = f"https://legis.senado.leg.br/dadosabertos/materia/{item['CodigoMateria']}"
                row_request = scrapy.Request(row_url, callback=self.parse_row_data)
                row_request.meta["item"] = item
                yield row_request

        except Exception:
            logging.info(f"Erro ao processar linha, tentativa: {tries}")
            self.redis.set(
                f'savepoint_senado_erro:{item["CodigoMateria"]}', f"{current_date}"
            )
            if tries < 3:
                tries += 1
                yield scrapy.Request(
                    response.url, callback=self.parse_node, dont_filter=True
                )

    def parse_row_data(self, response):
        item = response.meta["item"]

        item["ApelidoMateria"] = response.xpath(
            "//ApelidoMateria/text()"
        ).extract_first()
        item["Autor"] = response.xpath("//Autor/text()").extract_first()
        item["CasaIniciadoraNoLegislativo"] = response.xpath(
            "//CasaIniciadoraNoLegislativo/text()"
        ).extract_first()
        item["NumeroRepublicacaoMpv"] = response.xpath(
            "//NumeroRepublicacaoMpv/text()"
        ).extract_first()
        item["IndicadorComplementar"] = response.xpath(
            "//IndicadorComplementar/text()"
        ).extract_first()
        item["DataApresentacao"] = response.xpath(
            "//DataApresentacao/text()"
        ).extract_first()
        item["DataAssinatura"] = response.xpath(
            "//DataAssinatura/text()"
        ).extract_first()
        item["AssuntoEspecificoCod"] = response.xpath(
            "Assunto/AssuntoEspecifico/Codigo"
        ).extract_first()
        item["AssuntoEspecificoDesc"] = response.xpath(
            "Assunto/AssuntoEspecifico/Descricao"
        ).extract_first()
        item["AssuntoGeralCod"] = response.xpath(
            "Assunto/AssuntoGeral/Codigo"
        ).extract_first()
        item["AssuntoGeralDesc"] = response.xpath(
            "Assunto/AssuntoGeral/Descricao"
        ).extract_first()

        movements_url = response.xpath(
            '//Servico[NomeServico="MovimentacaoMateria"]/UrlServico/text()'
        ).extract_first()

        # Get author identification to fetch details
        autor_id = response.xpath('//Autor/IdentificacaoParlamentar/CodigoParlamentar/text()').extract_first()
        if autor_id:
            author_url = f"https://legis.senado.leg.br/dadosabertos/senador/{autor_id}"
            sexo, partido = scrapy.Request(author_url, callback=self.parse_author_details)
        else:
            sexo = None
            partido = None

        item["AutorSexo"] = sexo
        item["AutorPartido"] = partido

        movements_request = scrapy.Request(movements_url, callback=self.parse_movements)
        movements_request.meta["item"] = item
        yield movements_request

    def parse_author_details(self, response):
        item = response.meta["item"]

        return [response.xpath('//Parlamentar/SexoParlamentar/text()').extract_first(), 
                response.xpath('//Parlamentar/SiglaPartidoParlamentar/text()').extract_first()]

    def parse_movements(self, reponse):
        item = reponse.meta["item"]

        item["MovimentacaoDescricaoSituacao"] = reponse.xpath(
            "//SituacaoAtual/DescricaoSituacao/text()"
        ).extract_first()
        item["MovimentacaoDescricao"] = reponse.xpath(
            "//InformeLegislativo/Descricao/text()"
        ).extract_first()

        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
