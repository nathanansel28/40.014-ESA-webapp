gy﻿# Manufacturing Gantt App (Karen, Norah, Peck Yeok)
This project was built using these technologies.

- React.js
- Node.js
- AntDesign
- VsCode
- MUI
- Google-React-Charts

## Getting Started

Clone down this repository. You will need `node.js` and `git` installed globally on your machine. You would also need `Uvicorn`,  `FastApi` and  `Pandas` module installed.

In the event you need to download any of the above three modules, do:
1.  `pip install pandas` and/or
2.  `pip install fastapi` and/or
3.  `pip install uvicorn` 

## 🛠 Installation and Setup Instructions

There are three parts to this: Front-end,  Back-end (1) and Back-end (2), hence, you will need to run three different terminals to ensure that this website works!

## Back End Part 1

1. Open a new terminal, ensure that your directory is in the server folder (do `cd server`)

2. In the server directory, run `env\Scripts\activate`

3. Virtual env (env) should be created. Run `python -m uvicorn main:app --reload`

Uvicorn should be running on [http://127.0.0.1:8000]

## Back End Part 2

1. Open a new terminal, ensure that your directory is in the server folder (do `cd server`)
2. In the server directory, run `run flask`

Flask should be running on [http://127.0.0.1:5000]

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
