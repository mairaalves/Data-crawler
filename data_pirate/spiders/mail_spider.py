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
                callback=self.parse_content_page,
                cb_kwargs= dict(uf=uf, index=0)
            )
        
    def parse_content_page(self, response, uf, index):
        table_list = response.css('table.tmptabela')
        table = table_list[0]

        if len(table_list) == 2:
            table = table_list[1]

        table_items = table.css('tr')
        table_items = table_items[1:]
        
        result_url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/ResultadoBuscaFaixaCEP.cfm'
        next_page_form = response.css('[name="Proxima"] input::attr(value)').getall()

        for item in table_items:
            index = index + 1
            yield {
                'id': f'{uf}-{index}',
                'localidade': item.css('td::text').get(),
                'faixa de cep': item.css('td:nth-child(2)::text').get()
            }

        if len(next_page_form) > 0:
            yield scrapy.FormRequest.from_response(
                response,
                url = result_url,
                formdata={
                    'UF': uf, 'Localidade': next_page_form[1],
                    'Bairro': next_page_form[2], 'qtdrow': next_page_form[3],
                    'pagini': next_page_form[4], 'pagfim': next_page_form[5]
                },   
                callback=self.parse_content_page,
                cb_kwargs= dict(uf=uf, index=index)
            )
