import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MaxAbsScaler

cars = pd.read_csv('../data/CarPrice.csv')

# Splitting company name from CarName column
CompanyName = cars['CarName'].apply(lambda x: x.split(' ')[0])
cars.insert(3, "CompanyName", CompanyName)
cars.drop(['CarName'], axis=1, inplace=True)

cars.CompanyName = cars.CompanyName.str.lower()


def replace_name(a, b):
    cars.CompanyName.replace(a, b, inplace=True)


replace_name('maxda', 'mazda')
replace_name('porcshce', 'porsche')
replace_name('toyouta', 'toyota')
replace_name('vokswagen', 'volkswagen')
replace_name('vw', 'volkswagen')

# Fuel economy
cars['fueleconomy'] = (0.55 * cars['citympg']) + (0.45 * cars['highwaympg'])

# Binning the Car Companies based on avg prices of each Company.
cars['price'] = cars['price'].astype('int')
temp = cars.copy()
table = temp.groupby(['CompanyName'])['price'].mean()
temp = temp.merge(table.reset_index(), how='left', on='CompanyName')
bins = [0, 10000, 20000, 40000]
cars_bin = ['Budget', 'Medium', 'Highend']
cars['carsrange'] = pd.cut(temp['price_y'], bins, right=False, labels=cars_bin)

cars_lr = cars[['price', 'fueltype', 'aspiration', 'carbody', 'drivewheel', 'wheelbase',
                'curbweight', 'enginetype', 'cylindernumber', 'enginesize', 'boreratio', 'horsepower',
                'fueleconomy', 'carlength', 'carwidth', 'carsrange']]


# Defining the map function
def dummies(x, df):
    temp = pd.get_dummies(df[x], drop_first=True)
    df = pd.concat([df, temp], axis=1)
    df.drop([x], axis=1, inplace=True)
    return df


# Applying the function to the cars_lr
cars_lr = dummies('fueltype', cars_lr)
cars_lr = dummies('aspiration', cars_lr)
cars_lr = dummies('carbody', cars_lr)
cars_lr = dummies('drivewheel', cars_lr)
cars_lr = dummies('enginetype', cars_lr)
cars_lr = dummies('cylindernumber', cars_lr)
cars_lr = dummies('carsrange', cars_lr)

num_vars = ['enginesize', 'horsepower', 'carwidth']

Y = cars_lr['price'].values
#X = cars_lr[num_vars].values
X1 = cars_lr['enginesize'].values
X2 = cars_lr['horsepower'].values
X3 = cars_lr['carwidth'].values

# Standardization
X1 = X1/np.linalg.norm(X1)
X2 = X2/np.linalg.norm(X2)
X3 = X3/np.linalg.norm(X3)
cars_lr['quality'] = 0.4*X1 + 0.3*X2 + 0.3*X3

print(cars_lr["quality"])

Y_test = Y
Y_pred_test = cars_lr["quality"].values

fig = plt.figure()
plt.scatter(Y_test, Y_pred_test)
fig.suptitle('y_test vs y_pred', fontsize=20)  # Plot heading
plt.xlabel('y_test', fontsize=18)  # X-label
plt.ylabel('y_pred', fontsize=16)
plt.show()


km = KMeans(n_clusters=2, random_state=0)
cars_lr.info()
km.fit(cars_lr['price'].values)
centers = km.cluster_centers_
print(centers)
