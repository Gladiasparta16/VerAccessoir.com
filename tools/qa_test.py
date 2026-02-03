import sys
import os
import json
import urllib.request
import urllib.error
import random
import time

BASE = "http://127.0.0.1:5000"

results = []

import requests


def do_get(path):
    url = BASE + path
    try:
        r = requests.get(url, timeout=5, headers={'User-Agent':'QA-Agent'})
        return r.status_code, r.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def do_post(path, data):
    url = BASE + path
    try:
        r = requests.post(url, json=data, timeout=10, headers={'User-Agent':'QA-Agent'})
        return r.status_code, r.text
    except requests.exceptions.RequestException as e:
        # return None and include exception text for better debugging
        return None, str(e)


def wait_for_server(timeout=15):
    """Poll /api/health until server responds or timeout (seconds)."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(BASE + '/api/health', timeout=3, headers={'User-Agent':'QA-Agent'})
            if r.status_code == 200:
                print('QA: Server responded to /api/health')
                return True
            else:
                print(f'QA: /api/health returned {r.status_code}')
        except requests.exceptions.RequestException as e:
            print('QA: server not ready yet:', e)
        time.sleep(0.5)
    print(f'QA: server did not respond within {timeout}s')
    return False


print('QA: Attente 1s pour laisser le serveur démarrer...')
# Wait for server readiness (first quick pause, then poll)
time.sleep(1)
if not wait_for_server(timeout=15):
    print('\nÉCHEC: le serveur ne répond pas sur', BASE)
    sys.exit(3)

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

# 4. POST admin login (read credentials from env for QA or skip)
admin_email = os.environ.get('QA_ADMIN_EMAIL')
admin_password = os.environ.get('QA_ADMIN_PASSWORD')
if admin_email and admin_password:
    admin = {'email': admin_email, 'password': admin_password}
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
else:
    print('QA: QA_ADMIN_EMAIL not set — skipping admin login test')

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
