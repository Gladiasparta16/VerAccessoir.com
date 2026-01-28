from playwright.sync_api import sync_playwright

BASE = 'http://localhost:5000'

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        # capture console messages
        page.on('console', lambda msg: print('PAGE LOG:', msg.type, msg.text))

        print('Opening homepage...')
        page.goto(BASE + '/')
        page.wait_for_selector('.products .product-card .add-to-cart', timeout=5000)
        btn = page.query_selector('.products .product-card .add-to-cart')
        if not btn:
            print('ERROR: add-to-cart button not found')
            return
        print('Found add-to-cart buttons:', page.evaluate("() => document.querySelectorAll('.products .product-card .add-to-cart').length"))
        print('First add-to-cart outerHTML:', page.evaluate("() => document.querySelector('.products .product-card .add-to-cart').outerHTML"))
        print('LocalStorage cart before:', page.evaluate("() => localStorage.getItem('cart')"))
        btn.click()
        # give JS time to update localStorage and badge
        page.wait_for_timeout(500)
        badge = page.evaluate("() => document.querySelector('.cart-badge')?.textContent || ''")
        print('LocalStorage cart after:', page.evaluate("() => localStorage.getItem('cart')"))
        print('Cart badge after click:', badge)

        # Test client login
        print('Opening client login...')
        page.goto(BASE + '/pages/login.html')
        page.wait_for_selector('#clientEmail', timeout=5000)
        # use admin test credentials (admin user exists from seeding)
        page.fill('#clientEmail', 'admin@veraccessoire.com')
        page.fill('#clientPassword', 'admin123')
        page.click('#clientForm button[type=submit]')
        # wait for potential redirect
        try:
            page.wait_for_url(BASE + '/pages/account.html', timeout=3000)
            print('Login redirected to account page')
        except Exception:
            # check for token in localStorage
            token = page.evaluate("() => localStorage.getItem('token')")
            current = page.evaluate("() => localStorage.getItem('currentUser')")
            print('Login token:', bool(token), 'currentUser:', bool(current))

        # print some localStorage for debug
        token = page.evaluate("() => localStorage.getItem('token')")
        user = page.evaluate("() => localStorage.getItem('currentUser')")
        print('Final token present:', bool(token))
        print('Final currentUser present:', bool(user))

        context.close()
        browser.close()

if __name__ == '__main__':
    run()
