import unittest
from data_pirate.spiders import mail_spider
from data_pirate.tests.responses import mock_response

home_url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm'
result_url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'

class MailSpiderTest(unittest.TestCase):
    
    def setUp(self):
        self.spider = mail_spider.MailSpider()

    def _test_item_results(self, results):
        for item in results:
            self.assertIsNotNone(item['id'])
            self.assertIsNotNone(item['localidade'])
            self.assertIsNotNone(item['faixa de cep'])
    
    def _test_result_length(self, results):
        results_length = len(results)
        expected_length = 23
        self.assertEqual(results_length, expected_length)

    def test_parse_result_page(self):
        page_results = list(self.spider.parse_content_page(mock_response('mail_result_mock.html',result_url)))
        
        self._test_result_length(page_results)
        self._test_item_results(page_results)
    
    def test_parse_home_page_requests(self):
        home_results = list(self.spider.parse(mock_response('mail_home_mock.html', home_url)))

        for item in home_results:
            body= item.body
            body_parsed = body.decode("UTF-8")
            body_uf = body_parsed.split('UF=')[1]

            self.assertIsNotNone(body_uf)
            self.assertEqual(item.method, 'POST')
            self.assertEqual(item.url, result_url)
            self.assertIsNotNone(item.body)
