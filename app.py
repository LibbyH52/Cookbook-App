import pymongo
import os
from flask import Flask, render_template, redirect, request, url_for #check meaning
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import config
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# use os library to set constants
app.config['MONGO_URI'] = config.MONGO_URI
app.config['DB_NAME'] = config.DB_NAME

#creating a new instance of PyMongo and going to add the app object into that with a constructor method
mongo = PyMongo(app)


@app.route('/')
@app.route('/browse_recipes')
def browse_recipes():
    return render_template('browseRecipes.html', recipes=mongo.db.recipes.find())
        
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
        debug=True)