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
    helyos_agents = context['agents'] # contains all data about the agents 

    # Get agent identifiesr from user request data, it can be either agent_id or agent_uuid
    agent_id = request_data.get('agent_id', request_data.get('tool_id', None))
    if agent_id is None:
        agent_uuid = request_data['agent_uuid']
        agent = next((a for a in helyos_agents if a['uuid'] == str(agent_uuid)), None) # find target agent in context
        agent_id = agent['id']
    else:
        agent = next((a for a in helyos_agents if a['id'] == str(agent_id)), None) # find target agent in context
        agent_uuid = agent['uuid']

    # Get initial position either from user request or from helyOS context
    initial_position = request_data.get('initial_position', None) # start pose
    if initial_position is None:
        initial_position = agent['pose']

    # Get destination from user request data
    destination = request_data.get('destination', None) # destination pose
    if destination is None:
        destination = { 'x':request_data['x'], 'y':request_data['y'], 'orientations':request_data['orientations'], }

    # Calculate trajectory
    destination['orientations'][0] = (destination['orientations'][0]/1000)%(2*math.pi) 
    trajectory = calculate_path(initial_position, destination)

    # The autoTruck agent simulator accepts the autotruck-trucktrix data format for paths. So we need to convert to it.
    agent = next((a for a in helyos_agents if a['id'] == str(agent_id)), None) # 
    if 'trucktrix' in agent['data_format']:
        assignment = convert_to_trucktrix_format(trajectory)
    else:
        assignment = {'trajectory': trajectory, 'operation':'driving'}     
    
    # Return response
    response =     {
                    "results":[{
                                    "agent_uuid": agent_uuid,
                                    "assignment": assignment
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
        theta = clothoid0.Theta(i)%(2*math.pi)*1000
        trajectory.append ({ 'x':clothoid0.X(i), 'y':clothoid0.Y(i), 'orientations':[theta,0], 'time': None})

    return trajectory


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)