from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Global DataFrames
df_bom = pd.DataFrame()
df_workcentre = pd.DataFrame()

@app.route('/convert_to_dataframe_bom', methods=['POST', 'OPTIONS'])
def convert_to_dataframe_bom():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = None
        if request.headers.get('Access-Control-Request-Headers'):
            headers = request.headers['Access-Control-Request-Headers']
        h = response.headers

        # Allow the requested method(s)
        h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'

        # Allow the requested headers
        h['Access-Control-Allow-Headers'] = headers

        return response

    global df_bom
    csv_data = request.get_json()
    df_bom = convert_to_dataframe(csv_data)
    print(df_bom)
    df_bom.to_csv('df_bom.csv', index=False)  # Saving to a CSV file as an example
    return jsonify({'message': 'df_bom created successfully', 'dataframe': df_bom.to_dict(orient='records')}), 200

@app.route('/convert_to_dataframe_workcentre', methods=['POST', 'OPTIONS'])
def convert_to_dataframe_workcentre():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = None
        if request.headers.get('Access-Control-Request-Headers'):
            headers = request.headers['Access-Control-Request-Headers']
        h = response.headers

        # Allow the requested method(s)
        h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'

        # Allow the requested headers
        h['Access-Control-Allow-Headers'] = headers

        return response

    global df_workcentre
    csv_data = request.get_json()
    df_workcentre = convert_to_dataframe(csv_data)
    print(df_workcentre)
    df_workcentre.to_csv('df_workcentre.csv', index=False)  # Saving to a CSV file as an example
    return jsonify({'message': 'df_workcentre created successfully', 'dataframe': df_workcentre.to_dict(orient='records')}), 200

@app.route('/get_dataframe_bom', methods=['GET'])
def get_dataframe_bom():
    global df_bom
    if df_bom.empty:
        return jsonify({'message': 'No df_bom available'}), 404
    return jsonify({'dataframe': df_bom.to_dict(orient='records')}), 200

@app.route('/get_dataframe_workcentre', methods=['GET'])
def get_dataframe_workcentre():
    global df_workcentre
    if df_workcentre.empty:
        return jsonify({'message': 'No df_workcentre available'}), 404
    return jsonify({'dataframe': df_workcentre.to_dict(orient='records')}), 200

if __name__ == '__main__':
    app.run(debug=True)
