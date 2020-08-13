import smtplib
import ssl
import sys
from contextlib import closing

from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException


def search(args):
    
    if len(args) > 1:        
        index = 1 # first argument is always the name of the application
        while index < len(args):
            print("Results for '{}':".format(args[index]))
            scrape(args[index])
            index += 1
    else:
        return "No search terms given"

def scrape(term):
    url = 'https://www.auctionmaxx.com/Browse?FullTextQuery={}'.format(term)

    # get the content
    html = BeautifulSoup(simple_get(url), 'html.parser')
    
    # look for a div with class "noresults" and return if found
    if len(html.find_all("div", {"class":"noresults"})) != 0:        
        return "No results found"

    # get the results
    titles = html.find_all("h4")
    results = []
    i = 2 # the first 2 <h4> tags aren't things we want to deal with
    while i < len(titles):
        results.append(titles[i].text)
        i += 1
    
    return results

def simple_get(url):
    """
    Gets the content of a web page at "url"
    If it's HTML or XML, it will be parsed, otherwise None is returned
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    Just prints the damn errors
    """
    print(e)

# search for the terms
print(search(sys.argv))
# compare to the last search to see if anything new came up?
# send an email or some other notification?
