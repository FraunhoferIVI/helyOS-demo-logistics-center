import math
from flask import Flask, jsonify,  request
import requests

app = Flask(__name__)


def call_path_planner(url, data, api_key):
  headers={
    'Content-type':'application/json', 
    'Accept':'application/json',
    "Authorization": f"Bearer {api_key}"
}
  response = requests.post(f"{url}plan_job/", json=data, headers=headers)
  return response.json()


@app.route("/health")
def health():
    return jsonify(
        status = "UP"
    )  


def findStep(list_of_dicts, value): 
    for d in list_of_dicts:
        if 'step' in d and d['step'] == value:
            return d['response']
    return None

TRAILER_CONNECTION_DISTANCE = 3550

@app.post("/plan_job/")
def getPath():
    """
    Return the trajectory to helyOS which can be assigned to helyos_agent_slim_simulator.
    """
    # request body
    request_body = request.get_json() 
    request_data = request_body['request']
    context = request_body['context']
    service_config = request_body['config']

    step = context['orchestration']['current_step']

    agent_id = request_data['agent_id']


    if step == "prepare_mission":
        # Get truck data
        helyos_agents = context['agents'] # contains all data about the agent (tool)
        truck = next((tool for tool in helyos_agents if tool['id'] == str(agent_id)), None) # find agent in context
        truck_position = {**truck['pose']} 

        # Get trailer data
        trailer_uuid = request_data['trailer_uuid']
        helyos_agents = context['agents'] # contains all data about the agent (tool)
        trailer = next((tool for tool in helyos_agents if tool['uuid'] == str(trailer_uuid)), None) # find agent in context
        trailer_position = trailer['pose']

        # Set path planner request
        destination = {**trailer_position}
        destination['x'] = destination['x'] + TRAILER_CONNECTION_DISTANCE*math.cos(destination['orientations'][0]/1000)
        destination['y'] = destination['y'] + TRAILER_CONNECTION_DISTANCE*math.sin(destination['orientations'][0]/1000)
        new_request_data = {'agent_id': agent_id, **destination}

        response =  { 'status': "ready",
                      'results': [],
                      'trailer_uuid': trailer_uuid,
                      'initial_truck_position': truck_position,
                      'initial_trailer_position': trailer_position,
                      'orchestration': {'next_step_request':{"drive_to_trailer": new_request_data }}
            }
    


    if step == "connect_prep_move":
        # Get data from preivous services 
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')

        # Add new assignments to previous  mission
        assignment_connect_to_trailer = {'agent_id': agent_id, 'assignment':  {'operation': f"connect_trailer {prepare_mission_step['trailer_uuid']}"}}
        results = [assignment_connect_to_trailer]

        # Set path planner request
        start_position = prepare_mission_step['initial_trailer_position']
        destination = prepare_mission_step['initial_truck_position']
        new_request_data = {'agent_id': agent_id, 'initial_position': start_position, **destination}

        response =   {'status' : "ready", 
                      'results' : results,
                      'orchestration': {'next_step_request':{"drive_trailer_to_destiny": new_request_data }} }
    

    if step == "return_trailer":
        # Get data from preivous services 
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')

        # Add new assignments to previous  mission
        results =[]

        # Set path planner request
        start_position = prepare_mission_step['initial_truck_position']
        destination = prepare_mission_step['initial_trailer_position']
        destination['x'] = destination['x'] + TRAILER_CONNECTION_DISTANCE*math.cos(destination['orientations'][0]/1000)
        destination['y'] = destination['y'] + TRAILER_CONNECTION_DISTANCE*math.sin(destination['orientations'][0]/1000)
        new_request_data = {'agent_id': agent_id, 'initial_position': start_position, **destination}

        response =   {'status' : "ready", 
                      'results' : results,
                      'orchestration': {'next_step_request':{"drive_trailer_to_origin": new_request_data }} }
        

    if step == "disconnect_return_truck":
        # Get data from preivous services 
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')

        # Add new assignments to mission
        assignment_disconnect_to_trailer = {'agent_id': agent_id, 'assignment':  {'operation': f"disconnect_trailer"}}
        results = [assignment_disconnect_to_trailer]

        # Set path planner request
        start_position = prepare_mission_step['initial_trailer_position']
        destination = prepare_mission_step['initial_truck_position']
        new_request_data = {'agent_id': agent_id, 'initial_position': start_position, **destination}

        response =   {'status' : "ready", 
                      'results' : results,
                      'orchestration': {'next_step_request':{"drive_to_origin": new_request_data }} }



    if step == "combine_assignments":
        # Get data from preivous services 
        dependencies = context['dependencies']

        drive_to_trailer_step = findStep(dependencies, 'drive_to_trailer')
        connect_prep_move_step = findStep(dependencies, 'connect_prep_move')
        
        drive_trailer_to_destiny_step = findStep(dependencies, 'drive_trailer_to_destiny')

        drive_trailer_to_origin_step = findStep(dependencies, 'drive_trailer_to_origin')
        disconnect_return_truck_step = findStep(dependencies, 'disconnect_return_truck')

        drive_to_origin_step = findStep(dependencies, 'drive_to_origin')

        # Add new assignments to mission
        results =  drive_to_trailer_step['results'] + connect_prep_move_step['results'] + drive_trailer_to_destiny_step['results'] + \
                  drive_trailer_to_origin_step['results'] + disconnect_return_truck_step['results'] + drive_to_origin_step['results']

        response =   { "status": "ready", "results": results, 'dispatch_order':[[0],[1],[2],[3],[4],[5]] }
    
    return jsonify(response)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9100, debug=True)