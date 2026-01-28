#!/usr/bin/env python3
"""Simple test: authenticate as admin, toggle a product's `featured` flag via API,
and verify the change persisted.

Run using the project's Python environment, for example:
  .venv\Scripts\python.exe BACKEND\tools\e2e_admin_featured.py
"""
import sys
import requests

BASE = 'http://localhost:5000'
ADMIN_EMAIL = 'admin@veraccessoire.com'
ADMIN_PASS = 'admin123'


def login(email, password):
    url = f"{BASE}/api/auth/login"
    r = requests.post(url, json={'email': email, 'password': password})
    if r.status_code != 200:
        print('LOGIN FAILED', r.status_code, r.text)
        return None
    data = r.json()
    return data.get('access_token')


def list_products():
    url = f"{BASE}/api/products/"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def update_product(product_id, payload, token):
    url = f"{BASE}/api/products/{product_id}"
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.put(url, json=payload, headers=headers)
    return r


def main():
    print('Logging in as admin...')
    token = login(ADMIN_EMAIL, ADMIN_PASS)
    if not token:
        print('Cannot run test without admin token.')
        sys.exit(2)

    products = list_products()
    if not products:
        print('No products returned; aborting test.')
        sys.exit(3)

    # pick first product
    p = products[0]
    pid = p.get('id')
    current = bool(p.get('featured', False))
    new = (not current)
    print(f"Toggling product id={pid} featured: {current} -> {new}")

    resp = update_product(pid, {'featured': new}, token)
    if resp.status_code not in (200, 204):
        print('Update failed', resp.status_code, resp.text)
        sys.exit(4)

    # re-fetch and verify
    products_after = list_products()
    pid_after = next((x for x in products_after if x.get('id') == pid), None)
    if pid_after is None:
        print('Product missing after update')
        sys.exit(5)

    featured_after = bool(pid_after.get('featured', False))
    print('Featured after update:', featured_after)
    if featured_after == new:
        print('TEST PASSED: featured flag toggled successfully')
        sys.exit(0)
    else:
        print('TEST FAILED: featured flag did not change')
        sys.exit(6)


if __name__ == '__main__':
    main()
