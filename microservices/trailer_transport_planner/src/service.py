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
    path_planner_url = service_config['path_planner_url']
    path_planner_apikey = service_config['path_planner_apikey']

    tool_id = request_data['tool_id']


    if step == "get_trailer":
        # Get truck data
        helyos_tools = context['tools'] # contains all data about the agent (tool)
        truck = next((tool for tool in helyos_tools if tool['id'] == str(tool_id)), None) # find agent in context
        truck_position = truck['pose']    

        # Get trailer
        trailer_uuid = request_data['trailer_uuid']
        helyos_tools = context['tools'] # contains all data about the agent (tool)
        trailer = next((tool for tool in helyos_tools if tool['uuid'] == str(trailer_uuid)), None) # find agent in context
        trailer_position = trailer['pose']

        destination = trailer_position
        new_request_data = {'request':{'tool_id': tool_id, 'destination': destination}, 'context': context}
        path_planner_response = call_path_planner(path_planner_url, new_request_data , path_planner_apikey)

        assignment_drive_to_trailer = path_planner_response['results'][0]['assignment']
        assignment_connect_to_trailer = f"connect_trailer {trailer_uuid}"
        results = []
        results.append({'tool_id': tool_id, 'assignment': assignment_drive_to_trailer})
        results.append({'tool_id': tool_id, 'assignment': assignment_connect_to_trailer})

        response =   {
                "results":results,
                "initial_truck_position": truck_position,
                "initial_trailer_position": trailer_position
            }
    

    if step == "bring_trailer":
        dependencies = context['dependencies']
        get_trailer_step = findStep(dependencies, 'get_trailer')

        start_position = get_trailer_step['initial_trailer_position']
        destination = get_trailer_step['initial_truck_position']
        new_request_data = {'request':{'tool_id': tool_id, 'initial_position': start_position, 'destination': destination}, 'context': context}
        path_planner_response = call_path_planner(path_planner_url, new_request_data, path_planner_apikey)

        # Add new assignment to previous one
        assignment_drive_with_trailer = path_planner_response['results'][0]['assignment']
        results = get_trailer_step['results']
        results.append({'tool_id': tool_id, 'assignment': assignment_drive_with_trailer})

        response =   { "results": results }
    
    if step == "return_trailer":
        dependencies = context['dependencies']
        get_trailer_step = findStep(dependencies, 'get_trailer')
        bring_trailer_step = findStep(dependencies, 'bring_trailer')

        start_position = get_trailer_step['initial_truck_position']
        destination = get_trailer_step['initial_trailer_position']
        new_request_data = {'request':{'tool_id': tool_id, 'initial_position': start_position, 'destination': destination}, 'context': context}
        path_planner_response = call_path_planner(path_planner_url, new_request_data, path_planner_apikey)

        # Add new assignment to previous one
        assignment_drive_back_trailer = path_planner_response['results'][0]['assignment']
        results = bring_trailer_step['results']
        results.append({'tool_id': tool_id, 'assignment': assignment_drive_back_trailer})

        response =   { "results": results }


    if step == "return_truck":
        dependencies = context['dependencies']
        get_trailer_step = findStep(dependencies, 'get_trailer')
        return_trailer_step = findStep(dependencies, 'return_trailer')

        start_position = get_trailer_step['initial_trailer_position']
        destination = get_trailer_step['initial_truck_position']
        new_request_data = {'request':{'tool_id': tool_id, 'initial_position': start_position, 'destination': destination}, 'context': context}
        path_planner_response = call_path_planner(path_planner_url, new_request_data , path_planner_apikey)

        # Add new assignment to previous one
        assignment_drive_back_truck = path_planner_response['results'][0]['assignment']
        assignment_disconnect_to_trailer = f"disconnect_trailer"
        results = return_trailer_step['results']
        results.append({'tool_id': tool_id, 'assignment': assignment_drive_back_truck})
        results.append({'tool_id': tool_id, 'assignment': assignment_disconnect_to_trailer})

        response =   { "status": "completed", "results": results, 'dispatch_order':[[0],[1],[2],[3],[4],[5]] }
    
    return jsonify(response)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9100, debug=True)