from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

from handle_data import nomalizeData, handleData
from  versioning_data import read_mongo
import pickle

from dotenv import dotenv_values
config = dotenv_values(".env")

host = config['ATLAS_URI']
df = read_mongo('house_price', 'raw_data', {}, host= host)
print("---------- Handle data ---------")   
new_data = handleData(df)
x_transformed, y = nomalizeData(new_data)

x_train,x_test,y_train,y_test = train_test_split(x_transformed.values,
                                                 y.values,
                                                 test_size=0.2,
                                                 random_state=32)

# ==== Training =========    
print("---------- Traning model ---------")                            
model = LinearRegression()
model.fit(x_train,y_train)

# ==== Test =========
print("---------- Testing model ---------")   
y_pred = model.predict(x_test)

print(f"MAE: {mean_absolute_error(y_test,y_pred)}")
print(f"MSE: {mean_squared_error(y_test,y_pred)}")
print(f"Srore: {r2_score(y_test,y_pred)}")

print("---------- Save model ---------")   

filename = './model/model.sav'
pickle.dump(model, open(filename, 'wb'))