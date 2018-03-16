import urllib
from urllib.request import urlopen
import json


def connect(url, data, headers): # Function makes request with passed variables
    request = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(request)
    responseStr = response.read().decode('utf-8')
    return responseStr

def request():
    account = 'joe.kulp@gmail.com'#input("Account to lookup: ")
    url = "https://haveibeenpwned.com/api/v2/breachedaccount/"+ account
    data = None
    headers = headers = {'X-PrettyPrint' : '1'}
    responseStr = connect(url, data, headers)
    res_dict = {}
    res_dict = json.loads(responseStr)[0:30]
    for  i in res_dict:
        print (i)
    #domain = a['Domain']
    #print (domain)

def parse():
    print ('ayyy')

request()