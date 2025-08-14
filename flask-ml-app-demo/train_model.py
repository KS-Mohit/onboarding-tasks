import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Load the classic Iris dataset from a URL
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
columns = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
df = pd.read_csv(url, header=None, names=columns)

# Prepare the data
X = df.iloc[:, 0:4] # Features
y = df.iloc[:, 4]   # Target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

print("Model trained successfully!")

# Save the trained model to a file using pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved to model.pkl")