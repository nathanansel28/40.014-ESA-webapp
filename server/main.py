from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from typing import List
import pandas as pd
import csv
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel
from EDD import execute_edd_schedule, safe_literal_eval


app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Ensure the upload directory exists
UPLOAD_DIRECTORY = "static/files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

class ObjectiveSubmission(BaseModel):
    selectedObjective: str

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.post("/files/")
async def get_files(filenames: List[str] = Body(...)):
    file_paths = []
    for filename in filenames:
        file_path = f"{UPLOAD_DIRECTORY}/{filename}"
        if os.path.exists(file_path):
            file_paths.append({"filename": filename, "url": f"/static/files/{filename}"})
        else:
            file_paths.append({"filename": filename, "error": "File not found"})
    return JSONResponse(file_paths)

# @app.post("/convert_to_dataframe_bom")
# async def convert_to_dataframe_bom(data: List[dict]):
#     try:
#         df = pd.DataFrame(data)
#         # Save the DataFrame to a CSV file or handle it as needed
#         df.to_csv(os.path.join(UPLOAD_DIRECTORY, "converted_bom.csv"), index=False)
#         return {"message": "BOM data successfully converted to DataFrame"}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"message": str(e)})

# @app.post("/convert_to_dataframe_workcentre")
# async def convert_to_dataframe_workcentre(data: List[dict]):
#     try:
#         df = pd.DataFrame(data)
#         # Save the DataFrame to a CSV file or handle it as needed
#         df.to_csv(os.path.join(UPLOAD_DIRECTORY, "converted_workcentre.csv"), index=False)
#         return {"message": "Workcentre data successfully converted to DataFrame"}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"message": str(e)})

# @app.post("/convert_to_dataframe_bom")
# async def convert_to_dataframe_bom(data: List[dict]):
#     try:
#         # Log the type and content of the received data
#         logger.info(f"Received BOM data type: {type(data)}")
#         logger.info(f"Received BOM data content: {data}")

#         df = pd.DataFrame(data)

#         # Log the DataFrame type and head
#         logger.info(f"Converted BOM DataFrame type: {type(df)}")
#         logger.info(f"Converted BOM DataFrame head: \n{df.head()}")

#         # Save the DataFrame to a CSV file or handle it as needed
#         df.to_csv(os.path.join(UPLOAD_DIRECTORY, "converted_bom.csv"), index=False)
#         return {"message": "BOM data successfully converted to DataFrame"}
#     except Exception as e:
#         logger.error(f"Error converting BOM data to DataFrame: {str(e)}")
#         return JSONResponse(status_code=500, content={"message": str(e)})

# @app.post("/convert_to_dataframe_workcentre")
# async def convert_to_dataframe_workcentre(data: List[dict]):
#     try:
#         # Log the type and content of the received data
#         logger.info(f"Received Workcentre data type: {type(data)}")
#         logger.info(f"Received Workcentre data content: {data}")

#         df = pd.DataFrame(data)

#         # Log the DataFrame type and head
#         logger.info(f"Converted Workcentre DataFrame type: {type(df)}")
#         logger.info(f"Converted Workcentre DataFrame head: \n{df.head()}")

#         # Save the DataFrame to a CSV file or handle it as needed
#         df.to_csv(os.path.join(UPLOAD_DIRECTORY, "converted_workcentre.csv"), index=False)
#         return {"message": "Workcentre data successfully converted to DataFrame"}
#     except Exception as e:
#         logger.error(f"Error converting Workcentre data to DataFrame: {str(e)}")
#         return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/convert_to_dataframe_bom")
async def convert_to_dataframe_bom(data: List[dict]):
    try:
        df_bom = pd.DataFrame(data)
        df_bom = df_bom.dropna(subset=['operation'])
        logger.info(f"Received BOM data type: {type(data)}")
        logger.info(f"Received BOM data content: {data}")
        logger.info(f"Converted BOM DataFrame type: {type(df_bom)}")
        logger.info(f"Converted BOM DataFrame head: \n{df_bom.head()}")
        df_bom.to_csv(os.path.join(UPLOAD_DIRECTORY, "converted_bom.csv"), index=False)
        # df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)

        return {"message": "BOM data successfully converted to DataFrame"}
    except Exception as e:
        logger.error(f"Error converting BOM data to DataFrame: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/convert_to_dataframe_workcentre")
