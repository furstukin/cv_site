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
# home = [4272, 3, 3, 2016, 4.7530138494020395, 1, 6]
#
# response = model.predict([home])
# print(response)