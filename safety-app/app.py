#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request, render_template
import ast
import pymongo
import os
import pandas as pd


import numpy as np
import pandas as pd# Import from app/features.py.
# from features import FEATURES# Initialize the app and set a secret_key.
app = Flask(__name__)
# app.secret_key = 'something_secret'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/api', methods=['POST'])
def api():
    """Handle request and output model score in json format."""
    # Handle empty requests.
    if not request.json:
        return jsonify({'error': 'no request received'})    # Parse request args into feature array for prediction.
    
    route_list = parse_args(request.json)
    if contains_list(route_list):
        output = dict()
        # get ratings, scores and voice alerts for each route
        output["ratings"] = []
        output["scores"] = []
        output["navigation_ratings"]=[]
        output["voice_alerts"]=[]
        for route in route_list:
            route_ratings = []
            route_scores = []
            route_nav_ratings = []
            voice_alerts = []
            for point in route:
                vals = classify(point)
                route_ratings.append(vals[0])
                route_nav_ratings.append(nav_ratings_dict[vals[0]])
                route_scores.append(vals[1])
                voice_alerts.append(vals[2])
            output["ratings"].append(route_ratings)
            output["navigation_ratings"].append(route_nav_ratings)
            output["voice_alerts"].append(voice_alerts)
            mean_score = round(sum(route_scores)/len(route_scores))
            output["scores"].append(mean_score)
    else:
        return jsonify({'error': 'invalid request format'}) 
    
    return jsonify(output)
def parse_args(request_dict):
    """Parse model features from incoming requests formatted in    
    JSON."""
    # Initialize missing_data as False.
    
    data = request_dict.get("data", None)
    
    return ast.literal_eval(data)

def contains_list(input_list):
    return any(isinstance(el, list) for el in input_list)

# load data
key = os.environ.get('MONGOPASS')
uri = 'mongodb+srv://admin:{}@saferouter-ydztv.mongodb.net/test?retryWrites=true&w=majority'
mongo = pymongo.MongoClient(uri.format(key), maxPoolSize=50, connect=False)

db = pymongo.database.Database(mongo, 'saferouterdb')
col = pymongo.collection.Collection(db, 'safety-info')

data = []
for row in col.find({},{"_id": 0,"rating":1,"score":1,"info":1,"longitude":1,"latitude":1}):
    data.append(row)
df = pd.DataFrame(data)

# get ratings, scores and voice alerts for a location
coords = df[["longitude","latitude"]].to_numpy()
ratings = df["rating"]
scores = df["score"]
voice_info = df["info"]

def classify(point,data=coords,labels=ratings):
    diff = np.hypot(*(data - point).T)
    index =  np.argmin(diff)
    return (int(labels[index]), scores[index], voice_info[index])

nav_ratings_dict = {1:"low", 2:"moderate", 3:"severe"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4100, debug=True)



