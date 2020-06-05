import os
import json
import pandas as pd
import glob

temp  = pd.DataFrame()

path = 'jsonFiles'

json_pattern = os.path.join(path, '*.json')
file_list = glob.glob(json_pattern)
print(json_pattern)

for file in file_list:
    data = pd.read_json(file, lines=True)
    temp = temp.append(data, ignore_index = True)

df = temp.loc[:, ['access', 'capec', 'cvss', 'impact', 'summary']]

df.to_excel("sortet_output.xlsx")
