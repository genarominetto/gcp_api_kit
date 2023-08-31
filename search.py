from googleapiclient.discovery import build
from gcp_api_connector.resources.googleapis_auth import get_api_key
APIKEY = get_api_key()

#Custom Search API
def search(query, num_results=2):
    cservice = build('customsearch', 'v1', developerKey=APIKEY)
    results = cservice.cse().list( q=query, cr = 'countryUS', cx='017576662512468239146:omuauf_lfve', num=num_results).execute()
    return results['items']
