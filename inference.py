import pickle
import pandas as pd

from dotenv import dotenv_values

from  versioning_data import read_mongo
from handle_data import encodeData, handleData, nomalizeData
config = dotenv_values(".env")

host = config['ATLAS_URI']
df = read_mongo('house_price', 'raw_data', {}, host= host)
new_data = handleData(df)
encoder = encodeData(new_data)

filename = './model/model.sav'
model = pickle.load(open(filename, 'rb'))

columns = ['street', 'statezip', 'city', 'sqft_living', 'sqft_above', 'bathrooms',
            'sqft_lot', 'floors', 'yr_built', 'bedrooms', 'view', 'sqft_basement', 'yr_renovated']


street = sorted(new_data['street'].unique())
statezip = sorted(new_data['statezip'].unique())
city = sorted(new_data['city'].unique())
yr_renovated = sorted(new_data['yr_renovated'].unique())
yr_built = sorted(new_data['yr_built'].unique())


def predict(*args):
    df = pd.DataFrame([args], columns= columns)

    x_transformed = encoder.transform(df)
    
    normalizer = nomalizeData(x_transformed, encoder, inference = True)
    x_transformed = normalizer.transform(x_transformed)

    try:
        pred = model.predict(x_transformed.reshape(1, -1))
    except:
        print("Error")

    return abs(round(float(pred[0]), 2))