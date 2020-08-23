## Data Science Growth Estimator: Project Overview

- Created a tool that estimates data science growth between three of the biggest car companies in the US, Ford, GM, and Toyota plus a new player with promising future, Tesla. (BestEstimator = RandomForest - MAE ~ 5.71%).
- Scraped four tables from URL: https://carsalesbase.com/car-sales-us-home-main/car-sales-by-brand-us/, where I had to use Scrapy due to lack of formating of BeautifulSoup. I also tried Pandas, but the site was blocking my requests.
- Optimized Linear, Lasso and Random Forest Regression using GridsearchCV to reach the best model.
- Built a client facing API using flask.

# Code and Resources Used

Python Version: 3.7
Packages: pandas,numpy,sklearn,matplotlib,seaborn,selenium,flask,json,pickle,scrapy,intertools,csv
For Web Framework Requirements: pip install -r requirements.txt
Web Scrap URL: https://carsalesbase.com/car-sales-us-home-main/car-sales-by-brand-us/
Flask Productionization: https://github.com/PlayingNumbers/ds_salary_proj/tree/master/FlaskAPI

# Web scraping

Used the webscraper module built by myself to scrape four tables. With each table, we got the following:

- Year
- US Market Sales
- US Market Growth
- US Market Share

# Web scraper

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
        
f = open("ford.csv", "r")
#print(f.read())

header_names = ['Year', 'Sales', 'Growth', 'Market_Share']
ford_table = pd.read_csv("ford.csv", header=None, names = header_names)
print(ford_table)


Saving data.csv

ford_table.to_csv("Ford_us.csv")

# Data Cleaning

After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

- Joined all the four tables into one
- Made a average column for all the players but Tesla.
- Made a average column for all the players

# EDA

I looked at the distributions of the data and the value counts for the various categorical variables.

# Model Building

First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.

I tried three different models:

Multiple Linear Regression – Baseline for the model
Lasso Regression – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
Random Forest – Again, with the sparsity associated with the data, I thought that this would be a good fit.

# Model performance
The Random Forest model far outperformed the other approaches on the test and validation sets.

Random Forest : MAE = 5.71
Linear Regression: MAE = 11.09
Lasso Regression: MAE = 11.07

# Productionization
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a car's growth listing and returns an estimated growth.


