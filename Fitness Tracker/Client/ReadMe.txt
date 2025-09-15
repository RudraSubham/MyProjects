Step-1: Install dependencies

Client: npm install styled-components @mui/material @mui/lab @mui/icons-material @emotion/styled @emotion/react axios react-router-dom react-redux redux-persist @reduxjs/toolkit dayjs @mui/x-date-pickers

Server:npm install bcrypt cors dotenv express jsonwebtoken mongoose nodemon

Step-2: Clean Files and set the folder structure

Step-3: Set environment variables in Server and connect to mongo DB

Dashboard Data Format:
{
        "totalCaloriesBurnt":13500,
        "totalWorkouts":6,
        "avgCaloriesBurntPerWorkout":2250,
        "totalWeeksCaloriesBurnt": {
            "weeks": [
                "17th",
                "18th",
                "19th",
                "20th",
                "21th",
                "22th",
                "23th"
            ],
            "caloriesBurned": [
                10500,
                0,
                0,
                0,
                0,
                0,
                13500
            ]
        },
        "pieChartData": [
            {
                "id":0,
                "value":6000,
                "label":"Legs"
            },
            {
                "id":1,
                "value":1500,
                "label":"Back"
            },
            {
                "id":2,
                "value":3750,
                "label":"Shoulder"
            },
            {
                "id":3,
                "value":2250,
                "label":"ABS"
            },
        ],
};