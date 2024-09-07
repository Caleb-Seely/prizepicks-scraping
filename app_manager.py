from selenium import webdriver
import os
from bs4 import BeautifulSoup
import prizepicks_db


#Not used but may come back to try and make this work in the future
def make_httpx_request( league = None ):
    '''
    league = string which is an acronym in league_dict which the caller can pick from to get all the prizepicks bets available
   
    Function which will make request to prizepicks API for bets for the passed in league described below:
    First, it validates that league passed into it is one of the known valid ones. If not, will return 1. If no values is passed in, this will default to NFL.
    Second, it makes the request to prizepicks api.
    Third, if request was unsuccessful for whatever reason, then basic troubleshooting will be done.
    Fourth, request will be returned to caller (even if request was ultimatley unsuccessful).
    '''

    '''using as placeholders for api call'''
    page_num = 20
    single_stat = "true"
    game_mode = "pickem"

    '''---Validate input---'''

    league = validate_league(league)
    if league is None:
        '''---League not recognized, try again---'''
        return (1)
    
    '''---Make request to prizepicks api---'''
    my_header = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding" : "gzip, deflate, br, zstd",
        "Accept-language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority" : "u=0, i",
        "Sec-Ch-Ua": "Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "naviagte",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1" ,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Connection": "close"
       }
    
    prizepicks_url = "https://app.prizepicks.com/"
    api_call =  f"https://api.prizepicks.com/projections?league_id={league}&per_page={page_num}&single_stat={single_stat}&game_mode={game_mode}"
        
    print(f"--------Calling: {api_call}----------")
    my_request = httpx.get(prizepicks_url, headers=my_header)
    print(my_request.text)
    print("\n-----------------\n")
    print(my_request.request.headers)
    
    if my_request.status_code == 200:
        print("We did it!")
    else:
        print("Still bad")

    return my_request

def make_selenium_request (league = None):
    '''
    Function to make a call to get lines/spreads from prizepicks
    '''
    league = validate_league(league)
    if league is None:
        return(1)

    '''using as placeholders for api call'''
    page_num = 20
    single_stat = "true"
    game_mode = "pickem"
    api_call =  f"https://api.prizepicks.com/projections?league_id={league}&per_page={page_num}&single_stat={single_stat}&game_mode={game_mode}"
    #can I make this headless or go faster at least?
    ops = webdriver.ChromeOptions()
    #ops.add_argument("--headless=new")
    session = webdriver.Chrome("C:\\Users\\elius\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe", options=ops) #fix this to add it to my path so I don't have to keep this so ugly
    session.get(api_call)
    source = session.page_source
    session.quit()
    soup = BeautifulSoup(source, 'html.parser')
    my_info = soup.find('pre').text
    return (my_info)

def validate_league(league):
    '''
    Function to return league number if known. If league is not known, then returns None. If league is None,
    then default it to return 9.
    '''
    if league is None:
        return (9)

    known_leagues = {
        "NFL":9,
        "CFB":15,
        "MLB":2,
        "WNBA":3,
        "Soccer":82
    }
    return known_leagues.get(league)
    
def validate_data(wp = None):
    input("validate_data function is not complete. Continue anyway?")
    if wp is None:
        with open('denied.html', 'r') as input:
            wp = input.read()
    print(wp)

def save_wp_data(wp, fn):
    if wp == 1:
        print("Issue with default params, nothing written")
    else:
        with open(fn, 'w') as file:
            file.write(wp)
        print(f"Wrote WP to: {fn}")

if __name__ == "__main__":
    '''
    Eventually, this will be the code that is the manager for the scraper that keep running all the time
    '''
    fn = "example_wp.json"
    use_local = True
    ow_local = False
    file_check = os.path.isfile(fn)
    wp = None

    if ow_local:
        print("OW Local...")
        wp = make_selenium_request()
        save_wp_data(wp, fn)

    elif use_local:
        print("Reading from local html file...")
        if (file_check is False) or (os.stat(fn).st_size == 0):
            print("File does not exist or is empty. Attempting re-write...")
            wp = make_selenium_request()
            save_wp_data(wp, fn)
        else:
            print(f"Reading from:{fn}")
            with open(fn, 'r') as file:
                wp = file.read()
            print("Read complete!")

    else:
        print("Parsing data from internet request...")
        wp = make_selenium_request()

    prizepicks_db.to_db(wp)

    exit()