import pandas as pd
import numpy as np

KNOWLEDGE_BASE_PATH = "./../data/knowledge_base.pl"

cars = pd.read_csv('../data/CarPrice.csv')

# Splitting company name from CarName column
CompanyName = cars['CarName'].apply(lambda x: x.split(' ')[0])
cars.insert(3, "CompanyName", CompanyName)
cars.CompanyName = cars.CompanyName.str.lower()
cars['CarName'] = cars['CarName'].apply(lambda x: ' '.join(x.split(' ')[1:]))

print(cars.info())

file_data = ""
cars.rename({'CompanyName': 'companyName'}, axis=1, inplace=True)
cars.rename({'CarName': 'carName'}, axis=1, inplace=True)


def replace_name(a, b):
    cars.companyName.replace(a, b, inplace=True)


replace_name('maxda', 'mazda')
replace_name('porcshce', 'porsche')
replace_name('toyouta', 'toyota')
replace_name('vokswagen', 'volkswagen')
replace_name('vw', 'volkswagen')
replace_name('Nissan', 'nissan')

# Generating company
for string in np.unique(cars['companyName']):
    file_data += "company(" + string + ")\n"

file_data += "\n"

# Generating fuelType
for string in np.unique(cars['fueltype']):
    file_data += "fuelType(" + string + ")\n"

file_data += "\n"

# Generating model - fuelType
for row in cars.itertuples():
    file_data += "fuelCar(" + row[3] + "," + row[5] + ")\n"

file_data += "\n"

# Generating company - model
for row in cars.itertuples():
    file_data += "companyModel(" + row[4] + "," + row[3] + ")\n"

file_data += "\n"

# Generating model - carbody
for row in cars.itertuples():
    file_data += "modelBody(" + row[3] + "," + row[8] + ")\n"

knowledge_base = open(KNOWLEDGE_BASE_PATH, mode="w")
knowledge_base.write(file_data)
knowledge_base.close()

print("File created in: ", KNOWLEDGE_BASE_PATH)
