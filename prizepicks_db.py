import mysql.connector
import json
import pickle

def _print_all_fields(my_data, search):

    master_dict = dict()
    for each in my_data[search]:
        my_type = each.get("type")
        if my_type not in master_dict:
            master_dict[my_type] = set(each.keys())
        if each.get("attributes") is not None:
            master_dict[my_type] = master_dict[my_type] | set(each.get("attributes").keys())
        if each.get("relationships") is not None:
            to_add = [ 'relate--'+key for key in each.get("relationships").keys()]
            master_dict[my_type] = master_dict[my_type] | set(to_add)


    print(f"\n---Data from '{search}' section---\n")
    for table in master_dict:
        print(table)
        comeback = set()
        for col in master_dict[table]:
            if col == "attributes": 
                continue
            if "--" in col: 
                comeback.add(col)
                continue
            print(f"\t{col}")
        for relationship in comeback: print(f"\t{relationship}")

def to_db(data):
    '''
    data - json from the internet with all the prizepicks data for a given league

    This function will be responsible for taking all the data from the json passed into it
    and adding it into a prizepicks_history mysql database.
    '''

    sql = create_db_connection()
    exit()
    '''
    my_data = json.loads(data)

    for each in ["data","included"]:
        _print_all_fields(my_data, each)

    exit()

    print(my_data.keys())
    print()
    for parent_key in my_data.keys():
        print(f"Parent_key = {parent_key}")
        for point in my_data[parent_key]:
            if type(point) is not dict:
                print(point)
            else:
                for key in point:
                    if type(point[key]) == dict:
                        print(f"{key} :")
                        for each in point[key].items():
                            print(f"\t{each}")
                    else:
                        print(f"{key} : {point[key]}")
            input()
            break
    '''

#Long term, this should not need to be root user
def root_login():
    '''
    This function is used to retrive the username, host name, and password to gain access to the local
    mySQL database. This assumes that the user already has a file called "local_config.pkl" which contains
    a dictionary that looks like this:
    pickled_dict = {
        "mySQL":{
            "pw": "my_password",
            "hn": "SQL_host_name",
            "un": "SQL_username"
            }
        }
    
    So, to access this, that file must be setup beforehand and then this function will work properly as it
    is simply reading those 3 items from the "mySQL" key of the dict. There may be other keys in the dict,
    but this function reads from "mySQL" and to work propoerly, should have *accurate* user info of the 3
    fields above to get into the SQL DB
    '''
    #In future, write code to take this info from a JSON file and add it to the pickled dict

    with open("local_config.pkl", "rb") as f:
        '''---Load creds in from pkl file as dict and assert that creds["mySQL"] is a dict---'''
        creds = pickle.load(f)
        assert isinstance(creds["mySQL"], dict)

    return creds["mySQL"]

def create_db_connection(db_name="prizepicks", host_name= None, user_name = None, user_password = None):
    
    if not host_name:
        creds = root_login()
        host_name = creds['hn']
        user_name = creds['un']
        user_password = creds['pw']

    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name
    )

    print("MySQL Database connection successful")
    return connection