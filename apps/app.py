from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up our Flask routes: 
# one for the main HTML page everyone will view when visiting the web app
# and one to actually scrape new data
@app.route("/")
def index():
   mars = mongo.db.mars.find_one() #  find the “mars” collection in our database
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True) # upsert=True: create a new document if one doesn’t already exist.
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run(debug=True)
