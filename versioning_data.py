# Versioning data.
from dotenv import dotenv_values
import pandas as pd
from pymongo import MongoClient

config = dotenv_values(".env")

print('------Versioning data--------')

def read_mongo(db, collection, query={}, host='localhost', no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    client = MongoClient(host)
    db = client[db]

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    return df


print('------End Versioning--------')
if __name__ == '__main__':
    host = config['ATLAS_URI']
    df = read_mongo('house_price', 'raw_data', {}, host= host)
    print(df.head(1))









