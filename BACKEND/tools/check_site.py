import requests
from bs4 import BeautifulSoup
import os
import sys

BASE='http://localhost:5000'
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FRONTEND'))
pages = ['index.html']
for root, dirs, files in os.walk(os.path.join(frontend_dir, 'pages')):
    for f in files:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), frontend_dir)
            pages.append(rel.replace('\\', '/'))

errors = []

print('Checking', len(pages), 'pages...')
for p in pages:
    if p == 'index.html':
        url = BASE + '/'
    elif p.startswith('pages/'):
        url = BASE + '/' + p
    else:
        url = BASE + '/' + p
    try:
        r = requests.get(url, timeout=5)
        print(f'PAGE {url} -> {r.status_code}')
        if r.status_code != 200:
            errors.append((url, r.status_code))
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        # find assets
        assets=[]
        for tag in soup.find_all(['script','link','img']):
            if tag.name=='script' and tag.get('src'):
                assets.append(tag.get('src'))
            if tag.name=='link' and tag.get('href'):
                assets.append(tag.get('href'))
            if tag.name=='img' and tag.get('src'):
                assets.append(tag.get('src'))
        for a in assets:
            # ignore external
            if a.startswith('http://') or a.startswith('https://') or a.startswith('//'):
                continue
            # resolve relative
            if a.startswith('/'):
                asset_url = BASE + a
            else:
                # relative to page path
                asset_url = BASE + '/' + os.path.dirname(p) + '/' + a if os.path.dirname(p) != '.' else BASE + '/' + a
            asset_url = asset_url.replace('//', '/')
            if asset_url.startswith('http:/'):
                asset_url = 'http://' + asset_url.split('http:/',1)[1]
            try:
                ar = requests.get(asset_url, timeout=5)
                if ar.status_code != 200:
                    errors.append((asset_url, ar.status_code))
                    print(f'  ASSET {asset_url} -> {ar.status_code}')
            except Exception as e:
                errors.append((asset_url, str(e)))
                print(f'  ASSET {asset_url} -> ERROR {e}')
    except Exception as e:
        errors.append((url, str(e)))

# check APIs
apis=['/api/products/','/api/auth/health']
for a in apis:
    try:
        r = requests.get(BASE + a, timeout=5)
        print(f'API {a} -> {r.status_code}')
        if r.status_code != 200:
            errors.append((BASE+a,r.status_code))
    except Exception as e:
        errors.append((BASE+a,str(e)))

print('\nSummary:')
if not errors:
    print('No issues found')
else:
    print('Found', len(errors), 'issues:')
    for e in errors:
        print(e)

# exit code 0/1
sys.exit(0 if not errors else 1)
