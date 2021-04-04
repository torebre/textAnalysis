from textAnalysis import CreateOccurrenceData

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from typing import List

temp = CreateOccurrenceData.CreateOccurrenceData()
terms = temp.get_terms()
print("Terms: ", terms)

dates = pd.date_range('1/1/2015', '1/1/2020')

# data_frame = pd.DataFrame(index=dates, columns=terms)

# print("Data frame: ", data_frame)

data = temp.populate_frame(dates, terms)

data.plot(y='test', style='.')
plt.show()

# Which rows have a value greater than 0 in the test column
data.loc[data['test'] > 0]

data.rolling(5, win_type='boxcar').sum()

window = data['test'].rolling(1000, win_type='boxcar')

window.sum().plot()
plt.show()

data['test'].cumsum().plot()
plt.show()