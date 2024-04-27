X_test = test[:, :3]  # Features: sleep, smoke, obese
y_test = test[:, 3]   # Target variable: rate

# Make predictions using the trained model
y_pred = model.predict(X_test)

# Print the first few predictions and actual values
for i in range(5):
    print(f"Predicted: {y_pred[i]:.2f}, Actual: {y_test[i]:.2f}")

# Evaluate the model on the test data
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nMean Squared Error:", mse)
print("R-squared:", r2)
