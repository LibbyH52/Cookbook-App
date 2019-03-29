import pymongo
import os
from flask import Flask, render_template, redirect, request, url_for #check meaning
from flask_pymongo import PyMongo
from bson.objectid import ObjectId #converts id passed from temlate in a form that's readable by Mongodb
import config

app = Flask(__name__)

# constants are set in a config.py file
app.config['MONGO_URI'] = config.MONGO_URI
app.config['DB_NAME'] = config.DB_NAME

#creating a new instance of PyMongo and going to add the app object into that with a constructor method
mongo = PyMongo(app)


@app.route('/')
#route and function to display the recipe name and title, and apply filters
@app.route('/browse_recipes', methods=["GET", "POST"])
def browse_recipes():
    cuisine = mongo.db.cuisine.find()
    courses = mongo.db.course.find()
    allergens = mongo.db.allergens.find()
    if request.method == "POST":
        course = request.form.get("course")
        cuisine = request.form.get('cuisine')
        recipes= mongo.db.recipes.aggregate([{"$match" :{"$and": [{ "course_name" : course }, { "cuisine_name" : cuisine }  ]} }])
        return render_template('browserecipes.html', recipes=recipes)
    else:
        recipes = mongo.db.recipes.find()
        return render_template('browserecipes.html', recipes=recipes, courses=courses, cuisine=cuisine)

# retrieves full recipe from database when a user clicks on'View Recipe' button in the 'Browse Recipes' page
@app.route('/display_recipe/<recipe_id>')
def display_recipe(recipe_id):
    return render_template('displayrecipe.html', recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)}))

#selects a recipe and retreives from the database using its id and displays it in a form to allow the user to edit its properties
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    #get the recipe that matches the recipe id '_id' is the key 
    recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    #list of collections to populate form for editing
    cuisine = mongo.db.cuisine.find()
    courses = mongo.db.course.find()
    #allergens = mongo.db.allergens.find()
    return render_template("editrecipe.html", recipe=recipe, courses=courses, cuisine=cuisine)
    
# displays a form that allows the user to add a recipe to the database (only partially complete)
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', courses=mongo.db.course.find(), 
                        cuisine=mongo.db.cuisine.find(), allergens=mongo.db.allergens.find())        

@app.route('/insert_recipe', methods=["GET", "POST"])
def insert_recipe():
    #get recipe collection
    recipes = mongo.db.recipes
    #then do a recipe insert and convert form to a dictionary, so can be understood by Mongodb
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('browse_recipes'))
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
        debug=True)