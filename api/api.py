import requests
import json
from urllib import unquote_plus

# Features
# Supporta un unico merchant ID


sandboxURL = "https://api-sandbox.merchants.zalando.com"
productionURL = "https://api.merchants.zalando.com"
clientID = "017e345dfb5363a216c6342a306f84a4"
clientSecret = "cb8351e5-4ad0-4582-bd92-80876dd8f129"
authentication = str(clientID+":"+clientSecret).encode('base64').replace("\n", "")


isTest = False
apiURL = sandboxURL if isTest else productionURL

token = ""

def zalandoAPI_Me():
    token = zalandoAPI_RequestAccessToken()
    headers = {"Authorization": "Bearer " + token}
    r = requests.get(apiURL + "/auth/me", headers=headers)
    return r.text

def zalandoAPI_MerchantIDs():
    token = zalandoAPI_RequestAccessToken()
    headers = {"Authorization": "Bearer " + token}
    r = requests.get(apiURL + "/auth/me", headers=headers)
    return r.text

def zalandoAPI_RequestAccessToken():
    headers = {"Authorization": "Basic " + authentication}
    payload = {"grant_type": "client_credentials", "scope": "access_token_only"}
    r = requests.post(apiURL + "/auth/token", data=payload,headers=headers)
    response = r.json()
    token = response['access_token']
    return token

def zalandoAPI_PriceUpdateRequest(body):
    token = zalandoAPI_RequestAccessToken()
    merchantID = "602e66a4-cfd4-4060-8046-323f65abfd07"
    headers = {"Authorization": "Bearer " + token}
    postURL = "%s/merchants/%s/prices" % (apiURL, merchantID)
    r = requests.post(postURL,body,headers=headers)
    return r.text

def application(environ, start_response):
    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    apiRichiesta = str(environ['QUERY_STRING'])
    if request_method == 'GET':
    #if True:
        # Distinguere in base al parametro la chiamata a ZalandoAPI
        if apiRichiesta == "type=me":
            output = str(zalandoAPI_Me()).encode()
        elif apiRichiesta == "type=token":
            output = str(zalandoAPI_RequestAccessToken()).encode()
        elif apiRichiesta == "type=merchantIDs":
            output = str(zalandoAPI_MerchantIDs()).encode()
        else:
            output = "0x10: Comando GET non accettato."
        
    elif request_method == 'POST':
        output = "POST o altro"
        if apiRichiesta == "type=PriceUpdateRequest":
            body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
            output = str(zalandoAPI_PriceUpdateRequest(body)).encode()
        else:
            output = "0x10: Comando GET non accettato."
    else:
        output = "0x06: Methodo non accettato."
    

    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
        ('Access-Control-Allow-Origin', '*')
    ]
    start_response(status, response_headers)
    return [output]
