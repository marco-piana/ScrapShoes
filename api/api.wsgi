import requests


apiURL = "https://api-sandbox.merchants.zalando.com"
headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJxSXJSLUZkdm5vcms2RktjcV9nNDFUa3p4VC16dk8welRyUHFUM0tMem9zIn0.eyJleHAiOjE2NDE1NzkzMTMsImlhdCI6MTY0MTU3MjExMywianRpIjoiN2JhMTc2ZDItYzlhNi00MTI2LWEwMDUtYmU1ZGU5Mjc5NDhiIiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5tZXJjaGFudC1jZW50ZXIuemFsYW4uZG8vYXV0aC9yZWFsbXMvbWVyY2hhbnQtcGxhdGZvcm0iLCJhdWQiOlsiemZzIiwicHJvZmlsZSIsIm9yZGVycyIsImFydGljbGVzIiwicHJvZHVjdHMiXSwic3ViIjoiMTM0Nzk1M2YtMzcxNC00NjZjLWIxOWQtNmFiOGE2Njk0ZTEyIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiMDE3ZTM0NWRmYjUzNjNhMjE2YzYzNDJhMzA2Zjg0YTQiLCJzZXNzaW9uX3N0YXRlIjoiYzRmNDY3YWMtYWRjYy00ZjYxLThiYzItNTZiZTFiMGIyMjBlIiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJzYW5kYm94Il19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiemZzIjp7InJvbGVzIjpbInN0b2NrLWxvY2F0aW9uL3JlYWQiLCJzaGlwcGluZy1ub3RpY2Uvd3JpdGUiLCJ0b3Vycy9yZWFkIiwic2hpcHBpbmctbm90aWNlL3JlYWQiLCJyZWNlaXZlZC1pdGVtL3JlYWQiLCJyZXR1cm5lZC1pdGVtL3JlYWQiLCJpY20tcmVwb3J0cy9yZWFkIiwiaXRlbS1xdWFudGl0aWVzL3JlYWQiXX0sInByb2ZpbGUiOnsicm9sZXMiOlsic2FsZXMtY2hhbm5lbHMvcmVhZCJdfSwib3JkZXJzIjp7InJvbGVzIjpbInJlYWQiLCJ3cml0ZSJdfSwiYXJ0aWNsZXMiOnsicm9sZXMiOlsic3RvY2svd3JpdGUiLCJwcmljZS93cml0ZSJdfSwicHJvZHVjdHMiOnsicm9sZXMiOlsic3RvY2svd3JpdGUiLCJyZWFkIiwiYmxvY2tlcnMvcmVhZCIsInByaWNlL3JlYWQiLCJibG9ja2Vycy93cml0ZSIsInByaWNlL3dyaXRlIiwiYXR0cmlidXRlcy9yZWFkIiwid3JpdGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwgYWNjZXNzX3Rva2VuX29ubHkiLCJicGlkcyI6IjYwMmU2NmE0LWNmZDQtNDA2MC04MDQ2LTMyM2Y2NWFiZmQwNyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SWQiOiIwMTdlMzQ1ZGZiNTM2M2EyMTZjNjM0MmEzMDZmODRhNCIsImFjY291bnRfaWQiOiI3ZmU0M2MzNS1jN2Q3LTRlMWUtOTRkNy1hZTYxMzViMzQ4NmUiLCJjbGllbnRIb3N0IjoiMTUxLjE2LjM2LjEwIiwidGVjaF9hY2NvdW50X25hbWUiOiJjcCBncmFwaGljIGRlc2lnbmVyIiwibWVyY2hhbnRfYWNjb3VudF9pZCI6ImFlODA0YjdlLTQ2ZTUtNGU2Mi1iZjJjLTUzNTQ5MzkzMjkwZCIsIm1lcmNoYW50X2FjY291bnRfbmFtZSI6ImFudHVyYSBhY2Nlc3NvcmkiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtMDE3ZTM0NWRmYjUzNjNhMjE2YzYzNDJhMzA2Zjg0YTQiLCJjbGllbnRBZGRyZXNzIjoiMTUxLjE2LjM2LjEwLCAxOC4xODUuNDguMTY4In0.Tf9ntHQ3MA56DApmhOrq8jbYC5Fy25Gr-4fK1VCokpst7DpGVc5DG6tU_tBnDwmr8IMtGoimSx_PNfh377c1fQyGXe4hPgZx_5Z2X9YufxvTqA1fn2_bG1a0w_uxQyNTQJ3lX2z2OCHXz_0CLa8YtHCKm1j7pY2muas4kIt8ZnFdC-rKc745VxOsRveo54D1LDq8Q6v0k_Pu1ShF4xWK10DdLnCeg8Nputp1uIwrd91GeTzMyngQjJc1Lcf-Yr3xIzyD4OV5AMWrFtN7xur6Hf3ysj_p00j-vvDVfIeFK8rA7GSTJmYZD5DrXL460A6chCuUiLsJ49C58QFcpCHboA" }


def zalandoAPIMe():
    pass




def application(environ, start_response):
    status = '200 OK'



    r = requests.get(apiURL + "/auth/me", headers=headers)
    
    
    output = r.text.encode()
    try:
        output = str(environ['QUERY_STRING']).encode()
    except:
        output = "Errore 500 del server".encode()
        status = '500'
    

    case 


    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output))),
        ('Access-Control-Allow-Origin', '*')
    ]
    
    



    start_response(status, response_headers)
    return [output]
