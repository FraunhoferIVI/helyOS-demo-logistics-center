

def convert_to_trucktrix_format(trajectory):
    """ convert trajectory object to autotruck-trucktrix
        trajectory: [{"x": float, "y": float, "orientations":List[float], time:float}, ...] 
    
    """
    autotruck_path = {}
    autotruck_path['payload'] = {}
    autotruck_path['payload']['tasks'] = [{}]
    autotruck_path['payload']['tasks'][0]['payload'] = {}
    autotruck_path['payload']['tasks'][0]['payload']['operations'] = [{}]
    autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload'] = {} 
    autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload'] = {}
    autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'] = []

    for i in range(0,len(trajectory)):
        autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'].append({})
        autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step'] = {}
        autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'] = [{}]
        autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'][0]['vehicle'] = {}
        autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'][0]['vehicle']['position'] = [trajectory[i]['x'], trajectory[i]['y']]
        autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'][0]['vehicle']['orientation'] = trajectory[i]['orientations'][0]

        if len(trajectory[i]['orientations']) == 2:
             autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'].append({})
             autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'][1]['vehicle'] = {}
             autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'][1]['vehicle']['position'] = [trajectory[i]['x'], trajectory[i]['y']]
             autotruck_path['payload']['tasks'][0]['payload']['operations'][0]['payload']['data_payload']['steps'][i]['step']['vehicles'][1]['vehicle']['orientation'] = trajectory[i]['orientations'][1]

    return autotruck_path

