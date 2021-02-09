# importing the libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_log_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from statistics import median
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

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

num_vars = ['curbweight', 'enginesize', 'horsepower', 'carwidth', 'Highend']

Y = cars_lr['price'].values
X = cars_lr[num_vars].values

# train and test split
np.random.seed(0)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7, test_size=0.3, random_state=100)

# Standardization
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)


def try_model(model, parameters, X_train, Y_train, X_test, Y_test):
    mod = GridSearchCV(model, parameters, cv=None)
    mod.fit(X_train, Y_train)
    return mod

parameters = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]}
polyfeats = PolynomialFeatures(degree=2)
X_train_poly = polyfeats.fit_transform(X_train)
X_test_poly = polyfeats.transform(X_test)
mod = try_model(LinearRegression(), parameters, X_train_poly, Y_train, X_test_poly, Y_test)


def valore_nullo(feature, a, min, max):
    if feature == "":
        print("VALORE NON INSERITO --- E' STATO INSERITO VALORE MEDIANA")
        feature = median(a)
    elif float(feature) < min or float(feature) > max:
        print("VALORE NON VALIDO --- E' STATO INSERITO VALORE MEDIANA")
        feature = median(a)
    return feature


# Acquisizione features in input
print("\n-------------  FEATURES PER LA PREDIZIONE DEL PREZZO DELLA MACCHINA --------------")

print("\nInserire il peso della macchina in Kg (MIN:1488 Kg, MAX:4066 Kg)")
curbweight = valore_nullo(input(), cars_lr["curbweight"].values, 1488, 4066)
print("----------------------------------------------------------------------------------")

print("\nInserire la dimensione del motore in cc (MIN:61 cc, MAX:326 cc)")
enginesize = valore_nullo(input(), cars_lr["enginesize"].values, 61, 326)
print("----------------------------------------------------------------------------------")

print("\nInserire la potenza dei cavalli in kW (MIN:48 kW, MAX:288 kW)")
horsepower = valore_nullo(input(), cars_lr["horsepower"].values, 48, 288)
print("----------------------------------------------------------------------------------")

print("\nInserire la larghezza della macchina in pollici (MIN:60 pollici, MAX:72 pollici)")
carwidth = valore_nullo(input(), cars_lr["carwidth"].values, 60, 72)

highend = 0 #valore della mediana

X_user = np.array([curbweight, enginesize, horsepower, carwidth, highend])
X_user = X_user.reshape(1, -1)
X_user = ss.transform(X_user)
X_user = polyfeats.transform(X_user)
predict = mod.predict(X_user)

print("\n")
print("+---------------------------------------------------------------------------+")
print("|                        PREDIZIONE PREZZO AUTO                             |")
print("+---------------------------------------------------------------------------+")
print("| curbweight ---> ", curbweight)
print("+---------------------------------------------------------------------------+")
print("| enginesize ---> ", enginesize)
print("+---------------------------------------------------------------------------+")
print("| horsepower ---> ", horsepower)
print("+---------------------------------------------------------------------------+")
print("| carwidth ---> ", carwidth)
print("+---------------------------------------------------------------------------+")
print("| highend ---> ", highend)
print("+---------------------------------------------------------------------------+")
print("| PRICE ---> ", round(predict[0], 2))
print("+---------------------------------------------------------------------------+")