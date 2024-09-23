from flask import Flask, request, render_template
import numpy as np
import pickle

# Importing the model and scalers
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))

# Creating the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Retrieving form inputs
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        # Preparing the feature list for prediction
        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        # Applying transformations
        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)

        # Making the prediction
        prediction = model.predict(final_features)

        # Crop dictionary to map prediction to crop names
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya",
            7: "Orange", 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes",
            12: "Mango", 13: "Banana", 14: "Pomegranate", 15: "Lentil", 16: "Blackgram",
            17: "Mungbean", 18: "Mothbeans", 19: "Pigeonpeas", 20: "Kidneybeans",
            21: "Chickpea", 22: "Coffee"
        }

        # Retrieving the crop name based on prediction
        crop = crop_dict.get(prediction[0], "Unknown")
        result = f"{crop} is the best crop to be cultivated right there."

    except Exception as e:
        result = "An error occurred during prediction. Please check the input values."

    # Rendering the result on the same page
    return render_template('index.html', result=result)

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
