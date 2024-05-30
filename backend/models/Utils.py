import json
import time
from datetime import datetime

lower_weights = [0,1,2,5,9,13,17]
lower_w = 0.01
def_threshold = 0.04

def cord_to_string(hand_recon_data):
    return json.dumps(cord_to_json(hand_recon_data))

def cord_to_json(hand_recon_data):
    json_obj = []
    
    for point in hand_recon_data[0]:
        json_obj.append(point.__dict__)
    
    return json_obj

def validate_maps(current_map, saved_map, sign_threshold = def_threshold):
    pos_ok = []
    for i, v in enumerate(current_map):
        diff_x = abs(current_map[i]['x'] - saved_map[i]['x'])
        diff_y = abs(current_map[i]['y'] - saved_map[i]['y'])
        diff_z = abs(current_map[i]['z'] - saved_map[i]['z'])

        pos_ok.append(diff_x < sign_threshold and diff_y < sign_threshold and diff_z < sign_threshold)

    for p in pos_ok:
        if not p:
            return False

    return True    

def calc_deltas(current_map, saved_map):
    f_delta = 0
    for i, v in enumerate(current_map):
        diff_x = abs(current_map[i]['x'] - saved_map[i]['x'])
        diff_y = abs(current_map[i]['y'] - saved_map[i]['y'])
        diff_z = abs(current_map[i]['z'] - saved_map[i]['z'])

        d = (diff_x + diff_y + diff_z) / 3
        if i in lower_weights:
            d *= lower_w
        f_delta += d

    return f_delta / (len(current_map)-(len(lower_weights)*lower_w))

def convert_delta(d):
    # if there aren't hands inside of the image, the delta value is 0.04
    return 100-((d*100)/(def_threshold*100)*100)

def current_time_ms():
    return round(time.time() * 1000)

def get_formatted_date():
    now = datetime.now()
    return now.strftime("%d/%b/%Y %H:%M:%S")
