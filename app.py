# Import Tools
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set Up App (a.k.a. Flask) Routes
# tells Flask what to display when we're looking at the home page, index.html 
@app.route("/")
def index():
    # uses PyMongo to find the "mars" collection in our database
    mars = mongo.db.mars.find_one()
    # tells Flask to return an HTML template using an index.html file.
    return render_template("index.html", mars=mars)

# Add next route and function to our code
# Defines the route, Run the function created/defined beneath
@app.route("/scrape")
# allow us to access the database, scrape new data using our scraping.py script,....
# .... update the database, and return a message when successful
def scrape():
    # Assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # Create a new variable to hold the newly scraped data
    mars_data = scraping.scrape_all()
    # Update the database with the newley gathered data
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

# Inserting data, if no identical record already exists
#.update_one(query_parameter, {"$set": data}, options)
# query_parameter, specify a field (e.g. {"news_title": "Mars Landing Successful"})
# MongoDB will update a document with a matching news_title.
# If, {} are empty it will update the first matching document in the collection
# use the data we have stored in mars_data. The syntax used here is {"$set": data}. 
# This means that the document will be modified ("$set") with the data in question.
# upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and ....
# new data will always be saved (even if we haven't already created a document for it)
mars.update_one({}, {"$set":mars_data}, upsert=True)
# Navigate our page back to / where we can see the updated content
return redirect('/', code=302

# Tell Flask to Run
if __name__ == "__main__":
    app.run()