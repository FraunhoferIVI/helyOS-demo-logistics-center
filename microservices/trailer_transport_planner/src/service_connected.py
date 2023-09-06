import math
from flask import Flask, jsonify,  request
import requests

app = Flask(__name__)


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


@app.post("/plan_job/")
def getPath():
    """
    Return the trajectory to helyOS which can be assigned to helyos_agent_slim_simulator.
    """
    # request body
    request_body = request.get_json() 
    request_data = request_body['request']
    context = request_body['context']

    step = context['orchestration']['current_step']

    tool_id = request_data['tool_id']


    if step == "prepare_mission":
        # Get truck data
        helyos_tools = context['tools'] # contains all data about the agent (tool)
        truck = next((tool for tool in helyos_tools if tool['id'] == str(tool_id)), None) # find agent in context
        truck_position = truck['pose']    

        # Get trailer
        trailer_uuid = request_data['trailer_uuid']
        helyos_tools = context['tools'] # contains all data about the agent (tool)
        trailer = next((tool for tool in helyos_tools if tool['uuid'] == str(trailer_uuid)), None) # find agent in context
        trailer_position = trailer['pose']

        # Set path planner request
        destination = trailer_position
        new_request_data = {'tool_id': tool_id, 'destination': destination}

        response =  { 'status': "completed",
                      'results': [],
                      'initial_truck_position': truck_position,
                      'initial_trailer_position': trailer_position,
                      'orchestration': {'nex_step_request':{"drive_to_trailer": new_request_data }}
            }
    


    if step == "connect_prep_move":
        # Get data from preivous services 
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')
        drive_to_trailer_step = findStep(dependencies, 'drive_to_trailer')

        # Add new assignments to previous one
        assignment_connect_to_trailer = {'tool_id': tool_id, 'assignment': assignment_connect_to_trailer}
        results = prepare_mission_step['results'] + drive_to_trailer_step['results']
        results.append(assignment_connect_to_trailer)

        # Set path planner request
        start_position = prepare_mission_step['initial_trailer_position']
        destination = prepare_mission_step['initial_truck_position']
        new_request_data = {'tool_id': tool_id, 'initial_position': start_position, 'destination': destination}

        response =   {'status' : "completed", 
                      'results' : results,
                      'orchestration': {'nex_step_request':{"drive_trailer_to_destiny": new_request_data }} }
    

    if step == "return_trailer":
        # Get data from preivous services 
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')
        connect_prep_move_step = findStep(dependencies, 'connect_prep_move')
        drive_trailer_to_destiny_step = findStep(dependencies, 'drive_trailer_to_destiny')

        # Add new assignments to previous one
        results = connect_prep_move_step['results'] +  drive_trailer_to_destiny_step['results']

        # Set path planner request
        start_position = prepare_mission_step['initial_truck_position']
        destination = prepare_mission_step['initial_trailer_position']
        new_request_data = {'tool_id': tool_id, 'initial_position': start_position, 'destination': destination}

        response =   {'status' : "completed", 
                      'results' : results,
                      'orchestration': {'nex_step_request':{"drive_trailer_to_origin": new_request_data }} }
        

    if step == "disconnect_return_truck":
        # Get data from preivous services 
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')
        return_trailer_step = findStep(dependencies, 'return_trailer')
        drive_trailer_to_origin_step = findStep(dependencies, 'drive_trailer_to_origin')

        # Add new assignments to previous one
        assignment_disconnect_to_trailer = {'operation': f"disconnect_trailer"}
        results = return_trailer_step['results'] + drive_trailer_to_origin_step['results']
        results.append(assignment_disconnect_to_trailer)

        # Set path planner request
        start_position = prepare_mission_step['initial_trailer_position']
        destination = prepare_mission_step['initial_truck_position']
        new_request_data = {'tool_id': tool_id, 'initial_position': start_position, 'destination': destination}

        response =   {'status' : "completed", 
                      'results' : results,
                      'orchestration': {'nex_step_request':{"drive_to_origin": new_request_data }} }



    if step == "combine_assignments":
        dependencies = context['dependencies']
        prepare_mission_step = findStep(dependencies, 'prepare_mission')
        disconnect_return_truck_step = findStep(dependencies, 'disconnect_return_truck')
        drive_to_origin_step = findStep(dependencies, 'drive_to_origin')

        # Add new assignments to previous one
        results = disconnect_return_truck_step['results'] + drive_to_origin_step['results']

        response =   { "status": "completed", "results": results, 'dispatch_order':[[0],[1],[2],[3],[4],[5]] }
    
    return jsonify(response)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9100, debug=True)