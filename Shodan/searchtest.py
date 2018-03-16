import urllib
from urllib.request import urlopen
import json
from datetime import datetime, timedelta

shodanApiKey = 'GwQvrMaovMlfyoslpSiaQrZia2VNjaQF'

def connect(url, data, headers): # Function makes request with passed variables
    request = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(request)
    responseStr = response.read().decode('utf-8')
    return responseStr

def load():
    ip = input("Please enter an IP to lookup: ")
    date = datetime.now()# - timedelta(10)
    print (date.strftime('%d/%m/%y'))
    url = "https://api.shodan.io/shodan/host/count?key=" + shodanApiKey + "&query=" + ip +'&facets=before:'+date.strftime('%d/%m/%y')
    print (url)
    data = None
    headers = headers = {'X-PrettyPrint' : '1'}
    responseStr = connect(url, data, headers)
    res_dict = json.loads(responseStr)
    print (res_dict)
load()