import requests
import json

def getPageNumber():
    #headers = {}
    #apiURL = "https://scarpesp.com/categoria-prodotto/donna/page/5/?count=36"
    #r = requests.get(apiURL, headers=headers)
    #return r.text
    return "{\"Accessori\":\"Accessori.csv\", \"Donna\":\"Donna.csv\"}"
#
# def zalandoAPI_MerchantIDs():
#     token = zalandoAPI_RequestAccessToken()
#     headers = {"Authorization": "Bearer " + token}
#     r = requests.get(apiURL + "/auth/me", headers=headers)
#     return r.text
#
# def zalandoAPI_RequestAccessToken():
#     headers = {"Authorization": "Basic " + authentication}
#     payload = {"grant_type": "client_credentials", "scope": "access_token_only"}
#     r = requests.post(apiURL + "/auth/token", data=payload,headers=headers)
#     response = r.json()
#     token = response['access_token']
#     return token
#
# def zalandoAPI_PriceUpdateRequest(body):
#     token = zalandoAPI_RequestAccessToken()
#     merchantID = "602e66a4-cfd4-4060-8046-323f65abfd07"
#     headers = {"Authorization": "Bearer " + token}
#     postURL = "%s/merchants/%s/prices" % (apiURL, merchantID)
#     r = requests.post(postURL,body,headers=headers)
#     return r.text

def application(environ, start_response):
    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    apiRichiesta = str(environ['QUERY_STRING'])
    if request_method == 'GET':
    #if True:
        # Distinguere in base al parametro la chiamata la funzione
        if apiRichiesta == "type=online":
            output = "{\"Accessori\":\"Accessori.csv\", \"Donna\":\"Donna.csv\"}"
        else:
            output = "0x10: Comando GET non accettato."

    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
        ('Access-Control-Allow-Origin', '*')
    ]
    start_response(status, response_headers)
    return [output]
