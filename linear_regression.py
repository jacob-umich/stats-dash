import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

X = test[:, :-1]
y = test[:, -1]

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)

mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print("Coefficients:", model.coef_)
print("\nIntercept:", model.intercept_)
print("\nMean Squared Error:", mse)
print("R-squared:", r2)
