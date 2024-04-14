import logging

from api.scrap import scrap, clean_scrap

LOGLVL_INFO = logging.INFO
LOGLVL_DEBUG = logging.DEBUG
LOGLVL_ERROR = logging.ERROR
LOGLVL_WARNING = logging.WARNING
LOGLVL_DEFAULT = LOGLVL_INFO

log = logging.getLogger()
log.setLevel(LOGLVL_DEFAULT)

file = "/home/shoes/logs/apishoes.log"
f_format = logging.Formatter('[%(asctime)s]-[%(levelname)s]-%(message)s')
hdlr = logging.FileHandler(file)
hdlr.setFormatter(f_format)
log.addHandler(hdlr)

def application(environ, start_response):
    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    apiRichiesta = str(environ['QUERY_STRING'])
    if request_method == 'GET':
        # Distinguere in base al parametro la chiamata la funzione
        if apiRichiesta == "type=scrap":
            scraped_csv = scrap("/home/shoes/public_html/www/scrap/")
            output = ", ".join(x for x in scraped_csv)
        if apiRichiesta == "type=clean":
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
