# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from csv_to_dataframe import convert_to_dataframe
# import pandas as pd
# from ast import literal_eval

# app = Flask(__name__)
# CORS(app)

# df_bom = pd.DataFrame() 
# df_workcentre = pd.DataFrame()

# from EDD import load_factory, load_operations, EDD_schedule_operations, format_schedule

# def safe_literal_eval(val):
#     try:
#         return literal_eval(val)
#     except (ValueError, SyntaxError) as e:
#         print(f"Error parsing value: {val} - {e}")
#         return []

# @app.route('/convert_to_dataframe_bom', methods=['POST', 'OPTIONS'])
# def convert_to_dataframe_bom():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_bom
#     csv_data = request.get_json()
#     df_bom = convert_to_dataframe(csv_data)
#     df_bom.to_csv('df_bom.csv', index=False)  # Saving to a CSV file as an example
#     print("DataFrame df_bom after conversion:")
#     print(df_bom)
#     return jsonify({'message': 'df_bom created successfully', 'dataframe': df_bom.to_dict(orient='records')}), 200

# @app.route('/convert_to_dataframe_workcentre', methods=['POST', 'OPTIONS'])
# def convert_to_dataframe_workcentre():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_workcentre
#     csv_data = request.get_json()
#     df_workcentre = convert_to_dataframe(csv_data)
#     df_workcentre.to_csv('df_workcentre.csv', index=False)  # Saving to a CSV file as an example
#     print("DataFrame df_workcentre after conversion:")
#     print(df_workcentre)
#     return jsonify({'message': 'df_workcentre created successfully', 'dataframe': df_workcentre.to_dict(orient='records')}), 200

# @app.route('/api/submit-objective', methods=['POST', 'OPTIONS'])
# def submit_objective():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_bom, df_workcentre

#     data = request.get_json()
#     selected_objective = data.get('selectedObjective')

#     if selected_objective == 'EDD':
#         print("Before parsing predecessor_operations:")
#         print(df_bom)
        
#         df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)
        
#         print("After parsing predecessor_operations:")
#         print(df_bom)
        
#         operations = load_operations(df_bom)
#         factory = load_factory(df_workcentre)
#         EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
#         df_scheduled = format_schedule(EDD_scheduled_operations, factory)
#         df_scheduled.to_csv("static/files/scheduled.csv")
#         return jsonify({'message': 'EDD heuristic executed successfully'}), 200
#     # Implement similar logic for other heuristics here
#     else:
#         return jsonify({'error': 'Objective not implemented yet'}), 400

# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/api/submit-objective', methods=['POST', 'OPTIONS'])
# def submit_objective():
#     data = request.get_json()
#     selected_objective = data.get('selectedObjective')

#     if selected_objective == 'EDD':
#         # Parse predecessor operations correctly
        
#         operations = load_operations(df_bom)
#         factory = load_factory(df_workcentre)
#         EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
#         df_scheduled = format_schedule(EDD_scheduled_operations, factory)
#         df_scheduled.to_csv("static/files/scheduled.csv")
#         return jsonify({'message': 'EDD heuristic executed successfully'}), 200
#     else:
#         return jsonify({'error': 'Objective not implemented yet'}), 400

# @app.route('/api/submit-objective', methods=['POST', 'OPTIONS'])
# def submit_objective():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_bom, df_workcentre

#     data = request.get_json()
#     selected_objective = data.get('selectedObjective')

#     if selected_objective == 'EDD':

#         # df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
#         # df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(lambda x: literal_eval(x) if "[" in x else [])
#         # for i in range(len(df_bom)):
#         #     df_bom.at[i, 'predecessor_operations'] = literal_eval(df_bom.at[i, 'predecessor_operations'])
#         df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)
#         operations = load_operations(df_bom)
#         factory = load_factory(df_workcentre)
#         EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
#         df_scheduled = format_schedule(EDD_scheduled_operations, factory)
#         df_scheduled.to_csv("static/files/scheduled.csv")
#         return jsonify({'message': 'EDD heuristic executed successfully'}), 200
#     # Implement similar logic for other heuristics here
#     else:
#         return jsonify({'error': 'Objective not implemented yet'}), 400

# if __name__ == '__main__':
#     app.run(debug=True)

# app.py
# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from csv_to_dataframe import convert_to_dataframe
from ast import literal_eval
from EDD import load_factory, load_operations, EDD_schedule_operations, format_schedule

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

df_bom = pd.DataFrame() 
df_workcentre = pd.DataFrame()

