from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_draft
import sys

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars_draft"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    # print(list(listings),file=sys.stdout)
    return render_template("index.html", mars=listings)



@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = scrape_mars_draft.scrape()
   
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
