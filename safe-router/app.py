#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
import ast
from getRoute import get_route
from utils import *


app = Flask(__name__)



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
    
    points = parse_args(request.json)
    try:
        full_route_1 , full_route_2 = get_route(points[0],points[1])
        # mapbox only accepts routes with 100 or fewer points, so we simplify
        simplified_route = simplify_polyline(full_route_1)
        route_object = get_mapbox_route(simplified_route)
        # if the route with starting and points included is invalid, use only route with nodes
        if "NoMatch" in route_object.decode():
            simplified_route = simplify_polyline(full_route_2)
            route_object = get_mapbox_route(simplified_route )
    except:
        return jsonify({'error': 'no route found'}) 
    
    return route_object.decode()

def parse_args(request_dict):
    """Parse model features from incoming requests formatted in    
    JSON."""
    # Initialize missing_data as False.
    
    data = request_dict.get("data", None)
    
    return ast.literal_eval(data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)