async def convert_to_dataframe_workcentre(data: List[dict]):
    try:
        df_workcentre = pd.DataFrame(data)
        df_workcentre = df_workcentre.dropna(how='all')
        logger.info(f"Received Workcentre data type: {type(data)}")
        logger.info(f"Received Workcentre data content: {data}")
        logger.info(f"Converted Workcentre DataFrame type: {type(df_workcentre)}")
        logger.info(f"Converted Workcentre DataFrame head: \n{df_workcentre.head()}")

        df_workcentre.to_csv(os.path.join(UPLOAD_DIRECTORY, "converted_workcentre.csv"), index=False)

        return {"message": "Workcentre data successfully converted to DataFrame"}
    except Exception as e:
        logger.error(f"Error converting Workcentre data to DataFrame: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})
    
# @app.post("/schedule")
# async def schedule_operations():
#     try:
#         logger.info("Starting the scheduling process.")

#         # Load BOM DataFrame
#         bom_path = os.path.join(UPLOAD_DIRECTORY, "converted_bom.csv")
#         if os.path.exists(bom_path):
#             df_bom = pd.read_csv(bom_path)
#             logger.info("BOM DataFrame loaded successfully.")
#         else:
#             logger.error(f"BOM file not found at path: {bom_path}")
#             return JSONResponse(status_code=404, content={"message": "BOM file not found"})

#         # Load Workcentre DataFrame
#         workcentre_path = os.path.join(UPLOAD_DIRECTORY, "converted_workcentre.csv")
#         if os.path.exists(workcentre_path):
#             df_workcentre = pd.read_csv(workcentre_path)
#             logger.info("Workcentre DataFrame loaded successfully.")
#         else:
#             logger.error(f"Workcentre file not found at path: {workcentre_path}")
#             return JSONResponse(status_code=404, content={"message": "Workcentre file not found"})

#         # Convert the predecessor_operations column
#         df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)
#         logger.info("Converted predecessor_operations in BOM DataFrame.")

#         # Load operations
#         operations = load_operations(df_bom)
#         logger.info("Operations loaded successfully.")

#         # Load factory
#         factory = load_factory(df_workcentre)
#         logger.info("Factory loaded successfully.")

#         # Run the EDD scheduling algorithm
#         EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
#         logger.info("EDD scheduling algorithm executed successfully.")

#         # Format the schedule and save to CSV
#         df_scheduled = format_schedule(EDD_scheduled_operations, factory)
#         scheduled_csv_path = os.path.join(UPLOAD_DIRECTORY, "scheduled.csv")
#         df_scheduled.to_csv(scheduled_csv_path, index=False)
#         logger.info(f"Schedule saved successfully to {scheduled_csv_path}.")

#         return {"message": "Scheduling completed successfully", "schedule_url": f"/static/files/scheduled.csv"}
#     except Exception as e:
#         logger.error(f"Error in scheduling operations: {str(e)}")
#         return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/schedule")
async def schedule_operations():
    try:
        logger.info("Starting the scheduling process.")

        # Load BOM DataFrame
        bom_path = os.path.join(UPLOAD_DIRECTORY, "converted_bom.csv")
        if os.path.exists(bom_path):
            df_bom = pd.read_csv(bom_path)
            df_bom = df_bom.dropna(subset=['operation'])
            logger.info("BOM DataFrame loaded successfully.")
        else:
            logger.error(f"BOM file not found at path: {bom_path}")
            return JSONResponse(status_code=404, content={"message": "BOM file not found"})

        # Load Workcentre DataFrame
        workcentre_path = os.path.join(UPLOAD_DIRECTORY, "converted_workcentre.csv")
        if os.path.exists(workcentre_path):
            df_workcentre = pd.read_csv(workcentre_path)
            df_workcentre = df_workcentre.dropna(how='all')
            logger.info("Workcentre DataFrame loaded successfully.")
        else:
            logger.error(f"Workcentre file not found at path: {workcentre_path}")
            return JSONResponse(status_code=404, content={"message": "Workcentre file not found"})

        # Execute EDD scheduling process
        schedule_path = execute_edd_schedule(df_bom, df_workcentre)
        logger.info(f"Scheduling completed successfully. Schedule saved at: {schedule_path}")

        return {"message": "Scheduling completed successfully", "schedule_url": f"/static/files/scheduled.csv"}
    except Exception as e:
        logger.error(f"Error in scheduling operations: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})
    
# @app.post("/schedule")
# async def schedule_operations():
#     try:
#         df_bom = pd.read_csv(os.path.join(UPLOAD_DIRECTORY, "converted_bom.csv"))
#         df_workcentre = pd.read_csv(os.path.join(UPLOAD_DIRECTORY, "converted_workcentre.csv"))

#         df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)
#         operations = load_operations(df_bom)
#         factory = load_factory(df_workcentre)

#         EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
#         df_scheduled = format_schedule(EDD_scheduled_operations, factory)

#         scheduled_csv_path = os.path.join(UPLOAD_DIRECTORY, "scheduled.csv")
#         df_scheduled.to_csv(scheduled_csv_path, index=False)

#         return {"message": "Scheduling completed successfully", "schedule_url": f"/static/files/scheduled.csv"}
#     except Exception as e:
#         logger.error(f"Error in scheduling operations: {str(e)}")
#         return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/api/submit-objective")
async def submit_objective(objective_submission: ObjectiveSubmission):
    if objective_submission.selectedObjective == "EDD":
        response = await schedule_operations()
        logger.info("Success")
        return response
    else:
        logger.info("Objective not handled: %s", objective_submission.selectedObjective)
        return {"message": f"Objective {objective_submission.selectedObjective} is not handled yet."}

    logger.info("Objective submission complete")
# @app.post("/api/submit-objective")
# async def submit_objective(objective_submission: ObjectiveSubmission):
#     if objective_submission.selectedObjective == "EDD":
#         response = schedule_operations()
#         logger.info("Success")
#         return response
#     else:
#         logger.info("walao eh")
#         return {"message": f"Objective {objective_submission.selectedObjective} is not handled yet."}
#     logger.info("Objective submission complete")

# from fastapi import FastAPI, File, UploadFile, Body
# from fastapi.responses import FileResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles
# import os
# from typing import List
# import pandas as pd
# import csv
# from fastapi.middleware.cors import CORSMiddleware

# #This setup allows you to upload files, check their existence, and 
# #access them via URLs in the static/files directory.

# app = FastAPI()

# # Mount the static files directory
# app.mount("/static", StaticFiles(directory="static"), name="static")
# # Mounts the directory named "static" so files in this directory can be accessed via /static

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )
# # Adds middleware to allow requests from any origin (e.g., different websites or servers).

# # Ensure the directory exists
# UPLOAD_DIRECTORY = "static/files"
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

# # Ensure the directory exists
# UPLOAD_DIRECTORY = "static/files"
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
#     with open(file_location, "wb") as f:
#         f.write(await file.read())
#     return {"info": f"file '{file.filename}' saved at '{file_location}'"}

# @app.post("/files/")
# async def get_files(filenames: List[str] = Body(...)):
#     file_paths = []
#     for filename in filenames:
#         file_path = f"{UPLOAD_DIRECTORY}/{filename}"
#         if os.path.exists(file_path):
#             file_paths.append({"filename": filename, "url": f"/static/files/{filename}"})
#         else:
#             file_paths.append({"filename": filename, "error": "File not found"})
#     return JSONResponse(file_paths)

# from fastapi import FastAPI, File, UploadFile, Body, Request
# from fastapi.responses import JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# from csv_to_dataframe import convert_to_dataframe
# from ast import literal_eval
# from EDD import load_factory, load_operations, EDD_schedule_operations, format_schedule
# import os
# from typing import List
# import logging

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize FastAPI
# app = FastAPI()

# # Mount the static files directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Ensure the upload directory exists
# UPLOAD_DIRECTORY = "static/files"
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

# # Global DataFrames
# df_bom = pd.DataFrame()
# df_workcentre = pd.DataFrame()

# def safe_literal_eval(val):
#     try:
#         return literal_eval(val)
#     except (ValueError, SyntaxError) as e:
#         logging.error(f"Error parsing value: {val} - {e}")
#         return []

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
#         with open(file_location, "wb") as f:
#             f.write(await file.read())
#         logging.info(f"File '{file.filename}' saved at '{file_location}'")
#         return {"info": f"file '{file.filename}' saved at '{file_location}'"}
#     except Exception as e:
#         logging.error(f"Error in upload_file: {e}")
#         return JSONResponse({'error': str(e)}, status_code=500)

# @app.post("/files/")
# async def get_files(filenames: List[str] = Body(...)):
#     try:
#         file_paths = []
#         for filename in filenames:
#             file_path = f"{UPLOAD_DIRECTORY}/{filename}"
#             if os.path.exists(file_path):
#                 file_paths.append({"filename": filename, "url": f"/static/files/{filename}"})
#             else:
#                 file_paths.append({"filename": filename, "error": "File not found"})
#         return JSONResponse(file_paths)
#     except Exception as e:
#         logging.error(f"Error in get_files: {e}")
#         return JSONResponse({'error': str(e)}, status_code=500)
    
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the File Upload API"}

# @app.options("/convert_to_dataframe_bom")
# async def handle_options_bom():
#     return JSONResponse({"message": "Options request allowed"}, status_code=200, headers={
#         "Access-Control-Allow-Methods": "POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",
#     })

# @app.post("/convert_to_dataframe_bom")
# async def convert_to_dataframe_bom(request: Request):
#     global df_bom
#     try:
#         csv_data = await request.json()
#         logging.info(f"Received BOM Data: {csv_data}")

#         # Ensure the data is correctly received
#         if not csv_data:
#             raise ValueError("No data received in the request")

#         # Convert received data to DataFrame
#         df_bom = convert_to_dataframe(csv_data)
#         df_bom.to_csv('df_bom.csv', index=False)  # Saving to a CSV file as an example

#         # Verify the DataFrame creation
#         logging.info("DataFrame df_bom after conversion:")
#         logging.info(df_bom)

#         return JSONResponse({'message': 'df_bom created successfully', 'dataframe': df_bom.to_dict(orient='records')}, status_code=200)
#     except pd.errors.ParserError as e:
#         logging.error(f"Error parsing CSV data in convert_to_dataframe_bom: {e}")
#         return JSONResponse({'error': 'CSV parsing error', 'details': str(e)}, status_code=500)
#     except ValueError as e:
#         logging.error(f"Value error in convert_to_dataframe_bom: {e}")
#         return JSONResponse({'error': 'Value error', 'details': str(e)}, status_code=500)
#     except Exception as e:
#         logging.error(f"Unexpected error in convert_to_dataframe_bom: {e}")
#         return JSONResponse({'error': 'Unexpected error', 'details': str(e)}, status_code=500)

# @app.options("/convert_to_dataframe_workcentre")
# async def handle_options_workcentre():
#     return JSONResponse({"message": "Options request allowed"}, status_code=200, headers={
#         "Access-Control-Allow-Methods": "POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",
#     })

# @app.post("/convert_to_dataframe_workcentre")
# async def convert_to_dataframe_workcentre(request: Request):
#     global df_workcentre
#     try:
#         csv_data = await request.json()
#         logging.info(f"Received WorkCentre Data: {csv_data}")

#         # Ensure the data is correctly received
#         if not csv_data:
#             raise ValueError("No data received in the request")

#         # Convert received data to DataFrame
#         df_workcentre = convert_to_dataframe(csv_data)
#         df_workcentre.to_csv('df_workcentre.csv', index=False)  # Saving to a CSV file as an example

#         # Verify the DataFrame creation
#         logging.info("DataFrame df_workcentre after conversion:")
#         logging.info(df_workcentre)

#         return JSONResponse({'message': 'df_workcentre created successfully', 'dataframe': df_workcentre.to_dict(orient='records')}, status_code=200)
#     except pd.errors.ParserError as e:
#         logging.error(f"Error parsing CSV data in convert_to_dataframe_workcentre: {e}")
#         return JSONResponse({'error': 'CSV parsing error', 'details': str(e)}, status_code=500)
#     except ValueError as e:
#         logging.error(f"Value error in convert_to_dataframe_workcentre: {e}")
#         return JSONResponse({'error': 'Value error', 'details': str(e)}, status_code=500)
#     except Exception as e:
#         logging.error(f"Unexpected error in convert_to_dataframe_workcentre: {e}")
#         return JSONResponse({'error': 'Unexpected error', 'details': str(e)}, status_code=500)

# @app.options("/api/submit-objective")
# async def handle_options_objective():
#     return JSONResponse({"message": "Options request allowed"}, status_code=200, headers={
#         "Access-Control-Allow-Methods": "POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",
#     })

# @app.post("/api/submit-objective")
# async def submit_objective(request: Request):
#     global df_bom, df_workcentre
#     try:
#         data = await request.json()
#         selected_objective = data.get('selectedObjective')

#         if selected_objective == 'EDD':
#             logging.info("Before parsing predecessor_operations:")
#             logging.info(df_bom)

#             df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)

#             logging.info("After parsing predecessor_operations:")
#             logging.info(df_bom)

#             operations = load_operations(df_bom)
#             factory = load_factory(df_workcentre)
#             EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
#             df_scheduled = format_schedule(EDD_scheduled_operations, factory)
#             df_scheduled.to_csv("static/files/scheduled.csv")
#             return JSONResponse({'message': 'EDD heuristic executed successfully'}, status_code=200)
#         else:
#             return JSONResponse({'error': 'Objective not implemented yet'}, status_code=400)
#     except Exception as e:
#         logging.error(f"Error in submit_objective: {e}")
#         return JSONResponse({'error': str(e)}, status_code=500)

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the File Upload API"}

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the File Upload API"}

# @app.options("/api/submit-objective")
# async def handle_options_objective():
#     return JSONResponse({"message": "Options request allowed"}, status_code=200, headers={
#         "Access-Control-Allow-Methods": "POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",
#     })

# @app.post("/api/submit-objective")
# async def submit_objective(request: Request):
#     global df_bom, df_workcentre
#     data = await request.json()
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
#         return JSONResponse({'message': 'EDD heuristic executed successfully'}, status_code=200)
#     else:
#         return JSONResponse({'error': 'Objective not implemented yet'}, status_code=400)

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the File Upload API"}


# from fastapi import FastAPI, File, UploadFile, Body, Request
# from fastapi.responses import JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# from csv_to_dataframe import convert_to_dataframe
# from ast import literal_eval
# from EDD import load_factory, load_operations, EDD_schedule_operations, format_schedule
# import os
# from typing import List

# # Initialize FastAPI
# app = FastAPI()

# # Mount the static files directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Ensure the upload directory exists
# UPLOAD_DIRECTORY = "static/files"
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

# # Global DataFrames
# df_bom = pd.DataFrame() 
# df_workcentre = pd.DataFrame()

# def safe_literal_eval(val):
#     try:
#         return literal_eval(val)
#     except (ValueError, SyntaxError) as e:
#         print(f"Error parsing value: {val} - {e}")
#         return []

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
#     with open(file_location, "wb") as f:
#         f.write(await file.read())
#     return {"info": f"file '{file.filename}' saved at '{file_location}'"}

# @app.post("/files/")
# async def get_files(filenames: List[str] = Body(...)):
#     file_paths = []
#     for filename in filenames:
#         file_path = f"{UPLOAD_DIRECTORY}/{filename}"
#         if os.path.exists(file_path):
#             file_paths.append({"filename": filename, "url": f"/static/files/{filename}"})
#         else:
#             file_paths.append({"filename": filename, "error": "File not found"})
#     return JSONResponse(file_paths)

# @app.options("/convert_to_dataframe_bom")
# async def handle_options_bom():
#     return JSONResponse({"message": "Options request allowed"}, status_code=200, headers={
#         "Access-Control-Allow-Methods": "POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",
#     })

# @app.post("/convert_to_dataframe_bom")
# async def convert_to_dataframe_bom(request: Request):
#     global df_bom
#     try:
#         csv_data = await request.json()
#         print("Received BOM Data:", csv_data)
#         df_bom = convert_to_dataframe(csv_data)
#         df_bom.to_csv('df_bom.csv', index=False)  # Saving to a CSV file as an example
#         print("DataFrame df_bom after conversion:")
#         print(df_bom)
#         return JSONResponse({'message': 'df_bom created successfully', 'dataframe': df_bom.to_dict(orient='records')}, status_code=200)
#     except Exception as e:
#         print(f"Error in convert_to_dataframe_bom: {e}")
#         return JSONResponse({'error': str(e)}, status_code=500)

# @app.options("/convert_to_dataframe_workcentre")
# async def handle_options_workcentre():
#     return JSONResponse({"message": "Options request allowed"}, status_code=200, headers={
#         "Access-Control-Allow-Methods": "POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",
#     })

# @app.post("/convert_to_dataframe_workcentre")
# async def convert_to_dataframe_workcentre(request: Request):
#     global df_workcentre
#     try:
#         csv_data = await request.json()
#         print("Received WorkCentre Data:", csv_data)
#         df_workcentre = convert_to_dataframe(csv_data)
#         df_workcentre.to_csv('df_workcentre.csv', index=False)  # Saving to a CSV file as an example
#         print("DataFrame df_workcentre after conversion:")
#         print(df_workcentre)
#         return JSONResponse({'message': 'df_workcentre created successfully', 'dataframe': df_workcentre.to_dict(orient='records')}, status_code=200)
#     except Exception as e:
#         print(f"Error in convert_to_dataframe_workcentre: {e}")
#         return JSONResponse({'error': str(e)}, status_code=500)

# @app.options("/api/submit-objective")
# async def handle_options_objective():
#     return JSONResponse({"message": "Options request allowed"}, status_code=200, headers={
#         "Access-Control-Allow-Methods": "POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",
#     })

# @app.post("/api/submit-objective")
# async def submit_objective(request: Request):
#     global df_bom, df_workcentre
#     data = await request.json()
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
#         return JSONResponse({'message': 'EDD heuristic executed successfully'}, status_code=200)
#     else:
#         return JSONResponse({'error': 'Objective not implemented yet'}, status_code=400)

# # @app.get("/")
# # def read_root():
# #     return {"message": "Welcome to the File Upload API"}
