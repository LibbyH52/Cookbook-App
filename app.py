import pymongo
import os
from flask import Flask
#from config import * 

# use os library to set constant
#MONGODB_URI = os.getenv("MONGO_URI")
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
        debug=True)