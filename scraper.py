import requests
from urllib.parse import urlencode, quote
from search import Query
import mysql.connector
import time

def collect(q):
    """
    Scrapes the Grailed Algolia Search API for results from a 
    given query (a Query object).

    Parameter q: the Query from which results are scraped.
    Precondition: q must be a Query object
    """

    payload = {
        "requests": [{
            "indexName":"Listing_production",
            "params":("highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=2000&filters=&clickAnalytics=true&analytics=true&enableABTest=true&getRankingInfo=true&userToken=5113624&enablePersonalization=false&personalizationImpact=0&maxValuesPerFacet=100&query=" + q.getKeywordsURL() + "&page=0&facets=%5B%22department%22%2C%22category_path%22%2C%22category_size%22%2C%22designers.name%22%2C%22price_i%22%2C%22condition%22%2C%22location%22%2C%22badges%22%2C%22strata%22%5D&tagFilters=&facetFilters=" + q.getFiltersURL() + "&numericFilters=" + q.getRangeURL())
        }]
    }

    params = {
        "x-algolia-agent": "Algolia for JavaScript (4.14.2); Browser; JS Helper (3.8.2); react (17.0.2); react-instantsearch (6.24.3)",
        "x-algolia-api-key": "bc9ee1c014521ccf312525a4ef324a16",
        "x-algolia-application-id": "MNRWEFSS2Q"
    }

    search_url = "https://mnrwefss2q-dsn.algolia.net/1/indexes/*/queries?" + urlencode(params)

    response = requests.post(search_url, params=params, json=payload)
    new = response.json()['results'][0]['hits']
    results = []
    for each in new:
        if len(each['description']) > 200:
            description = each['description'][:194] + '. . .'
        else:
            description = each['description']
        results.append((each['title'], each['price'] + each['shipping']['us']['amount'], each['price_updated_at_i'], description, each['color'], each['id']))
    return results


def deposit(q,db):
    """
    Inputs the results of a search into a MySQL Database
    table.

    If the query does not have an existing table, a new
    table is created.

    If the query has an existing table, the table is updated.

    Parameter q: the query from which results are scraped.
    Precondition: q must be a Query object

    Parameter db: the database in which the results of a query is deposited
    Precondition: db must be a MySQLConnection object
    """
    results = collect(q)
    search = q.getKeywordsDB()
    mycursor = db.cursor()
    mycursor.execute('SET @@SESSION.sql_mode = "ONLY_FULL_GROUP_BY,NO_ENGINE_SUBSTITUTION"')

    mycursor.execute(f"SELECT count(*)\
        FROM information_schema.TABLES\
        WHERE (TABLE_SCHEMA = '{db.database}') AND (TABLE_NAME = '{search}')"
        )
    
    exists = mycursor.fetchone()[0]

    if exists == 0:
        mycursor.execute(f"CREATE TABLE {search} (title VARCHAR(120), price smallint UNSIGNED, time bigint UNSIGNED, description VARCHAR(200), color VARCHAR(50), listing_id int UNSIGNED)")
        db.commit()
        mycursor.executemany(f"INSERT INTO {search} (title, price, time, description, color, listing_id) VALUES (%s,%s,%s,%s,%s,%s)", results)
        db.commit()
    else:
        mycursor.execute(f"TRUNCATE {search}")
        db.commit()
        mycursor.executemany(f"INSERT INTO {search} (title, price, time, description, color, listing_id) VALUES (%s,%s,%s,%s,%s,%s)", results)
        db.commit()


def getRecents(q,db,t):
    """
    Obtains the results of a query within a certain time
    interval (starting from present time).

    Parameter q: the query from which results are scraped.
    Precondition: q must be a Query object

    Parameter db: the database in which the results of a query is deposited
    Precondition: db must be a MySQLConnection object

    Parameter t: the time interval (in minutes) that the query is limited to
    Precondition: t is an int; 0 < t <= 59
    """
    deposit(q,db)

    search = q.getKeywordsDB()

    mycursor = db.cursor()
    mycursor.execute(f"SELECT *\
        FROM {search}\
        WHERE time >= " +str(time.time()-(t*60))
        )

    return mycursor