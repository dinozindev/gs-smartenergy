from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

# Carregando os modelos
model_regression = joblib.load('random_forest_model_regression.pkl')
model_classification = joblib.load('random_forest_model_classification.pkl')

# Inicializando o Flask
app = Flask(__name__)
CORS(app)

continent_mapping = {
    0: "Américas",
    1: "Europa",
    2: "Oceania",
    3: "África",
    4: "Ásia"
}

# Função para converter tipos NumPy para tipos Python nativos
def convert_to_serializable(data):
    if isinstance(data, (np.integer, np.int64)):
        return int(data)
    elif isinstance(data, (np.floating, np.float64)):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    return data

# Rota para o modelo de regressão
@app.route('/predict_regression_carbon', methods=['POST'])
def predict_regression():
    try:
        # Obter os dados JSON enviados pela requisição
        data = request.get_json()

        # Criar DataFrame a partir dos dados recebidos
        input_data = pd.DataFrame(data, index=[0])

        # Fazer a previsão
        prediction = model_regression.predict(input_data)

        # Retornar a previsão como resposta em JSON
        return jsonify({'prediction': convert_to_serializable(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# Rota para o modelo de classificação
@app.route('/predict_classification_continent', methods=['POST'])
def predict_classification():
    try:
        # Obter os dados JSON enviados pela requisição
        data = request.get_json()

        # Criar DataFrame a partir dos dados recebidos
        input_data = pd.DataFrame(data, index=[0])

        # Passar os dados para o modelo sem as colunas
        input_data_values = input_data.values  # Remover nomes das colunas

        # Fazer a previsão
        predicted_class = model_classification.predict(input_data_values)[0]

        # Mapear o valor predito para a categoria correspondente
        predicted_category = continent_mapping.get(predicted_class, "Unknown")

        # Retornar a previsão como resposta em JSON
        return jsonify({'prediction': predicted_category})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)