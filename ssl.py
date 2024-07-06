import ssl
context = ssl._create_unverified_context()
urllib.request.urlopen(req,context=context)