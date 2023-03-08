from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import max_error
import numpy as np
import csv
actual = open('esp3.csv')
type(actual)
csvreader = csv.reader(actual)
rows = []
for row in csvreader:
        rows.append(row)
y_actual=[]
for x in range(len(rows)):
    print(rows[x][1])
    y_actual.append(rows[x][1])

predict=open('outesp3ma.csv')
type(predict)
iya = csv.reader(predict)
rows = []
for row in iya:
        rows.append(row)

y_predic=[]
for y in range(len(rows)):
    y_predic.append(rows[y][1])
y1=([float(x) for x in y_actual])
y2=([float(x) for x in y_predic])
print("ini y1")
print(y1)
print("ini y2")
print(y2)

rms = mean_squared_error(y1, y2,squared=False)
print("mse = "+str(rms))
mape=mean_absolute_percentage_error(y1, y2)
print("mape = "+str(mape))
mae=mean_absolute_error(y1, y2)
print("mae = " +str(mae))
r2=r2_score(y1,y2)
print("r2 = "+str(r2))
# msle=mean_squared_log_error(y1,y2)
# print("msle = "+str(msle))
# maxerr=accuracy_score(y1, y2)
# print("max err = "+str(maxerr))
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import cross_val_score
# scores = cross_val_score(LinearRegression(), y1, y2, cv=669, scoring='r2')
# print(scores)

