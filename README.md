# GANTT.: An Operations Scheduling Web App
Access a preview of our project here (read-only): https://nathanansel28.github.io/40.014-ESA-webapp/

## About GANTT.
Our web application is designed to help manufacturing companies optimise their assembly line scheduling. By incorporating heuristic methods, we aim to create an intuitive and efficient tool that addresses the complexities of large-scale scheduling. Our solution focuses on minimising makespan, time complexity, WIP cost, and/or number of tardy jobs. Ultimately, producing a schedule that can match the needs of all businesses, and enhance their productivity.

This project was built using these technologies.
- React.js
- Node.js
- AntDesign
- VsCode
- MUI
- timelines-charts

## Getting Started
Clone down this repository. You will need `node.js` and `git` installed globally on your machine. You would also need `Uvicorn`,  `FastApi` and  `Pandas` module installed.

# 🛠 Installation and Setup Instructions
There are two parts to this: back end and front end. Hence, you will need to run two different terminals to ensure that this website works!

## Back End 

1. Open a new terminal, ensure that your directory is in the server folder (do `cd server`)

2. In the server directory, run `env\Scripts\activate`

3. Virtual env (env) should be created. Run `python -m uvicorn main:app --reload`

4. Uvicorn should be running on [http://127.0.0.1:8000]

5. In the event you need to download any of the above three modules, do install the followings in your environment:
  1. `pip install pandas` and/or
  2.  `pip install fastapi` and/or
  3.  `pip install numpy` and/or
  4.  `pip install uvicorn`

6. If the terminal returns fatal error, do:
  1. `deactivate`
  2. `Remove-Item -Recurse -Force .\env`
  3. `python -m venv env`
  4. `.\env\Scripts\activate`
  5. `pip install -r requirements.txt`

## Front End

1. Open a new terminal, ensure that your directory is in the frontend folder. (do `cd frontend` )

1. Installation: `npm install`

1. In the project directory, you can run: `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.
The page will reload if you make edits.

## Usage Instructions

Open the project folder and Navigate to `/src/components/`. <br/>
You will find all the components used and you can edit your information accordingly.

Uploaded files would be in the `static\files` folder of backend server.

# Contributions
Nathan Ansel \
Lee Peck Yeok \
Georgia Karen Lau \
Kong Le'ann Norah \
Oon Eu Kuan Eugene \
Tan Chong Hao \
Long Yan Ting 
