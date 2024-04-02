import requests
import json

def application(environ, start_response):
    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    apiRichiesta = str(environ['QUERY_STRING'])
    if request_method == 'GET':
    #if True:
        # Distinguere in base al parametro la chiamata la funzione
        if apiRichiesta == "type=online":
            output = "\"Accessori.csv\", \"Donna.csv\"}"
        else:
            output = "0x10: Comando GET non accettato."

    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
        ('Access-Control-Allow-Origin', '*')
    ]
    start_response(status, response_headers)
    return [output]
