from tensorflow.keras.models import load_model
from joblib import load

class HousePriceModel:
    def __init__(self):
        self.model = load_model('static/ai/ann_house_price_model.keras')
        self.scaler = load('static/ai/ann_house_price_scaler.joblib')

    def predict(self, array: list):
        array = self.scaler.transform(array)
        prediction = self.model.predict(array)
        return prediction

# model = HousePriceModel()
#
# home = [1500, 4, 2, 1, 2015, 0.25, 2, 4]
#
# response = model.predict([home])
# print(response)
