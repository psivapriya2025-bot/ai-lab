from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# dummy data
# Features (e.g., height, weight, age)
X = [
    [180, 80, 40],
    [165, 55, 23],
    [170, 75, 34],
    [160, 50, 20],
    [177, 65, 28],
    [158, 45, 18]
]
# Labels (e.g., 0 for class A, 1 for class B)
y = [0, 1, 0, 1, 0, 1]
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
# Create a Gaussian Naive Bayes model
model = GaussianNB()
# Train the model
model.fit(X_train, y_train)
# Make predictions
y_pred = model.predict(X_test)
# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Predictions: {y_pred}")
print(f"Accuracy: {accuracy}")

