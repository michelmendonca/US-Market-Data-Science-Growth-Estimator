# project1_cars

@author: Michel Mendonca

Web scrapped originally from:

URL: https://carsalesbase.com/car-sales-us-home-main/car-sales-by-brand-us/

===========================================================================
Packages used
===========================================================================

import scrapy
import itertools
from itertools import chain
import csv
import pandas as pd

===========================================================================
Web scraping code 
===========================================================================

class project1_carsSpider(scrapy.Spider):
    name = 'project1_cars_ford'
    allowed_domains = ['Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)']
    start_urls = ['https://carsalesbase.com/us-ford/']

    def parse(self, response):
        # table : id = "table_3"
        # class_ : "responsive display nowrap data-t data-t wpDataTable dataTable no-footer"

        rows = response.css("table")[1].css('tr') # the first .css looks for the table we want and the secound .css looks for the rows
        row = rows.css('td').css('::text').getall()
       
======================================================
Data Cleaning
======================================================
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
        
f = open("ford.csv", "r")
#print(f.read())

header_names = ['Year', 'Sales', 'Growth', 'Market_Share']
ford_table = pd.read_csv("ford.csv", header=None, names = header_names)
print(ford_table)

====================================================
Saving data.csv
====================================================

ford_table.to_csv("Ford_us.csv")




