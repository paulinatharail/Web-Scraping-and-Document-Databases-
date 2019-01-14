from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os
import mission_to_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/MarsInfo"
mongo = PyMongo(app)
# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")



@app.route("/")
def index():
    mars_data = mongo.db.info.find_one()
    return render_template("index.html", listings=mars_data)



@app.route("/scrape")
def scraper():
    # conn = 'mongodb://localhost:27017'
    # client = pymongo.MongoClient(conn)

    # Define the 'MarsInfo' database in Mongo
    mars_info_before = mongo.db.info
    
    # Assign results of web-scraping to variable mars_data 
    mars_data = mission_to_mars.scrape()
    #mongo.db.info.insert_one(mars_data)

    app.config['MARS_hems'] = mars_data['Mars_Hemispheres']['url']
    #full_filename = os.path.join(app.config['MARS_hems'],'Mars_Hemispheres.png')
    full_filename = os.path.join(app.config['MARS_hems'])

    mars_data['Flask_Mars_Hems_URL'] = full_filename

    mars_info_before.update({}, mars_data, upsert=True)
    return redirect("/", code=302)





if __name__ == "__main__":
    app.run(debug=True)
