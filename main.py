from flask import Flask, request, render_template
import pickle
from tensorflow import keras
import tensorflow as tf
import library

app = Flask(__name__, template_folder='public', static_folder='public')

vectorizer = pickle.load(open('./model/vectorizer.pickle', 'rb'))
rf_model = pickle.load(open('./model/rf_clf.pickle', 'rb'))
vt_model = pickle.load(open('./model/vt_clf.pickle', 'rb')) # include svm, xgb
cnn_model = keras.models.load_model('./model/CNN_Model')

@app.route('/')
def main_page():
  return render_template('index.html')

@app.route('/check-sql', methods=['POST'])
def index():
  command = request.json['SQL_Query']
  print(command)
  command_encoded = vectorizer.transform([command]).toarray()

  y_pred_rf = rf_model.predict(command_encoded)
  y_pred_vt = vt_model.predict(command_encoded)
  y_pred_cnn = cnn_model.predict(command_encoded).flatten()
  y_pred_cnn = tf.math.round(y_pred_cnn[0])

  result = y_pred_rf[0]*0.25 + y_pred_vt[0]*0.35 + y_pred_cnn[0]*0.4
  result = tf.math.round(result)

  if (result != 1):
    result_decode = "An toàn"
  else:
    result_decode = "Nguy hiểm"

  # data = [command, round(y_pred[0]), round(y_pred_cnn[0][0][0])]
  # library.write_csv_file('history.csv', data)

  return {
    "status_code": 200, 
    "sql_query": command, 
    "result": result_decode,
    "full_result": [y_pred_rf[0], y_pred_vt[0], y_pred_cnn[0]]
  }

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
  app.run(debug=True)