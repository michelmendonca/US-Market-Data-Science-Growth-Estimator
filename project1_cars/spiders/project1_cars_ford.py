import scrapy
import itertools
from itertools import chain
import csv
import pandas as pd

# to call the crawler from terminal type the line below
# scrapy crawl ffcountry -L WARN
#scrapy crawl ffcountry -L WARN -o document.csv

class project1_carsSpider(scrapy.Spider):
    name = 'project1_cars_ford'
    allowed_domains = ['Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)']
    start_urls = ['https://carsalesbase.com/us-ford/']

    def parse(self, response):
        # table : id = "table_3"
        # class_ : "responsive display nowrap data-t data-t wpDataTable dataTable no-footer"

        rows = response.css("table")[1].css('tr') # the first .css looks for the table we want and the secound .css looks for the rows
        row = rows.css('td').css('::text').getall()
        n = 4
        splited = [row[i::n] for i in range(n)]

        year = splited[3]
        sales = splited[0][1:]
        growth = splited[1][1:]
        market_share = splited[2][1:]

        zippedlist = list(zip(year, sales, growth, market_share))
        #toyota_table = pd.DataFrame(zippedlist, columns = ["Year", "Age", "Growth", "Market_Share"])
        #print(zippedlist)
        f = open('ford.csv', 'w')
        with f:
            writer = csv.writer(f)
            writer.writerows(zippedlist)

        #print(splited)
