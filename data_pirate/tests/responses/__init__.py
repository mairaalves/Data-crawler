import os
from scrapy.http import Response, Request,HtmlResponse

def mock_response(mock_file, url):
    if not mock_file[0] == '/':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, mock_file)
    else:
        file_path = mock_file

    request = Request(url=url)

    mock = open(file_path, 'r').read()

    response = HtmlResponse(url=url,
        request=request,
        body=mock,
        encoding='utf-8')

    return response
