from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:5000'
OUT = 'BACKEND/tools/shop_page.png'

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1200, "height": 900})
    page = context.new_page()
    print('Opening', BASE + '/pages/shop.html')
    try:
        page.goto(BASE + '/pages/shop.html', timeout=60000)
        page.wait_for_load_state('networkidle', timeout=60000)
        # wait a bit for dynamic content
        page.wait_for_timeout(800)
        page.screenshot(path=OUT, full_page=True)
        print('Saved screenshot to', OUT)
    except Exception as e:
        print('Failed to capture screenshot:', e)
    context.close()
    browser.close()
