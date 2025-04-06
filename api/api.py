def application(environ, start_response):
    status = '200 OK'
    output = b"Ciao modo"
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
        ('Access-Control-Allow-Origin', '*')
    ]
    start_response(status, response_headers)
    return [output]
