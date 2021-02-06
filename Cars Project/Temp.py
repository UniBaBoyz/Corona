import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

TEST_SIZE = 0.2

cars = pd.read_csv("../data/CarPrice_Assignment.csv")

Y = cars["selling_price"].values
X = cars.drop(labels="selling_price", axis=1)
X.info()
#X = pd.get_dummies()
X_copy = X

X = StandardScaler().fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=TEST_SIZE)

model = LinearRegression()
model.fit(X_train, Y_train)

Y_pred_test = model.predict(X_test)
Y_pred_train_test = model.predict(X_train)

print("\nMean squared error pred: ", mean_squared_error(Y_test, Y_pred_test))
print("\nRegression score pred: ", r2_score(Y_test, Y_pred_test))

print("\nMean squared error true: ", mean_squared_error(Y_train, Y_pred_train_test))
print("\nRegression score true: ", r2_score(Y_train, Y_pred_train_test))

#X = PolynomialFeatures(degree=2).fit_transform(X)


#model = Ridge()
#model = Lasso()
#model = BayesianRidge()

