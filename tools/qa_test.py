import sys
import json
import urllib.request
import urllib.error
import random
import time

BASE = "http://localhost:5000"

results = []

def do_get(path):
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"QA-Agent"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
            return resp.getcode(), body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, str(e)


def do_post(path, data):
    url = BASE + path
    b = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=b, headers={
        'Content-Type':'application/json',
        'User-Agent':'QA-Agent'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
            return resp.getcode(), body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, str(e)


print('QA: Attente 1s pour laisser le serveur démarrer...')
time.sleep(1)

# 1. GET /api/products
code, body = do_get('/api/products')
ok = (code == 200)
results.append(('GET /api/products', ok, code))
print('GET /api/products ->', code)

# 2. GET /shop.html
code, body = do_get('/shop.html')
ok2 = (code == 200)
results.append(('GET /shop.html', ok2, code))
print('GET /shop.html ->', code)

# 3. GET /cart.html
code, body = do_get('/cart.html')
ok3 = (code == 200)
results.append(('GET /cart.html', ok3, code))
print('GET /cart.html ->', code)

# 4. POST admin login
admin = {'email':'admin@veraccessoire.com', 'password':'admin123'}
code, body = do_post('/api/auth/login', admin)
ok4 = (code == 200)
token_present = False
try:
    j = json.loads(body)
    if isinstance(j, dict) and ('access_token' in j or 'token' in j or 'accessToken' in j):
        token_present = True
except Exception:
    token_present = False
results.append(('POST /api/auth/login', ok4 and token_present, code))
print('POST /api/auth/login ->', code, ' token:', token_present)

# 5. Optional: try register with random email
rand = random.randint(1000,9999)
user = {'email':f'test{rand}@example.com', 'password':'Test1234'}
code, body = do_post('/api/auth/register', user)
reg_ok = (code in (200,201))
results.append(('POST /api/auth/register', reg_ok, code))
print('POST /api/auth/register ->', code)

# Summary
print('\n=== Résumé QA ===')
failed = []
for name, ok, code in results:
    status = 'OK' if ok else 'FAIL'
    print(f'- {name}: {status} (HTTP {code})')
    if not ok:
        failed.append((name, code))

if failed:
    print('\nÉCHEC: Certains contrôles ont échoué.')
    sys.exit(2)
else:
    print('\nTOUS LES CONTRÔLES ONT RÉUSSI')
    sys.exit(0)
