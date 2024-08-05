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
from LETSA import execute_LETSA_schedule
from LR import execute_LR_schedule
from SA import execute_SA_schedule

app = FastAPI()
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
        # df_workcentre = df_workcentre.dropna(subset=['workcenter'])
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
    
@app.post("/api/submit-objective")
async def submit_objective(objective_submission: ObjectiveSubmission):
    logger.info(f"Submit objective function called: {objective_submission.selectedObjective}")
    if objective_submission.selectedObjective == "EDD":
        response = await schedule_operations("EDD")
        return response

    elif objective_submission.selectedObjective == "LETSA":
        response = await schedule_operations("LETSA") 
        return {"message": "LETSA objective handled."}

    elif objective_submission.selectedObjective == "SA":
        response = await schedule_operations("SA") 
        return {"message": "SA objective handled."}

    elif objective_submission.selectedObjective == "LR":
        response = await schedule_operations("LR")
        return {"message": "LR objective handled."}

    else:
        logger.error("Error at submit objective in main.py")
        logger.error("Objective not handled: %s", objective_submission.selectedObjective)
        return {"message": f"Objective {objective_submission.selectedObjective} is not handled yet."}

@app.post("/schedule")
async def schedule_operations(heuristic):
    logger.info("Running schedule_operations")
    try:
        bom_path = os.path.join(UPLOAD_DIRECTORY, "converted_bom.csv")
        if os.path.exists(bom_path):
            df_bom = pd.read_csv(bom_path)
            df_bom = df_bom.dropna(subset=['operation'])
        else:
            logger.error(f"BOM file not found at path: {bom_path}")
            return JSONResponse(status_code=404, content={"message": "BOM file not found"})

        workcentre_path = os.path.join(UPLOAD_DIRECTORY, "converted_workcentre.csv")
        if os.path.exists(workcentre_path):
            df_workcentre = pd.read_csv(workcentre_path)
            df_workcentre = df_workcentre.dropna(how='all')
        else:
            logger.error(f"Workcentre file not found at path: {workcentre_path}")
            return JSONResponse(status_code=404, content={"message": "Workcentre file not found"})

        if heuristic == "EDD": 
            schedule_path = execute_edd_schedule(df_bom, df_workcentre)
        elif heuristic == "LETSA": 
            schedule_path = execute_LETSA_schedule(df_bom, df_workcentre)
        elif heuristic == "LR": 
            schedule_path = execute_LR_schedule(df_bom, df_workcentre)
        elif heuristic == "SA": 
            schedule_path = execute_SA_schedule(df_bom, df_workcentre)

        if not schedule_path:
            logger.info(schedule_path)
            logger.error("execute_edd_schedule returned None")
            return JSONResponse(status_code=500, content={"message": "Scheduling failed"})
        logger.info("schedule_operations success")
        return {"message": "Scheduling completed successfully", "schedule_url": f"/static/files/scheduled.csv"}
    
    except Exception as e:
        logger.info("Error")
        logger.error(f"Error in scheduling operations: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})
    
