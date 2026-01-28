from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:5000'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.on('console', lambda msg: print('PAGE LOG:', msg.type, msg.text))
    print('Opening shop...')
    page.goto(BASE + '/pages/shop.html')
    page.wait_for_selector('.product-card .add-to-cart', timeout=5000)
    # ensure cart empty
    page.evaluate("() => localStorage.removeItem('cart')")
    page.reload()
    # add first product
    page.click('.product-card .add-to-cart')
    page.wait_for_timeout(300)
    print('Cart after one add:', page.evaluate("() => localStorage.getItem('cart')"))
    # remove using btn-remove if visible in cart page: open cart
    page.goto(BASE + '/pages/cart.html')
    try:
        page.wait_for_selector('.btn-remove', timeout=2000)
        page.click('.btn-remove')
        page.wait_for_timeout(300)
        print('Cart after remove click:', page.evaluate("() => localStorage.getItem('cart')"))
        print('Badge:', page.evaluate("() => document.querySelector('.cart-badge')?.textContent || ''"))
    except Exception as e:
        print('No remove button found on cart page:', e)
    context.close()
    browser.close()
