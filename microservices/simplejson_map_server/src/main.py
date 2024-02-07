from flask import Flask, jsonify, render_template, request, abort, make_response
import socket
import json


app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(
        status = "UP"
    )  

@app.route("/")
def details():
    """
    Check address of current host and IP.
    """
    hostname, ip = fetchDetails()
    return render_template('index.html', hostname=hostname, IP =ip)


@app.post("/map/")
def buildAssignments():
    """
    Return the assignment to helyOS which will be forwarded to the selected agent.
    """
    params = request.get_json() 
    yard_id = params['context'].get('id', {})
    origin = params['context'].get('origin', {})
    previous_service_results = params['context'].get('dependencies', [])

    try:
        # Get the user app mission request data.
        request_data = params['request']
        print(request_data)
        # Get information of the agent specified in the mission request data.
        map_file_path = f"/app/data/{request_data.get('map_name', 'default')}.json"
        with open(map_file_path) as fp:
            map_data = json.load(fp)
            new_data_format =  map_data.get('dataFormat', map_data.get('data_format', None))
            new_origin = map_data.get('origin', None)
            new_map_objects = map_data.get('mapObjects', map_data.get('map_objects', None))
            
            if new_origin:
                new_origin = {**origin, **new_origin}
            status = "completed"

        statusCode = 200
        
    except Exception as error:
        results = str(error)
        print( results)
        status = "failed"
        statusCode = 400
        abort(400, results)

    update = {'id': yard_id}
    if new_origin: update['origin'] = new_origin
    if new_data_format: update['data_format'] = new_data_format
    if new_map_objects: update['map_objects'] = new_map_objects

    return  jsonify ({  'status': status,
                        'result':  {'update': update}
                    }
            ), statusCode





# Function to fetch hostname and ip
def fetchDetails():
    """
    get host ip
    """
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return str(hostname), str(ip)     


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9300, debug=True)