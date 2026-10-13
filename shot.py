from playwright.sync_api import sync_playwright
import sys
url=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
  for n,w,h in [("phone",390,844),("tablet",768,1024),("desktop",1440,900)]:
    pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=2 if n=="phone" else 1)
    pg.goto(url);pg.wait_for_timeout(1200)
    print(n,"scrollW",pg.evaluate("document.documentElement.scrollWidth"),w)
    pg.screenshot(path=f"shots/{n}-{w}.png",full_page=True)
