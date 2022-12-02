import pandas as pd
from pymongo import MongoClient
from dotenv import dotenv_values
config = dotenv_values(".env")

def mongoimport(csv_path,db_name, db_url='localhost'):
    """ 
    Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = MongoClient(db_url)
    data = pd.read_csv(csv_path)
    data = data.to_dict(orient= "records")
    db = client[db_name]
    db['raw_data'].insert_many(data)
    print(f"Import data to MongoDb successfull {db}")
    
print('------Import Data to MongoDB--------')


data_path = './data.csv'
db_name = "house_price"

db_url = config['ATLAS_URI']

mongoimport(data_path, db_name, db_url = db_url)


print('------End Import Data --------')