import pandas as pd

cars = pd.read_csv("../data/pippo2.csv", index_col=0)
# sns.heatmap(auto.corr())
# plt.show()

#cars.drop(columns=["torque"], inplace=True)

#cars = pd.get_dummies(cars, columns=["fuel"])
#cars = pd.get_dummies(cars, columns=["transmission"])
#cars = pd.get_dummies(cars, columns=["owner"])
#cars = pd.get_dummies(cars, columns=["seller_type"])

myList = list()
for power in cars["max_power (bhp)"]:
    if "nan" not in str(power):
        string = str(power)[:-1]
        if "." not in str(power):
            myList.append(float(string + ".0"))
        else:
            myList.append(float(string))
    else:
        myList.append(power)

cars.drop(columns=["max_power (bhp)"], inplace=True)
cars["max_power (bhp)"] = myList
cars.info()
print(cars["max_power (bhp)"])
#cars.to_csv(path_or_buf="C:\\Users\\WinEnzo\\Desktop\\Corona\\data\\pippo2.csv")
