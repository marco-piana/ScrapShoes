def application(environ, start_response):
    import sys
    sys.path.insert(0, '/home/shoes/public_html/api')

    from lib import scrap, clean_scrap

    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    apiRichiesta = str(environ['QUERY_STRING'])
    if request_method == 'GET':
        # Distinguere in base al parametro la chiamata la funzione
        if apiRichiesta == "type=scrap":
            scraped_csv = scrap("/home/shoes/public_html/www/scrap/")
            output = ", ".join(x for x in scraped_csv)
        elif apiRichiesta == "type=clean":
            output = clean_scrap("/home/shoes/public_html/www/scrap/")
        else:
            output = "0x10: Comando GET non accettato."

    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
        ('Access-Control-Allow-Origin', '*')
    ]
    start_response(status, response_headers)
    return [output]
