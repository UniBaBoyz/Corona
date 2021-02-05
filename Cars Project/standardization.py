import pandas as pd
import numpy as np
import sklearn.linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt

SIZE = 0.2

cars = pd.read_csv("../data/Cars.csv")
cars.dropna(inplace=True)

cols = ["selling_price", "transmission_Automatic", "transmission_Manual", "max_power (bhp)"]
sns.heatmap(cars[cols].corr(), annot=True, annot_kws={'size': 12})
sns.pairplot(cars[cols])
plt.show()

Y = cars['selling_price'].values
X = cars[cols].drop(['selling_price'], axis=1).values
ss = StandardScaler()
X = ss.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=SIZE)

model = LinearRegression()
model.fit(X_train, Y_train)
car_price_test = model.predict(X_test)

print(mean_squared_error(Y_test, car_price_test))
print(r2_score(Y_test, car_price_test))

# plt.scatter(X_train, Y_train, c="green", edgecolors="white", label="TrainSet")

# plt.scatter(X_test, Y_test, c="blue", edgecolors="white", label="TestSet")

# plt.xlabel("Car info")

# plt.ylabel("Price")

# plt.legend(loc="upper left")

# plt.plot(X_test, car_price_test, color="red", linewidth="3")

# plt.show()
