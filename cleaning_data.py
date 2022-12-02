from email import header
import pandas as pd

house_price = pd.read_csv("./data.csv")
header = house_price[0]
print(header)