from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:5000'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.on('console', lambda msg: print('PAGE LOG:', msg.type, msg.text))
    print('Opening shop...')
    page.goto(BASE + '/pages/shop.html')
    # Wait for the products container to be updated by JS
    page.wait_for_selector('.products', timeout=10000)
    html = page.evaluate("() => document.querySelector('.products')?.innerHTML || ''")
    print('DEBUG: products HTML length:', len(html))
    print('DEBUG: first 500 chars:', html[:500])

    # ensure cart empty
    page.evaluate("() => localStorage.removeItem('cart')")
    page.reload()

    # Wait for a product card to appear and click
    try:
        page.wait_for_selector('.product-card .add-to-cart', timeout=10000)
        page.click('.product-card .add-to-cart')
        page.wait_for_timeout(300)
        print('Cart after one add:', page.evaluate("() => localStorage.getItem('cart')"))
    except Exception as e:
        print('Could not add product via UI:', e)
        print('Products HTML snapshot:', html[:2000])
        raise
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
