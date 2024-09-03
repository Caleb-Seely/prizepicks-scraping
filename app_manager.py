import requests
import random
import httpx
from time import sleep

def make_request( league = None ):
    '''
    league = string which is an acronym in league_dict which the caller can pick from to get all the prizepicks bets available
   
    Function which will make request to prizepicks API for bets for the passed in league described below:
    First, it validates that league passed into it is one of the known valid ones. If not, will return 1. If no values is passed in, this will default to NFL.
    Second, it makes the request to prizepicks api.
    Third, if request was unsuccessful for whatever reason, then basic troubleshooting will be done.
    Fourth, request will be returned to caller (even if request was ultimatley unsuccessful).
    '''

    '''---Setting up variables---'''
    league_dict = {
        "NFL":9,
        "CFB":15,
        "MLB":2,
        "WNBA":3,
        "Soccer":82
    }
    '''using as placeholders for api call'''
    page_num = 20
    single_stat = "true"
    game_mode = "pickem"

    '''---Validate input---'''
    if league is None:
        league = 9
    elif league in league_dict:
        league = league_dict[league]
    else:
        '''League not recognized, try again'''
        return (1)
    
    '''---Make request to prizepicks api---'''
    my_header = {
        "Accept" : "application/json",
        "Accept-Encoding" : "gzip, deflate, br, zstd",
        "Accept-language": "en-US,en;q=0.9,it;q=0.8,es;q=0.7",
        "Content-Type" : "application/json",
        "Origin" : "https://app.prizepicks.com",
        "Priority" : "u=0, i",
        "Referer" : "https://app.prizepicks.com/",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
       }
    
    api_call =  f"https://api.prizepicks.com/projections?league_id={league}&per_page={page_num}&single_stat={single_stat}&game_mode={game_mode}"
    print(f"Calling: {api_call}")
    with httpx.Client( http2=True, headers=my_header, cookies={"language":"en", }) as session:
        r = session.get(api_call)
        print(r.text)
        print()
        if r.status_code == 200:
            print("We did it!")
        else:
            print("Still bad")
    return r


def parse_wp(wp):
    pass


if __name__ == "__main__":
    '''
    Eventually, this will be the code that is the manager for the scraper that keep running all the time
    '''
    r = make_request()
    exit()