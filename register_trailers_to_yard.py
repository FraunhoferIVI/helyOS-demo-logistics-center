#!/usr/bin/env python
# coding: utf-8
# # Using HTTP requests to add/remove trailers into the yard 

import sys
import subprocess
import time
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
# # Wait helyOS to start
time.sleep(15)


# ## Connecting with helyOS
import requests,  json
hostname = "http://helyos_core:5000"
username = "admin"
password = "admin"
session = requests.Session()
session.headers.update({ "Content-Type": "application/json; charset=utf-8"})
    

def get_create_token(username, password):
    session.headers.pop('Authorization', '')
    graphql_request = {"operationName": "authenticate",
                       "query":""" mutation authenticate($postMessage:  AuthenticateInput!) {
                                       authenticate(input:$postMessage)  {  jwtToken }}
                            """,
                        "variables": {"postMessage": { "username": username, "password":password} }
                        }
    res = session.post(f"{hostname}/graphql", json=graphql_request)
    token = res.json()['data']['authenticate']['jwtToken']
    return token

authToken = get_create_token(username, password)
session.headers.update({ "Authorization": f"Bearer {authToken}"})    


## CRUDE functions

def list_agents(uuid):
    graphql_request = {"operationName": "allAgents",
                       "query":""" 
                                query allAgents($condition: AgentCondition!) {
                                          allAgents (condition: $condition){
                                            nodes {id,  uuid, geometry}
                                          }
                                        }
                                """,

                            "variables": {"condition": {"uuid": uuid} }
                        }

    res = session.post(f"{hostname}/graphql", json=graphql_request)
    return res.json()['data']['allAgents']['nodes']
    

def create_resource(uuid, name, pose, geometry, status, agentType, yardId, **other):

    tool_data = {'uuid':uuid, 'name': name, 'yardId': yardId, 'geometry': json.dumps(geometry),'status': status,
                 'agentType': agentType}
    tool_data['x']=pose['x']
    tool_data['y']=pose['y']
    tool_data['orientations']=pose['orientations']
    
    tool_data = {**tool_data, **other}
    
    graphql_request = {"operationName": "createAgent",
                           "query":""" 
                                    mutation createAgent($postMessage: CreateAgentInput!){
                                        createAgent(input:$postMessage) { agent{id} }
                                    }""",

                            "variables": {"postMessage": {"agent": tool_data} }
                            }    
    
    res = session.post(f"{hostname}/graphql", json=graphql_request)
    print(res.json())
    if res.status_code != 200:
        print(res.status_code)
        
        
def update_resource(uuid, name, pose, geometry, status, agentType, yardId, **other):
    tool_data = dict()
    if pose: 
        tool_data['x']=pose['x']
        tool_data['y']=pose['y']
        tool_data['orientations']=pose['orientations']
                            
    if name: tool_data['name'] = name
    if yardId: tool_data['yardId'] = yardId
    if geometry: tool_data['geometry'] = json.dumps(geometry)
    if status: tool_data['status'] = status
    if agentType: tool_data['agentType'] = agentType
    tool_data = {**tool_data, **other}
    
    graphql_request = {"operationName": "updateAgentByUuid",
                           "query":""" 
                                    mutation updateAgentByUuid($postMessage: UpdateAgentByUuidInput!){
                                        updateAgentByUuid(input:$postMessage) { agent{id} }
                                    }""",

                            "variables": {"postMessage": { "uuid": uuid, "toolPatch": tool_data} }
                            }    
    
    res = session.post(f"{hostname}/graphql", json=graphql_request)
    if res.status_code != 200:
        print(res.status_code)
        

def create_or_update_resource(uuid, *arg, **others):
    res = list_agents(uuid)
    if len(res):
        print('update', uuid)
        return update_resource(uuid, *arg, **others)
    else:
        print('create', uuid)
        return create_resource(uuid,  *arg, **others)
    


 ## Creating or Reseting trailers

yardId = 1
with open('geometry_trailer.json', 'r') as f:
    trailer_geometry = json.load(f)

try_again = True
while try_again:
    try:
        create_or_update_resource("trailer1",  "trailer1", {'x':-26833,'y':500, 'orientations':[2876]}, 
                                trailer_geometry, "free","trailer", yardId,
                                factsheet= json.dumps({'current_gate': "G21"}),
                                acknowledgeReservation=False, agentClass='tool')


        create_or_update_resource("trailer2",  "trailer2", {'x':-28490,'y':-6266, 'orientations':[2876]}, 
                                trailer_geometry, "free", "trailer", yardId,
                                factsheet= json.dumps({'current_gate': "G22"}),
                                acknowledgeReservation=False, agentClass='tool')
                                

        create_or_update_resource("trailer3",  "trailer3", {'x':-29884,'y':-9967, 'orientations':[2876]}, 
                                trailer_geometry, "free", "trailer", yardId,
                                factsheet= json.dumps({'current_gate': "G23"}),
                                acknowledgeReservation=False, agentClass='tool')


        create_or_update_resource("trailer4",  "trailer4", {'x':-30323,'y':-13940, 'orientations':[2876]}, 
                                trailer_geometry, "free", "trailer", yardId,
                                factsheet= json.dumps({'current_gate': "G24"}),
                                acknowledgeReservation=False, agentClass='tool')
        try_again = False
    except:
        print('try again...')
        time.sleep(2)
        continue                          
                          

