# Data Pirate

The goal to this project is to collect data from Correios website. In order to do so, a web crawler using Python 3 and Scrapy is being used.


### Running The Project

To see the magic happening, first of all you need to install all the requirements needed. To do so, open your terminal in the root of this project and type:

> pip install -r requirements.txt.

The next step is to run the spider to get the data. In your terminal type:

> scrapy crawl mail -o mail.jl

This command will generate a JSONL file in the root of the project named mail.jl and it will contain all the info the crawled got.



### Tests

To run unit tests just open your terminal in the root of the project and type:

>python -m unittest data_pirate/tests/test_mail.py

this will run the tests concerning the mail spider :)

### PS.: It's highly recomended to use a Python3 virtual environmnet 

In case you choose not to do so, you can run your tests with 

>python3 -m unittest data_pirate/tests/test_mail.py