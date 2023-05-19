from flask import Flask
from datetime import datetime
app = Flask(__name__)

data = {
    "drinks": [
        {
            "name": "Grape", 
            "description": "Delicious grape fruit drink",
            "date": datetime.now()
            },
            {
            "name": "Lemon", 
            "description": "Undiluted lemon fruit drink",
            "date": datetime.now()
            },
            {
            "name": "Mango", 
            "description": "This is a mango fruit",
            "date": datetime.now() 
        }
    ]
} 

@app.route("/")
def index():
        return "Welcome To My Drinks API"

@app.route('/drinks')
def get_drinks():
    return data


if __name__ == "__main__":
    app.debug = True
    app.run()