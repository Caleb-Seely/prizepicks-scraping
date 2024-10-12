import os
import web_scraper
import my_parser

def save_wp_data(wp, fn):
    '''
    Function to take data from PrizePicks API and save it as a file.
    It takes 2 arguments:
        wp - wbpage data to be saved
        fn - name of file to save the webpage data at
    '''
    with open(fn, 'w') as file:
        file.write(wp)
    print(f"Wrote WP to: {fn}")

def get_wp_example(fn = "example_wp.html", local = True, ow = False, league = "NFL"):
    '''
    Function to load in example file for development use or request a new one from the prizepicks API.
    
    3 parameters are passed in:
        fn - file name as a string of the file that is to be used
        local - bool which dictates whether an existing local file should be used or not
        ow - bool which tells whether to overwrite any existing files which may have the same name as what was passed in

    This function default to picking "NFL" data, but that can be changed to any of a number of the following abbreviations
    which are recognized by the scraper and PrizePicks database: "NFL", "CFB", "MLB", "WNBA", "Soccer", "CFB2H".
    '''
    use_local = local
    ow_local = ow
    wp = None
    my_lg = league

    '''
    This line checks to see if there is an existing file that matches fn. If not, then the code will create and fill in a file with
    that name from Prizepicks API call. This will override any other flags for local or ow sent in by user.
    '''
    file_check = os.path.isfile(fn)
    
    if ow_local:
        print(f"OW Local '{fn}'...")
        wp = web_scraper.make_selenium_request(my_lg)
        save_wp_data(wp, fn)
    elif use_local:
        print(f"Reading from local file '{fn}'")
        if (file_check is False) or (os.stat(fn).st_size == 0):
            '''---If local file does not exist or is empty, then create and fill one with that name---'''
            print(f"File '{fn} does not exist or is empty. Attempting re-write...")
            wp = web_scraper.make_selenium_request(my_lg)
            save_wp_data(wp, fn)
        else:
            print(f"Reading from:{fn}")
            with open(fn, 'r') as file:
                wp = file.read()
            print("Read complete!")
    else:
        print("Parsing data from internet request...")
        wp = web_scraper.make_selenium_request(my_lg)
    
    return wp


if __name__ == "__main__":
    '''
    Eventually, this will be the code that is the manager for the scraper that keep running all the time
    '''
    example = "example_wp.html"
    inflight = "example_wp_inflight.html"
    wp_response = get_wp_example(example, local = True, ow = False)
    my_var = my_parser.parse_webpage(wp_response)

    if my_var: print("Sucessfully parsed the response without crashing!!")
