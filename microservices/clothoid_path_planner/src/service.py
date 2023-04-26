import math
from flask import Flask, jsonify,  request
from convert_data_format import convert_to_trucktrix_format
from pyclothoids import Clothoid

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(
        status = "UP"
    )  

@app.post("/plan_job/")
def getPath():
    """
    Return the trajectory to helyOS which can be assigned to helyos_agent_slim_simulator.
    """
    # request body
    request_body = request.get_json() 
    request_data = request_body['request']
    context = request_body['context']

    # Get destination from request data
    tool_id = request_data['tool_id']
    destination = request_body.get('destination', None) # destination pose
    if destination is None:
        destination = { 'x':request_data['x'], 'y':request_data['y'], 'orientations':request_data['orientations'], }

    # Get initial position from helyOS context
    helyos_tools = context['tools'] # contains all data about the agent (tool)
    tool = next((tool for tool in helyos_tools if tool['id'] == str(tool_id)), None) # find target agent in context
    initial_position = tool['pose']

    # Calculate trajectory
    destination['orientations'][0] = (destination['orientations'][0]/1000)%(2*math.pi) 
    trajectory = calculate_path(initial_position, destination)

    # The autoTruck agent simulator accepts the autotruck-trucktrix data format for paths. So we need to convert to it.
    trucktrix_assignment = convert_to_trucktrix_format(trajectory)


    response =     {
                    "results":[{
                                    "tool_id": tool_id,
                                    "assignment": trucktrix_assignment
                                }]
                }
    

    return jsonify(response)


def calculate_path(initial_position, destination):
    """
    Use Clothoid library to create drivable path
    """
    print(initial_position, destination)
    clothoid0 = Clothoid.G1Hermite(initial_position['x'], initial_position['y'], initial_position['orientations'][0],
                                        destination['x'],       destination['y'],      destination['orientations'][0])
    
    trajectory = [];  npts = 80
    sample_points = [clothoid0.length * m/(npts-1) for m in range(0,npts)]
    for i in sample_points:
        trajectory.append ({ 'x':clothoid0.X(i), 'y':clothoid0.Y(i), 'orientations':[clothoid0.Theta(i),0]})

    return trajectory






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)