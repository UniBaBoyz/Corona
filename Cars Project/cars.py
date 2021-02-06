# importing the libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge
from sklearn.metrics import mean_squared_log_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
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
    Y_pred_test = mod.predict(X_test)
    Y_pred_train_test = mod.predict(X_train)

    print("\nMean squared log error test: ", mean_squared_log_error(Y_test, Y_pred_test))
    print("\nRegression score pred test: ", r2_score(Y_test, Y_pred_test))

    print("\nMean squared log error train: ", mean_squared_log_error(Y_train, Y_pred_train_test))
    print("\nRegression score pred train: ", r2_score(Y_train, Y_pred_train_test))

    # EVALUATION OF THE MODEL
    # Plotting y_test and y_pred to understand the spread.
    fig = plt.figure()
    plt.scatter(Y_test, Y_pred_test)
    fig.suptitle('y_test vs y_pred', fontsize=20)  # Plot heading
    plt.xlabel('y_test', fontsize=18)  # X-label
    plt.ylabel('y_pred', fontsize=16)
    plt.show()


parameters = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]}
print("\nRegressione Lineare")
try_model(LinearRegression(), parameters, X_train, Y_train, X_test, Y_test)

parameters = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False],
              'precompute': [True, False], 'max_iter': [i for i in range(1000, 10000, 500)],
              'warm_start': [True, False],
              'positive': [True, False], 'selection': ['cyclic', 'random']}
print("\n\nModello Lasso")
try_model(Lasso(), parameters, X_train, Y_train, X_test, Y_test)

parameters = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False],
              'max_iter': [i for i in range(1000, 10000, 500)],
              'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']}
print("\n\nModello Ridge")
try_model(Ridge(), parameters, X_train, Y_train, X_test, Y_test)

parameters = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False],
              'n_iter': [i for i in range(300, 2000, 100)], 'compute_score': [True, False]}
print("\n\nModello Bayesiano")
try_model(BayesianRidge(), parameters, X_train, Y_train, X_test, Y_test)

parameters = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]}
print("\n\nRegressione Polinomiale di grado ", 2)
polyfeats = PolynomialFeatures(degree=2)
X_train_poly = polyfeats.fit_transform(X_train)
X_test_poly = polyfeats.transform(X_test)
try_model(LinearRegression(), parameters, X_train_poly, Y_train, X_test_poly, Y_test)
