#importing libraries needed
import json
import requests
from argparse import Namespace
import sqlite3

#Update or initialize database
def updateDatabase(itemnums):
    conn=sqlite3.connect('items.db')
    c=conn.cursor()
    #check if 'prices' table already exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='prices' ''')
    if c.fetchone()[0]==1:
        conn.commit()
    else:
        c.execute("CREATE TABLE prices(DateTime VARCHAR)")
        conn.commit()
    #continue to check table for missing item IDs
    items_in_db=c.execute('''PRAGMA table_info('prices')''')
    missing_items=list(set(itemnums)-set(items_in_db))
    for i in missing_items:
        c.execute("ALTER TABLE prices ADD COLUMN '%s' VARCHAR" % i)
        conn.commit()

def json2obj(data): return json.loads(data,object_hook=lambda d: Namespace(**d))

#base API URL
URL='https://api.guildwars2.com/v2/'

#API key from GW2
api_key = "58660480-AF04-DE41-BBDB-BB8032A62D542EF41A1B-5AB1-4E50-91CA-C47567C4EE95"

# defining a params dict for the parameters to be sent to the API
POST_PARAMS = {"Content-Type": "application/json; charset=utf-8","cache-control": "no-cache","Authorization": "Bearer " + api_key,"X-Schema-Version": "2020-01-01T00:00:00Z"}

#Search for item ID based on input keyword


# api-endpoint using item ID
item_id=1868
itemURL = f'{URL}/items/{item_id}'

#get all Item ID's and make name dict
idsURL = f'{URL}/commerce/listings'
r=requests.get(url = idsURL , params = POST_PARAMS)
valid_IDs=r.json()
item_dict={}
for k in valid_IDs:
    item_id=k
    r = requests.get(url = itemURL, params = POST_PARAMS)
    item_dict[k]=json2obj(r.text).name
jsfile=json.dumps(item_dict)
f=open("items.json","w")
f.write(jsfile)
f.close()

# sending get request and saving the response as response object
r = requests.get(url = itemURL, params = POST_PARAMS)

# extracting data in json format, parsing into an object
j=json.loads(r.text,object_hook=lambda d: Namespace(**d))
print(j.name)
