import pymongo
import os
from flask import Flask, render_template, redirect, request, url_for #check meaning
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import config

app = Flask(__name__)

# constants are set in a config.py file
app.config['MONGO_URI'] = config.MONGO_URI
app.config['DB_NAME'] = config.DB_NAME

#creating a new instance of PyMongo and going to add the app object into that with a constructor method
mongo = PyMongo(app)


@app.route('/')
#route and function to display the recipe name and title,
@app.route('/browse_recipes')
def browse_recipes():
    courses = mongo.db.course.find()
    recipes = mongo.db.recipes.find()
    cuisine = mongo.db.cuisine.find()
    return render_template('browserecipes.html', recipes=recipes, courses=courses, cuisine=cuisine)

#returns recipes based on select options
@app.route('/filter_recipes', methods=["GET", "POST"])
def filter_recipes():
    recipes = mongo.db.recipes.find({"course_name": request.form.get('course')})
    return render_template('filteredrecipes.html', recipes=recipes)
    
   # return("There are no recipes to show. Please widen your search filters!")
   
# retrieves full recipe from database when a user clicks on'View Recipe' button in the 'Browse Recipes' page
@app.route('/display_recipe/<recipe_id>')
def display_recipe(recipe_id):
    return render_template('displayrecipe.html', recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)}))
    
# displays a form that allows the user to add a recipe to the database (only partially complete)
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html')        
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
        debug=True)