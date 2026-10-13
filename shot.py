from playwright.sync_api import sync_playwright
import sys
url=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
  for n,w,h,d in [("phone",390,844,3),("macbook-air",1470,956,2),("macbook-air",1280,800,2),("monitor",2560,1440,1)]:
    pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=d)
    pg.goto(url);pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const de=document.documentElement;const small=[...document.querySelectorAll('a,button,summary')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&(r.height<44||r.width<44)}).map(e=>e.textContent.trim().slice(0,30));
    const cut=[...document.querySelectorAll('*')].filter(e=>e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflowX!='visible').length;
    return {sw:de.scrollWidth,small,cut,main:document.querySelector('main').getBoundingClientRect().width}}""")
    print(n,w,r)
    pg.screenshot(path=f"shots/{n}-{w}.png",full_page=True)
