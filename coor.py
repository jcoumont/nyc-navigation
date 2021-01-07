# import modules and libraries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import folium
from folium import plugins
from folium.plugins import HeatMap
import calendar


# import dataset
df = pd.read_csv('data/data_100000_out_final.csv')

#print the dataset
df.sample(5)
#print shape
df.shape

# adding asked columns : - location, nb accident total, nb accident avec blessé, nb accident avec tué

df['total_injured'] = df['persons_injured'] + df['pedestrians_injured'] + df['cyclist_injured'] + df['motorist_injured']
df['total_killed'] = df['persons_killed'] + df['pedestrians_killed'] + df['cyclist_killed'] + df['motorist_killed']
df['accidents'] = np.repeat(1, df.shape[0])

df.head()

# creating a new dataset with only 4 columns

data = df.groupby(['latitude', 'longitude'], as_index=False)['latitude', 'longitude','total_injured', 'total_killed', 'accidents'].sum()
data.head()

#check for values
data['total_killed'].value_counts()

#save to csv file
data.to_csv('data/final_set.csv')