import math
from flask import Flask, jsonify,  request

app = Flask(__name__)

TRAILER_CONNECTION_DISTANCE = 3550
TRAILER_CONNECTION_GATE_DISTANCE = 3550
TRAILER_CONNECTION_DROP_DISTANCE = 8000

@app.route("/health")
def health():
    return jsonify(
        status = "UP"
    )  


@app.post("/plan_job/")
def main():
    """
    This service is employed in 2 of 3 used in the pick and drop missions:
    1. prepare_mission: Pased input data and filter context. (performed by this service)
    2. drive_the_path: The truck drives to the target. (path is planned by another service)
    3. connect_trailer or disconnect_trailer: The truck connects or disconnects the trailer. (performed by this service)

    For park missions, only the first and the second steps are used.

    """
    # Input data
    request_body = request.get_json() 
    request_data = request_body['request']
    context = request_body['context']
    step = context['orchestration']['current_step']
    
    agent_id = request_data['agent_id']
    operation = request_data['operation']
    trailer_uuid = request_data.get('trailer_uuid', None)
    target_name = request_data.get('target_name', None)

    # Error handling
    if operation == "pick" and trailer_uuid is None and target_name is None:
        raise ValueError('Either trailer_uuid or target_name must be provided')
    
    if operation == "drop" and target_name is None:
        raise ValueError('target_name must be provided')

    if operation == "park" and target_name is None:
        raise ValueError('target_name must be provided')

    
# STEP 1
    if step == "prepare_mission":
        # Get truck data from context
        helyos_agents = context['agents'] # contains all data about the agent
        truck = next((tool for tool in helyos_agents if tool['id'] == str(agent_id)), None) # find agent in context
        truck_position = {**truck['pose']} 
        
        if operation == "pick":          
            if trailer_uuid is None:
                target_name = request_data['target_name']
                trailer, distance = get_neareset_trailer(target_name, context)
                trailer_uuid = trailer['uuid']
            else:
                helyos_agents = context['agents'] # contains all data about the agent (tool)
                trailer = next((tool for tool in helyos_agents if tool['uuid'] == str(trailer_uuid)), None) # find agent in context

            # Get trailer data from context         
            trailer_position = trailer['pose']

            # Set path planner request data to drive to trailer
            destination = {**trailer_position}
            destination['x'] = destination['x'] + TRAILER_CONNECTION_DISTANCE*math.cos(destination['orientations'][0]/1000)
            destination['y'] = destination['y'] + TRAILER_CONNECTION_DISTANCE*math.sin(destination['orientations'][0]/1000)
            new_request_data = {'agent_id': agent_id, **destination}

            response =  { 'status': "ready",
                        'results': [],
                        'trailer_uuid': trailer_uuid,
                        'initial_truck_position': truck_position,
                        'initial_trailer_position': trailer_position,
                        'orchestration': {'next_step_request':{"drive_the_path": new_request_data }}
                }
    


        if operation == "drop" or operation == "park":          
            # Get target data from context
            map_objects = context['map'].get('map_objects', []) 
            target = next((t for t in map_objects if t['name'] == target_name), None)
            trailer_uuid = None    
            
            # Set path planner request data to drive to target
            positon_offset = TRAILER_CONNECTION_DROP_DISTANCE if operation == "drop" else TRAILER_CONNECTION_DISTANCE
            destination = {}
            destination['x'] = target['metadata']['x'] + positon_offset*math.cos(target['metadata']['orientations'][0]/1000)
            destination['y'] = target['metadata']['y'] + positon_offset*math.sin(target['metadata']['orientations'][0]/1000)
            destination['orientations'] = target['metadata']['orientations']
            new_request_data = {'agent_id': agent_id, **destination}

            response =  { 'status': "ready",
                        'results': [],
                        'trailer_uuid': trailer_uuid,
                        'orchestration': {'next_step_request':{"drive_the_path": new_request_data }}
                }
            
        
# STEP 2
#   It is not perfomred here. A path planner service is called by helyos core to plan the path to the target. 
#   The request data is set by the orchestration field in the response of the previous step.

# STEP 3
    if step == "connect_or_disconnect_trailer":
        # Create a second assignment to connect to the trailer
        # Get data from preivous services 
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')
        if operation == "pick":
            assignment = {'agent_id': agent_id, 'assignment':  {'operation': f"connect_trailer {prepare_mission_step['trailer_uuid']}"}}
        if operation == "drop":
            assignment = {'agent_id': agent_id, 'assignment':  {'operation': f"disconnect_trailer"}}

        response =   {'status' : "ready", 
                      'results' : [assignment]
                       }
    
    return jsonify(response)

    

def findStep(list_of_dicts, value): 
    for d in list_of_dicts:
        if 'step' in d and d['step'] == value:
            return d['response']
    return None



def  get_neareset_trailer(target_name, context):
    """
    Get the nearest trailer to the target_id
    """

    targets = context['map'].get('map_objects', [])
    target = next((t for t in targets if t['name'] == target_name), None) # find target in context

    helyos_agents = context['agents'] 
    trailers = [obj for obj in helyos_agents if (obj['agent_type'] == 'trailer' or obj['agent_type'] == 'swapbody') ] # find all trailers in context

    x = target['metadata']['x']
    y = target['metadata']['y']
    
    # make a list of distances between trailer and targets
    distances = []
    for trailer in trailers:
        trailer_x = trailer['x']
        trailer_y = trailer['y']
        distance = ((trailer_x - x)**2 + (trailer_y - y)**2)**0.5
        distances.append(distance)
    min_distance = min(distances)

    # get the trailer name with the smallest distance to the map object or select UNKNOWN trailer
    if min_distance < 50000:
        nereast_trailer = trailers[distances.index(min_distance)]  
    else:
        nereast_trailer = {'uuid':'UNKNOWN'}   

    return nereast_trailer, min_distance



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9200, debug=True)


