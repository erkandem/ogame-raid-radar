"""
Processing script to convert
text tables to json / dict
"""

with open('research_properties', 'r') as f:
    txt = f.read()
txt0 = txt[1:-1]
txt0 = txt0.replace(',', '')
txt0 = txt0.replace('/', 'NaN')
txt1 = txt0.split('\n')
txt2 = [elm.split('\t') for elm in txt1]
txt3 = [[cell.strip() for cell in row] for row in txt2]


# %% mapping prep
header = txt3[0][1:]
row_names = [elm[0] for elm in txt3[1:]]
raw_data = [elm[1:] for elm in txt3[1:]]

#%% Formatting
header = [elm.replace(' ', '') for elm in header]
row_names = [elm.replace(' ', '') for elm in row_names]

# %% mapping
data = {
    ship_name: {prop_name: float(prop_value) for prop_name, prop_value in zip(header, row)}
    for ship_name, row in zip(row_names, raw_data)
}

#%%
data = {
    ship_name: {prop_name: prop_value for prop_name, prop_value in zip(header, row)}
    for ship_name, row in zip(row_names, raw_data)
}

#%%
property_names = ['Metal', 'Crystal', 'Deuterium', 'Energy']
filtered_data = {
  row: {name: float(data[row][name]) for name in property_names}
for row in data}

#%%
import json
print(json.dumps(filtered_data, indent=2))
