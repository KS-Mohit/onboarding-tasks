import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create the flask app
app = Flask(__name__)

# Load the pickle model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    # Pass an empty image_filename so the image doesn't show on the first load
    return render_template("index.html", image_filename=None)

@app.route("/predict", methods=["POST"])
def predict():
    # Get the feature values from the HTML form
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    
    # Make a prediction using the loaded model
    prediction = model.predict(features)
    prediction_class = prediction[0] 

    # Create a mapping from the prediction class to the image filename
    image_map = {
        "Iris-setosa": "setosa.jpg",
        "Iris-versicolor": "versicolor.jpg",
        "Iris-virginica": "virginica.jpg"
    }
    # Get the correct image filename from the map
    image_filename = image_map.get(prediction_class)

    prediction_text = f"The flower species is {prediction_class}"

    # Pass BOTH the text and the image filename to the template
    return render_template("index.html", prediction_text=prediction_text, image_filename=image_filename)


if __name__ == "__main__":
    app.run(debug=True)