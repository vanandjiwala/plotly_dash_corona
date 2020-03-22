from pandas import read_html
import pandas as pd

df = pd.read_html('https://www.mohfw.gov.in/')[1]
df.to_csv('./Data/covid19_1.csv')


