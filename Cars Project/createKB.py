import numpy as np
import pandas as pd

KNOWLEDGE_BASE_PATH = "./../data/knowledge_base.pl"

cars = pd.read_csv('../data/CarPrice.csv')

# Splitting company name from CarName column
CompanyName = cars['CarName'].apply(lambda x: x.split(' ')[0])
cars.insert(3, "CompanyName", CompanyName)
cars.CompanyName = cars.CompanyName.str.lower()
cars['CarName'] = cars['CarName'].apply(lambda x: ' '.join(x.split(' ')[1:]))

file_data = ":- discontiguous companyModel/2.\n\n"
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

cars['price'] = cars['price'].astype('int')
temp = cars.copy()
table = temp.groupby(['companyName'])['price'].mean()
temp = temp.merge(table.reset_index(), how='left', on='companyName')
bins = [0, 10000, 20000, 40000]
cars_bin = ['budget', 'medium', 'highend']
cars['carsrange'] = pd.cut(temp['price_y'], bins, right=False, labels=cars_bin)


def is_not_blank(s):
    if s and s.strip():
        return True
    return False


# Generating company
for string in np.unique(cars['companyName']):
    if is_not_blank(string):
        file_data += "company(\"" + string + "\").\n"

file_data += "\n"

# Generating fuelType
for string in np.unique(cars['fueltype']):
    if is_not_blank(string):
        file_data += "fuelType(\"" + string + "\").\n"

file_data += "\n"

# Generating model - fuelType
for row in cars.itertuples():
    model = row[3]
    fuel = row[5]
    string = "fuelCar(\"" + model + "\",\"" + fuel + "\")."

    if is_not_blank(model) and is_not_blank(fuel) and (string not in file_data):
        file_data += string + "\n"

file_data += "\n"

# Generating company - model
for row in cars.itertuples():
    company = row[4]
    model = row[3]
    string = "companyModel(\"" + company + "\",\"" + model + "\")."

    if is_not_blank(company) and is_not_blank(model) and (string not in file_data):
        file_data += string + "\n"

file_data += "\n"

# Generating model - carbody
for row in cars.itertuples():
    model = row[3]
    carbody = row[8]
    string = "modelBody(\"" + model + "\",\"" + carbody + "\")."

    if is_not_blank(model) and is_not_blank(carbody) and (string not in file_data):
        file_data += string + "\n"

file_data += "\n"

# Generating model - carsrange
for row in cars.itertuples():
    company = row[4]
    carsrange = row[28]
    string = "carsrange(\"" + company + "\",\"" + str(carsrange) + "\")."

    if is_not_blank(company) and (string not in file_data):
        file_data += string + "\n"

knowledge_base = open(KNOWLEDGE_BASE_PATH, mode="w")
knowledge_base.write(file_data)
knowledge_base.close()

print("\nFile created in: ", KNOWLEDGE_BASE_PATH)
