import unittest
import normalize_tweets as n

class TestSum(unittest.TestCase):
    def test_text(self):
        self.assertEqual(n.norm(' tem trim '), 'tem trim')

        self.assertEqual(n.norm(
            'CÂMARA: PL 2753/2020, de autoria de Erika santos de souza Patrus Ananias de foo barPatrus Ananias de foo barPatrus Ananias de foo bar, fala sobre crianças e sofreu alterações em sua tramitação. Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093 '),
            'CÂMARA: PL 2753/2020, de autoria de Erika santos de…, fala sobre crianças e sofreu alterações em sua tramitação. Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093')

        self.assertEqual(n.norm(
            'CÂMARA: PL 2753/2020, de autoria de Erika santos de souza Patrus Ananias de foo barPatrus Ananias de foo barPatrus, Outro nome, mais um nome, fala sobre crianças e sofreu alterações em sua tramitação. Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093 '),
            'CÂMARA: PL 2753/2020, de autoria de Erika santos de… e outros(as), fala sobre crianças e sofreu alterações em sua tramitação. Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093')

        self.assertEqual(n.norm(
            'CÂMARA: PL 2753/2020 tweet grande demais pra caber no tweet vai ser cortado onde nos autores, de autoria de fulano, fala sobre crianças e sofreu alterações em sua tramitação. Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093 '),
            'CÂMARA: PL 2753/2020 tweet grande demais pra caber no tweet vai ser cortado onde nos autores, Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093')

        self.assertEqual(n.norm(
            'CÂMARA: PL 2753/2020 outros campo grandes demais, de autoria de qualquer texto aqui tambem vai ser cortado caso nao tenha como ir até oSofreAlteracoes sofreu alterações em sua tramitação. Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093 '),
            'CÂMARA: PL 2753/2020 outros campo grandes demais, Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093')

if __name__ == '__main__':
    unittest.main()
