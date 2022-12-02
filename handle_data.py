from sklearn.feature_selection import mutual_info_regression
from scipy import stats
from category_encoders import MEstimateEncoder

import pandas as pd
import numpy as np

from  versioning_data import read_mongo

# ================== Feature engineer ====================
def miScore(x, y):
    """
    Compute Mi-Score of all collums
    """
    x = x.copy()
    for colname in x.select_dtypes(['object','category']):
        x[colname], _ = x[colname].factorize() # similar one hot encoding ['b', 'b', 'a', 'c', 'b'] => [0, 0, 1, 2, 0]
    
    discrete_features = [pd.api.types.is_integer_dtype(t) for t in x.dtypes]
    mi_score = mutual_info_regression(x,y,
                                      discrete_features=discrete_features,
                                      random_state=32)
    mi_score = pd.Series(mi_score,name='Mutual Information Score',index=x.columns)
    mi_score = mi_score.sort_values(ascending=False)
    
    return mi_score

# ================== Remove outliers ====================
def zScore(dataset, columns):
    """
    Compute z-score 
    """

    return np.abs(stats.zscore(dataset[columns]))

def handleData(dataset):
    """
    Filter Feature needed for training and remove outlirer with Z-Score
    """
    x = dataset.copy()
    y = x.pop('price')

    mi_score = miScore(x,y)

    feature = [col for col in mi_score.index if mi_score[col] > 0.01]

    dataset = dataset[feature]
    dataset=dataset.join(y)

    z_score = zScore(dataset, columns= ['sqft_living','sqft_above','bathrooms','yr_built','sqft_lot','bedrooms'])
    new_dataset = dataset[(z_score<3).all(axis=1)]

    return new_dataset

def encodeData(dataset, columns = ['street','statezip','city', 'yr_built', 'yr_renovated']):
    x = dataset.copy()
    y = x.pop('price')
    encoder = MEstimateEncoder(cols=columns,m=0.5)
    encoder.fit(x,y)

    return encoder
    

def nomalizeData(dataset, encoder, inference = False):
    x = dataset.copy()
    if inference == False:
        y = x.pop('price') 
    
    x_transformed = encoder.transform(x)
    means, maxs, mins = dict(), dict(), dict()
    for col in x_transformed:
        means[col] = x_transformed[col].mean()
        maxs[col] = x_transformed[col].max()
        mins[col] = x_transformed[col].min()
    
    x_transformed = (x_transformed - x_transformed.mean()) / (x_transformed.max() - x_transformed.min())
    if inference:
        return x_transformed.mean(), x_transformed.max(), x_transformed.min()

    return x_transformed, y

if __name__ == "__main__":
    from dotenv import dotenv_values
    config = dotenv_values(".env")

    host = config['ATLAS_URI']
    df = read_mongo('house_price', 'raw_data', {}, host= host)

    new_data = handleData(df)
    encoder = encodeData(new_data)
    x_transformed, y = nomalizeData(new_data, encoder)

    print(x_transformed['street'])