def safe_literal_eval(val):
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing value: {val} - {e}")
        return []

@app.route('/convert_to_dataframe_bom', methods=['POST', 'OPTIONS'])
def convert_to_dataframe_bom():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = None
        if request.headers.get('Access-Control-Request-Headers'):
            headers = request.headers['Access-Control-Request-Headers']
        h = response.headers

        h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        h['Access-Control-Allow-Headers'] = headers

        return response

    global df_bom
    try:
        csv_data = request.get_json()
        print("Received BOM Data:", csv_data)
        df_bom = convert_to_dataframe(csv_data)
        df_bom.to_csv('df_bom.csv', index=False)  # Saving to a CSV file as an example
        print("DataFrame df_bom after conversion:")
        print(df_bom)
        return jsonify({'message': 'df_bom created successfully', 'dataframe': df_bom.to_dict(orient='records')}), 200
    except Exception as e:
        print(f"Error in convert_to_dataframe_bom: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/convert_to_dataframe_workcentre', methods=['POST', 'OPTIONS'])
def convert_to_dataframe_workcentre():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = None
        if request.headers.get('Access-Control-Request-Headers'):
            headers = request.headers['Access-Control-Request-Headers']
        h = response.headers

        h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        h['Access-Control-Allow-Headers'] = headers

        return response

    global df_workcentre
    try:
        csv_data = request.get_json()
        print("Received WorkCentre Data:", csv_data)
        df_workcentre = convert_to_dataframe(csv_data)
        df_workcentre.to_csv('df_workcentre.csv', index=False)  # Saving to a CSV file as an example
        print("DataFrame df_workcentre after conversion:")
        print(df_workcentre)
        return jsonify({'message': 'df_workcentre created successfully', 'dataframe': df_workcentre.to_dict(orient='records')}), 200
    except Exception as e:
        print(f"Error in convert_to_dataframe_workcentre: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-objective', methods=['POST', 'OPTIONS'])
def submit_objective():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = None
        if request.headers.get('Access-Control-Request-Headers'):
            headers = request.headers['Access-Control-Request-Headers']
        h = response.headers

        h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        h['Access-Control-Allow-Headers'] = headers

        return response

    global df_bom, df_workcentre

    data = request.get_json()
    selected_objective = data.get('selectedObjective')

    if selected_objective == 'EDD':
        print("Before parsing predecessor_operations:")
        print(df_bom)
        
        df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)
        
        print("After parsing predecessor_operations:")
        print(df_bom)
        
        operations = load_operations(df_bom)
        factory = load_factory(df_workcentre)
        EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
        df_scheduled = format_schedule(EDD_scheduled_operations, factory)
        df_scheduled.to_csv("static/files/scheduled.csv")
        return jsonify({'message': 'EDD heuristic executed successfully'}), 200
    else:
        return jsonify({'error': 'Objective not implemented yet'}), 400

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# from ast import literal_eval

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# # Global DataFrames
# df_bom = pd.DataFrame()
# df_workcentre = pd.DataFrame()

# def convert_to_dataframe(csv_data):
#     try:
#         # Assuming csv_data is a list of dictionaries
#         df = pd.DataFrame(csv_data)
#         return df
#     except Exception as e:
#         print(f"Error converting to dataframe: {e}")
#         return pd.DataFrame()

# @app.route('/convert_to_dataframe_bom', methods=['POST', 'OPTIONS'])
# def convert_to_dataframe_bom():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         # Allow the requested method(s)
#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'

#         # Allow the requested headers
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_bom
#     try:
#         csv_data = request.get_json()
#         print(f"Received CSV data: {csv_data}")
#         df_bom = convert_to_dataframe(csv_data)
#         print("Converted DataFrame:")
#         print(df_bom)
#         df_bom.to_csv('df_bom.csv', index=False)  # Saving to a CSV file as an example
#         return jsonify({'message': 'df_bom created successfully', 'dataframe': df_bom.to_dict(orient='records')}), 200
#     except Exception as e:
#         print(f"Error in convert_to_dataframe_bom: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/convert_to_dataframe_workcentre', methods=['POST', 'OPTIONS'])
# def convert_to_dataframe_workcentre():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         # Allow the requested method(s)
#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'

#         # Allow the requested headers
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_workcentre
#     try:
#         csv_data = request.get_json()
#         print(f"Received CSV data: {csv_data}")
#         df_workcentre = convert_to_dataframe(csv_data)
#         print("Converted DataFrame:")
#         print(df_workcentre)
#         df_workcentre.to_csv('df_workcentre.csv', index=False)  # Saving to a CSV file as an example
#         return jsonify({'message': 'df_workcentre created successfully', 'dataframe': df_workcentre.to_dict(orient='records')}), 200
#     except Exception as e:
#         print(f"Error in convert_to_dataframe_workcentre: {e}")
#         return jsonify({'error': str(e)}), 500
    
# @app.route('/api/submit-objective', methods=['POST', 'OPTIONS'])
# def submit_objective():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         # Allow the requested method(s)
#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#         # Allow the requested headers
#         h['Access-Control-Allow-Headers'] = headers
#         return response

#     global df_bom, df_workcentre

#     try:
#         data = request.get_json()
#         selected_objective = data.get('selectedObjective')

#         if selected_objective == 'EDD':
#             print("Before parsing predecessor_operations:")
#             print(df_bom)
#             df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)
#             print("After parsing predecessor_operations:")
#             print(df_bom)
#             operations = load_operations(df_bom)
#             factory = load_factory(df_workcentre)
#             EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
#             df_scheduled = format_schedule(EDD_scheduled_operations, factory)
#             df_scheduled.to_csv("static/files/scheduled.csv")
#             return jsonify({'message': 'EDD heuristic executed successfully'}), 200
#         # Implement similar logic for other heuristics here
#         else:
#             return jsonify({'error': 'Objective not implemented yet'}), 400
#     except Exception as e:
#         print(f"Error in submit_objective: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/get_dataframe_bom', methods=['GET'])
# def get_dataframe_bom():
#     global df_bom
#     if df_bom.empty:
#         return jsonify({'message': 'No df_bom available'}), 404
#     return jsonify({'dataframe': df_bom.to_dict(orient='records')}), 200

# @app.route('/get_dataframe_workcentre', methods=['GET'])
# def get_dataframe_workcentre():
#     global df_workcentre
#     if df_workcentre.empty:
#         return jsonify({'message': 'No df_workcentre available'}), 404
#     return jsonify({'dataframe': df_workcentre.to_dict(orient='records')}), 200

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# # Global DataFrames
# df_bom = pd.DataFrame()
# df_workcentre = pd.DataFrame()

# @app.route('/convert_to_dataframe_bom', methods=['POST', 'OPTIONS'])
# def convert_to_dataframe_bom():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         # Allow the requested method(s)
#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'

#         # Allow the requested headers
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_bom
#     csv_data = request.get_json()
#     df_bom = convert_to_dataframe(csv_data)
#     print(df_bom)
#     df_bom.to_csv('df_bom.csv', index=False)  # Saving to a CSV file as an example
#     return jsonify({'message': 'df_bom created successfully', 'dataframe': df_bom.to_dict(orient='records')}), 200

# @app.route('/convert_to_dataframe_workcentre', methods=['POST', 'OPTIONS'])
# def convert_to_dataframe_workcentre():
#     if request.method == 'OPTIONS':
#         response = app.make_default_options_response()
#         headers = None
#         if request.headers.get('Access-Control-Request-Headers'):
#             headers = request.headers['Access-Control-Request-Headers']
#         h = response.headers

#         # Allow the requested method(s)
#         h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'

#         # Allow the requested headers
#         h['Access-Control-Allow-Headers'] = headers

#         return response

#     global df_workcentre
#     csv_data = request.get_json()
#     df_workcentre = convert_to_dataframe(csv_data)
#     print(df_workcentre)
#     df_workcentre.to_csv('df_workcentre.csv', index=False)  # Saving to a CSV file as an example
#     return jsonify({'message': 'df_workcentre created successfully', 'dataframe': df_workcentre.to_dict(orient='records')}), 200

# @app.route('/get_dataframe_bom', methods=['GET'])
# def get_dataframe_bom():
#     global df_bom
#     if df_bom.empty:
#         return jsonify({'message': 'No df_bom available'}), 404
#     return jsonify({'dataframe': df_bom.to_dict(orient='records')}), 200

# @app.route('/get_dataframe_workcentre', methods=['GET'])
# def get_dataframe_workcentre():
#     global df_workcentre
#     if df_workcentre.empty:
#         return jsonify({'message': 'No df_workcentre available'}), 404
#     return jsonify({'dataframe': df_workcentre.to_dict(orient='records')}), 200

# if __name__ == '__main__':
#     app.run(debug=True)
