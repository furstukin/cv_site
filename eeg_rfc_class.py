from joblib import load


class EegEyeModel:
    def __init__(self):
        self.model = load('static/ai/eeg_eye_model.joblib')
        self.scaler = load('static/ai/eeg_eye_scaler.joblib')

    def predict(self, array: list):
        array = self.scaler.transform(array)
        prediction = self.model.predict(array)
        return prediction

# model = EegEyeModel()
#
# closed = [4.4, 4.45, 4.26, 4.29, 4.03, 4.65, 4.14, 4.22, 4.07, 4.58, 4.61, 4.17, 4.35, 4.23]
# closed2 = [val*1000 for val in closed]
# print(closed2)
#
# response = model.predict([closed2])
# print(response)

