import mysql.connector
import json

def to_db(data):
    '''
    data - json from the internet with all the prizepicks data for a given league

    This function will be responsible for taking all the data from the json passed into it
    and adding it into a prizepicks_history mysql database.
    '''
    my_data = json.loads(data)


    master_dict = dict()
    for each in my_data['included']:
        my_type = each.get("type")
        if my_type not in master_dict:
            master_dict[my_type] = set(each.keys())
        if each.get("attributes") is not None:
            master_dict[my_type] = master_dict[my_type] | set(each.get("attributes").keys())

    for table in master_dict:
        print(table)
        for col in master_dict[table]:
            if col == "attributes": continue
            print(f"\t{col}")

    exit()

    print("-------------------")
    for each in includes: print(each)

    input("-------Done--------")


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

    sql = create_db_connection()


#Long term, this should not need to be root user
def root_login():

    creds = {'hn': 'localhost', 'un':'root'}
    with open("C:\\Users\\elius\\OneDrive\\Documents\\Untouchable\\passwords.txt") as f:
        creds['pw'] = f.readlines()[0]
    return creds


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