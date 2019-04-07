import pymongo
import os
from flask import Flask, render_template, redirect, request, url_for #check meaning
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId #converts id passed from temlate in a form that's readable by Mongodb


app = Flask(__name__)

# constants are set in a config.py file
if app.config["DEBUG"] == True:
    import config
    app.config['MONGO_URI'] = config.MONGO_URI
    app.config['DB_NAME'] = config.DB_NAME
else:
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["DB_NAME"] = os.getenv("DB_NAME")

#creating a new instance of PyMongo and going to add the app object into that with a constructor method
mongo = PyMongo(app)

@app.route('/')


#route and function to display the recipe name and title, and apply filters
@app.route('/browse_recipes', methods=["GET", "POST"])
def browse_recipes():
    courses=mongo.db.course.find()
    cuisine=mongo.db.cuisine.find()
    recipes=mongo.db.recipes.find()
    allergens = mongo.db.allergens.find()
    if request.method == "POST":
        course= request.form.get("course")
        cuisine = request.form.get('cuisine')
        allergens=request.form.getlist("allergen")
    
        filter_recipes=mongo.db.recipes.find( {"$and": 
            [{"course_name" : course }, {"cuisine_name" : cuisine }, {"allergens" : { "$nin": allergens }} ] 
            
        })
            
        print(filter_recipes)
        return render_template('browserecipes.html', recipes=filter_recipes)
    else:
        recipes = mongo.db.recipes.aggregate([
                {"$sort": {"course_name": pymongo.DESCENDING}},
                {"$sort": {"cuisine_name": pymongo.ASCENDING}}
        ])
      
        return render_template('browserecipes.html', recipes=recipes, courses=courses, cuisine=cuisine, allergens=allergens)

# retrieves full recipe from database when a user clicks on'View Recipe' button
@app.route('/display_recipe/<recipe_id>')
def display_recipe(recipe_id):
    return render_template('displayrecipe.html', recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)}))

#selects a recipe and retreives from the database using its id and displays it in a form to allow the user to edit its properties
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    #get the recipe that matches the recipe id '_id' is the key 
    recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    return render_template("editrecipe.html", recipe=recipe, allergens=mongo.db.allergens.find())

#updates the database with edited recipe
@app.route('/update_recipe/<recipe_id>', methods=["GET", "POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    #access recipes collection and call the update function
    recipes.update({'_id':ObjectId(recipe_id)},
        #match form fields to keys in the recipes collection
        {
            'recipe_name': request.form.get('recipe_name').title(),
            'image_url' :request.form.get('image_url'),
            'author' :request.form.get('author').title(),
            'course_name': request.form.get('course_name').title(),
            'cuisine_name': request.form.get('cuisine_name').title(),
            'servings':request.form.get('servings'),
            'prep_time':request.form.get('prep_time'),
            'cook_time':request.form.get('cook_time'),
            'allergens':request.form.getlist('allergen'),
            'ingredients':request.form.getlist('ingredient'),
            'instructions':request.form.get('instructions')
        })
    return redirect(url_for('browse_recipes'))
    
    
# displays a form that allows the user to add a recipe to the database (only partially complete)
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', allergens=mongo.db.allergens.find())        

@app.route('/insert_recipe', methods=["GET", "POST"])
def insert_recipe():
    #get recipe collection
    recipes = mongo.db.recipes
    #then do a recipe insert and convert form to a dictionary, so can be understood by Mongodb
    recipes.insert_one(  {
            'recipe_name': request.form.get('recipe_name'),
            'image_url' :request.form.get('image_url'),
            'author' :request.form.get('author'),
            'course_name': request.form.get('course_name'),
            'cuisine_name': request.form.get('cuisine_name'),
            'servings':request.form.get('servings'),
            'prep_time':request.form.get('prep_time'),
            'cook_time':request.form.get('cook_time'),
            'allergens':request.form.getlist('allergen'),
            'ingredients':request.form.getlist('ingredient'),
            'instructions':request.form.get('instructions')
        })
    
    
    
    course_name=request.form.get('course_name')
   # adds new course and cuisine names, if not already there
    if not course_name == "":
        course = mongo.db.course.update(
            {"course_name": course_name},
            { "$setOnInsert": { "course_name": course_name },
        },
            upsert= True 
        ); 
    cuisine_name=request.form.get('cuisine_name')
    if not cuisine_name == "":
        cuisine = mongo.db.cuisine.update(
            {"cuisine_name": cuisine_name},
            { "$setOnInsert": { "cuisine_name": cuisine_name },
            },
            upsert= True 
            ); 
    return redirect(url_for('browse_recipes'))
    
#deletes a recipe
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect(url_for('browse_recipes'))
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
        debug=True)