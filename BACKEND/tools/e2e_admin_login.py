from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:5000'


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.on('console', lambda msg: print('PAGE LOG:', msg.type, msg.text))

        print('Opening admin login...')
        page.goto(BASE + '/pages/admin-login.html')
        try:
            page.wait_for_selector('#adminEmail', timeout=5000)
        except Exception as e:
            print('ERROR: admin form not found', e)
            context.close()
            browser.close()
            return

        page.fill('#adminEmail', 'admin@veraccessoire.com')
        page.fill('#adminPassword', 'admin123')
        page.click('#adminForm button[type=submit]')

        # wait for possible redirect to admin.html
        try:
            page.wait_for_url(BASE + '/pages/admin.html', timeout=4000)
            print('Redirected to admin page')
        except Exception:
            token = page.evaluate("() => localStorage.getItem('token')")
            adminUser = page.evaluate("() => localStorage.getItem('adminUser')")
            print('Token present:', bool(token))
            print('adminUser present:', bool(adminUser))

        context.close()
        browser.close()


if __name__ == '__main__':
    run()
