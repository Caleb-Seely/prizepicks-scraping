import mysql.connector
import helper

#Long term, this should not need to be root user
def root_login():
    '''
    This function is used to retrive the username, host name, and password to gain access to the local
    mySQL database. requires that the user have a file called 'secrets.txt' where 3 of the lines in it are:
    mysql_un=username
    mysql_pw=password
    mysql_hn=hostname
    
    So, to access this, that file must be setup beforehand and then this function will work properly as it
    is simply reading those 3 items from the file. It muse have *accurate* user info of the 3
    fields above to get into the SQL DB
    '''

    my_dict = helper.get_secret("mysql")
    
    '''---Checking to make sure all the necessary parts were read from file---'''
    not_found_list = []
    if my_dict.get('un') is None: not_found_list.append('un')
    if my_dict.get('pw') is None: not_found_list.append('pw')
    if my_dict.get('hn') is None: not_found_list.append('hn')
    if len(not_found_list) > 0:
        print(f"WARNING: Missing values in dict:{not_found_list}")
        return None

    return my_dict

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

def _print_all_fields(my_data, search):
    '''
    Function to print all fields in the prize picks json tag
    '''
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
