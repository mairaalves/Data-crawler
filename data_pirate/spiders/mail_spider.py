import scrapy
from scrapy.http import FormRequest


class MailSpider(scrapy.Spider):
    name = "mail"
    start_urls = [
        'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm',
    ]

    def parse(self, response):
        ufs = response.css('select option::text').getall()
        ufs.pop(0)

        for uf in ufs:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'UF': uf},
                callback=self.parse_content_page
            )
        
    def parse_content_page(self, response):
        counter = 0
        uf = response.css('table.tmptabela tr td::text').get()
        table = response.css('table.tmptabela')[1]
        table_items = table.css('tr')
        table_items = table_items[2:]
        
        for item in table_items:
            counter = counter + 1
            yield {
                'id': f'{uf}-{counter}',
                'localidade': item.css('td::text').get(),
                'faixa de cep': item.css('td:nth-child(2)::text').get()
            }


