import bs4
import urllib2
import sqlite3
import json
import sys

def fetch_with_retries(url, retries=3):
    last_exc = None
    for i in range(retries):
        try:
            return urllib2.urlopen(url).read()
        except Exception as e:
            last_exc = e
            continue
    raise last_exc

def gather_more_data(url):

    full_url = "http://app.audiogon.com/" + url

    html = fetch_with_retries(full_url)

    soup = bs4.BeautifulSoup(html)
    details = soup.find('section', id='listing-details')

    asking = details.find('span', class_='asking-price')

    asking_price = asking.string.split("$")[-1].replace(",", "")

    new = details.find('span', class_='new-retail-price')
    new_price = new.string.split("$")[-1].replace(",", "") if new else -1

    return {'asking_price':asking_price, 'new_price':new_price}

def insert_data(con, data):
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM audiogon WHERE listing_id = %d" % int(data['listing_id']))
        cur.execute("INSERT INTO audiogon VALUES(%d, '%s', '%s', '%s', '%s', %f, %f)" % (int(data['listing_id']), "http://app.audiogon.com" + data['url'], data['display_title'], data['anchor_title'], data['category'], float(data['asking_price']), float(data['new_price'])))
        con.commit()
    except sqlite3.Error, e:
        print "Error: %s" % e
        sys.exit(1)

db = "data/audiogon.sqlite"
con = sqlite3.connect(db)

with con:

    audiogon_new = "http://app.audiogon.com/listings/new-today"

    html = fetch_with_retries(audiogon_new)

    soup = bs4.BeautifulSoup(html)

    # find the listing info, parse the dom

    # 1. select only classified ads, no promos, etc

    classifieds = soup.find_all('table', class_='classifieds')

    # are there more than one of these divs? iterate over any

    for classified_sec in classifieds:
        tbody = classified_sec.tbody

        # get the listings
        rows = tbody.find_all('tr', class_='browsable-listing-row')
        for row in rows:
            # select out the useful stuff!
            listing_id = row['data-id']

            item = row.find('td', class_='item')

            url = item.a['href']
            anchor_title = item.a['title'].replace("'", "")
            display_title = item.a.string.replace("'", "")

            category = row.find('td', class_='category').string

            price = row.find('td', class_='price').string

            data = {
                'listing_id':listing_id,
                'url':url,
                'anchor_title':anchor_title,
                'display_title':display_title,
                'category':category,
                'price':price
            }

            # get page data, save everything to sqlite

            details = gather_more_data(url)

            data.update(details)

            print json.dumps(data)
            insert_data(con, data)
