from bs4 import BeautifulSoup
import json

def parse_webpage(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')
    json_data = json.loads(soup.find('pre').text)
    for item in json_data['data']:
        my_data = parse_data(item)
    
def parse_data(data_item):
    my_dict = {
        "type": None,
        "id": None,
        "adjusted_odds": None,
        "board_time": None,
        "description": None,
        "end_time": None,
        "flash_sale_line_score": None,
        "game_id": None,
        "hr_20": None,
        "in_game": None,
        "is_live": None,
        "is_promo": None,
        "line_score": None,
        "odds_type": None,
        "projection_type": None,
        "rank": None,
        "refundable": None,
        "start_time": None,
        "stat_type": None,
        "status": None,
        "tv_channel": None,
        "updated_at": None,
        "duration": None,
        "league": None,
        "new_player": None,
        "projection_type_num": None,
        "score": None,
        "stat_type_num": None
    }

    relationship_dicts = [
        "league",
        "new_player",
        "stat_type_num"
    ]

    relationship_data = [
        "duration",
        "score"
    ]

    not_found = {
        "type": None,
        "id": None,
        "adjusted_odds": None,
        "board_time": None,
        "description": None,
        "end_time": None,
        "flash_sale_line_score": None,
        "game_id": None,
        "hr_20": None,
        "in_game": None,
        "is_live": None,
        "is_promo": None,
        "line_score": None,
        "odds_type": None,
        "projection_type": None,
        "rank": None,
        "refundable": None,
        "start_time": None,
        "stat_type": None,
        "status": None,
        "tv_channel": None,
        "updated_at": None,
        "duration": None,
        "league": None,
        "new_player": None,
        "projection_type_num": None,
        "score": None,
        "stat_type_num": None
    }

    '''---Loading data from the json tag into a dict to send to mySQL---'''
    my_dict['type'] = data_item['type']
    my_dict['id'] = data_item['id']

    del not_found['type']
    del not_found['id']

    '''---Parsing attributes dict---'''
    for attr, val in data_item['attributes']:
        if attr in my_dict:
            my_dict[attr] = val
            del not_found[attr]

    '''---Parsing relationships dict and sub-dicts---'''
    for sub_dict in relationship_dicts:
        my_dict[sub_dict] = data_item['relationships'][sub_dict]['data'].get('id')
        del not_found[sub_dict]

    for sub_dict in relationship_data:
        my_dict[sub_dict] = data_item['relationships'][sub_dict].get('data')
        del not_found[sub_dict]

    '''---This one is an excpetion because the naming is not the same between prizepicks and my db, so need to hard-code this one---'''
    my_dict["projection_type_num"] = data_item['relationships']["projection_type"]['data'].get('id')
    del not_found['projection_type_num']


    print("Could not find data for the following:")
    for k in not_found: print(f"{k},")

    return my_dict