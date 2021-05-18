from textAnalysis import CreateOccurrenceData

import textAnalysis.utilities as util
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from typing import List


def write_occurrence_data_to_file():
    temp = CreateOccurrenceData.CreateOccurrenceData()
    terms = temp.get_terms()
    # print("Terms: ", terms)

    dates = pd.date_range('1/1/2015', '1/1/2020')

    data: pd.DataFrame = temp.populate_frame(dates, terms)
    paths_dict = util.getPaths()
    fs_directory = paths_dict['fs_project_data_misc']
    data.to_json(fs_directory + '/occurrence_data.json')


def read_occurrence_data_from_file() -> pd.DataFrame:
    paths_dict = util.getPaths()
    fs_directory = paths_dict['fs_project_data_misc']
    return pd.read_json(fs_directory + '/occurrence_data.json')


# data.plot(y='test', style='.')
# plt.show()

# Which rows have a value greater than 0 in the test column
# data.loc[data['test'] > 0]

# data.rolling(5, win_type='boxcar').sum()

# window = data['test'].rolling(1000, win_type='boxcar')

# window.sum().plot()
# plt.show()

# data['test'].cumsum().plot()
# plt.show()


# write_occurrence_data_to_file()
data_frame: pd.DataFrame = read_occurrence_data_from_file()
sum_of_occurrences: pd.Series = data_frame.sum()

# plt.figure()
sum_of_occurrences.hist(alpha=0.5)
plt.show()

# Selecting all rows and the column with index 100
data_frame.iloc[:, 100]
