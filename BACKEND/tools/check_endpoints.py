import urllib.request

endpoints = [
    'http://127.0.0.1:5000/api/products/',
    'http://127.0.0.1:5000/api/auth/health'
]

for url in endpoints:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read().decode('utf-8')
            print('URL:', url)
            print('STATUS:', r.status)
            print('BODY_PREVIEW:', body[:500])
    except Exception as e:
        print('URL:', url)
        print('ERROR:', repr(e))
