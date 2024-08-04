from flask import Flask, request, jsonify
from flask_cors import CORS
from csv_to_dataframe import convert_to_dataframe

app = Flask(__name__)
CORS(app)

@app.route('/convert_to_dataframe', methods=['POST'])
def convert_to_dataframe_endpoint():
    csv_data = request.get_json()
    df = convert_to_dataframe(csv_data)
    print(df)
    # You can now process the DataFrame as needed
    # For example, you can save it to a file or database
    df.to_csv('output.csv', index=False)  # Saving to a CSV file as an example
    return jsonify({'message': 'DataFrame created successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
