import logging
import os
import scrapy
from scrapy.spiders import XMLFeedSpider
from scrapy.exporters import CsvItemExporter
import redis
from datetime import datetime, timedelta
from .theme_assert import assert_theme

DATA_DIR = os.environ.get("DATA_DIR", "/data")
LOG_DIR = os.environ.get("LOG_DIR", "/logs")

"""
This is the spider (https://docs.scrapy.org/en/latest/topics/spiders.html)
that scrapes the data for the Senado (upper chamber).
"""

BASE_URL = "http://legis.senado.leg.br/dadosabertos/materia/tramitando?data={}"


class SenadoSpider(XMLFeedSpider):
    "Definition of basic configs of the Spider and the rules for its iterations"

    name = "senado"
    allowed_domains = ["legis.senado.leg.br"]
    iterator = "iternodes"
    itertag = "Materia"

    def __init__(self, date_from=None, date_to=None, *args, **kwargs):
        "Init using Redis for caching and savepoint, and also versioning the output file with the current YMD."
        super().__init__(*args, **kwargs)
        yesterday = datetime.now() - timedelta(1)
        self.date_from = datetime.strptime(date_from, "%Y-%m-%d") if date_from else yesterday
        self.date_to = datetime.strptime(date_to, "%Y-%m-%d") if date_to else yesterday

        current_date = datetime.now().strftime("%Y%m%d")
        self.file = open(os.path.join(DATA_DIR, f"senado_{current_date}.csv"), "wb")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
        self.items_exported = 0
        self.items_seen = 0
        self.redis = redis.Redis(host="redis", port=6379, db=0)

        log_handler = logging.FileHandler(
            os.path.join(LOG_DIR, f"senado_{current_date}.log")
        )
        log_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
        )
        logging.getLogger().addHandler(log_handler)

    def start_requests(self):
        "Logs the execution plan and generates one request per day in the date range."
        total_days = (self.date_to - self.date_from).days + 1
        logging.info(
            "[senado] Plano de execução:\n"
            "  Período : %s → %s\n"
            "  Dias    : %d\n"
            "  Janela  : 1 dia por requisição",
            self.date_from.strftime("%Y-%m-%d"),
            self.date_to.strftime("%Y-%m-%d"),
            total_days,
        )
        current = self.date_from
        while current <= self.date_to:
            day_str = current.strftime("%Y%m%d")
            yield scrapy.Request(BASE_URL.format(day_str), callback=self._parse)
            current += timedelta(1)

    def parse_node(self, response, node):
        """
        The first endpoint required for scraping the Senado data.
        Using retries and redis.
        The Senado API uses XML.
        """
        tries = 1
        try:
            item = dict()
            item["id"] = node.xpath(
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

            item["UrlTramitacao"] = (
                f"https://www25.senado.leg.br/web/atividade/materias/-/materia/{item['id']}"
            )

            self.items_seen += 1
            theme_assertion = assert_theme({"Ementa": item["Ementa"]})
            if theme_assertion["row_relevant"]:
                item["temas"] = ", ".join(theme_assertion["temas"])

                current_date = datetime.now().isoformat()
                self.redis.set(
                    "savepoint_senado", f'{item["id"]}, {current_date}'
                )

                row_url = f"https://legis.senado.leg.br/dadosabertos/materia/{item['id']}"
                row_request = scrapy.Request(row_url, callback=self.parse_row_data)
                row_request.meta["item"] = item
                yield row_request

        except Exception:
            logging.info(f"Erro ao processar linha, tentativa: {tries}")
            self.redis.set(
                f'savepoint_senado_erro:{item["id"]}', f"{current_date}"
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
        movements_request = scrapy.Request(movements_url, callback=self.parse_movements)
        movements_request.meta["item"] = item
        yield movements_request

    def parse_movements(self, reponse):
        item = reponse.meta["item"]

        item["MovimentacaoDescricaoSituacao"] = reponse.xpath(
            "//SituacaoAtual/DescricaoSituacao/text()"
        ).extract_first()
        item["MovimentacaoDescricao"] = reponse.xpath(
            "//InformeLegislativo/Descricao/text()"
        ).extract_first()

        self.items_exported += 1
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        total_days = (self.date_to - self.date_from).days + 1
        logging.info(
            "[senado] Resumo da execução:\n"
            "  Período    : %s → %s (%d dia(s))\n"
            "  Matérias vistas     : %d\n"
            "  Matérias exportadas : %d (filtro temático)\n"
            "  Arquivo de saída    : %s",
            self.date_from.strftime("%Y-%m-%d"),
            self.date_to.strftime("%Y-%m-%d"),
            total_days,
            self.items_seen,
            self.items_exported,
            self.file.name,
        )
