from flask import Flask, request, render_template
import pickle
from tensorflow import keras
import tensorflow as tf
import library

app = Flask(__name__, template_folder='public', static_folder='public')
vectorizer = pickle.load(open('./model/vectorizer.pickle', 'rb'))
rf_model = pickle.load(open('./model/rf_clf.pickle', 'rb'))

with tf.device('/cpu:0'):
  model = keras.models.load_model('./model/CNN_Model')

@app.route('/')
def main_page():
  return render_template('index.html')

@app.route('/check-sql', methods=['POST'])
def index():
  command = request.json['SQL_Query']
  print(command)
  command_encoded = vectorizer.transform([command]).toarray()

  y_pred = rf_model.predict(command_encoded)
  y_pred_cnn = model.predict(command_encoded)

  print((y_pred_cnn[0][0]), round(y_pred[0]))
  
  if (y_pred_cnn[0][0] != 1):
    result_decode = "An toàn"
  else:
    result_decode = "Nguy hiểm"

  # data = [command, round(y_pred[0]), round(y_pred_cnn[0][0][0])]
  # library.write_csv_file('history.csv', data)

  return {
    "status_code": 200, 
    "sql_query": command, 
    "result": result_decode
  }

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
  app.run(debug=True)