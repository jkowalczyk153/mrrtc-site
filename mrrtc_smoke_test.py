#!/usr/bin/env python3
"""MRRTC prototype smoke test. Run after EVERY edit, before delivering.
Usage: python3 mrrtc_smoke_test.py /path/to/MRRTC_website_prototype.html
Needs: pip install playwright --break-system-packages (chromium already present in Claude's sandbox)
Tests run INSIDE a sandboxed iframe (like the Claude app viewer), at phone width, plus no-JS and desktop checks.
Exit code 0 = all pass, 1 = failures printed."""
import sys, html
from playwright.sync_api import sync_playwright

import os
SRC = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/MRRTC_website_prototype.html')
PAGES = [('map','Trail Map'),('plan','Plan My Visit'),('trails','Trail Info'),('about','About / Donate'),('volunteer','Volunteer')]
EXPECTED_ORDER = [l for _, l in PAGES]
fails = []
def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok: fails.append(msg)

CONTRAST_JS = """el=>{
 const rgb=s=>s.match(/[\\d.]+/g).map(Number);
 const lum=c=>{const [r,g,b]=c.map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
 let bg=null,n=el;
 while(n){const c=rgb(getComputedStyle(n).backgroundColor);if(c.length<4||c[3]>0.5){bg=c.slice(0,3);break}n=n.parentElement}
 bg=bg||[255,255,255];
 const fg=rgb(getComputedStyle(el).color).slice(0,3);
 const a=lum(fg),b=lum(bg);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)}"""

src = open(SRC, encoding='utf-8').read()
wrap = '<html><body style="margin:0"><iframe sandbox="allow-scripts allow-popups" style="width:390px;height:844px;border:0" srcdoc="%s"></iframe></body></html>' % html.escape(src, quote=True)
open('/tmp/mrrtc_wrap.html', 'w').write(wrap)

with sync_playwright() as p:
    b = p.chromium.launch()

    # ---- A. sandboxed iframe, phone width (the real-world viewer) ----
    pg = b.new_page(viewport={'width':400,'height':860})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto('file:///tmp/mrrtc_wrap.html'); pg.wait_for_timeout(700)
    fr = pg.frame_locator('iframe'); F = pg.frames[1]
    cur = lambda: F.evaluate("document.body.dataset.page")
    def home():
        if cur() != 'home':
            fr.locator('#%s .brand' % cur()).click(); pg.wait_for_timeout(250)
    check(cur() == 'home', 'loads on home inside sandboxed iframe')
    for pid, label in PAGES:                      # hero menu -> every page
        home(); fr.locator('label.menubtn').click(); pg.wait_for_timeout(150)
        ratio = fr.locator('#hero nav a.l', has_text=label).first.evaluate(CONTRAST_JS)
        check(ratio >= 4.5, 'hero menu link "%s" readable (contrast %.1f)' % (label, ratio))
        fr.locator('#hero nav a.l', has_text=label).click(); pg.wait_for_timeout(250)
        check(cur() == pid, 'hero menu -> %s' % label)
    home(); fr.locator('#home a.btn.green', has_text='Plan my visit').click(); pg.wait_for_timeout(250)
    check(cur() == 'plan', 'landing page "Plan my visit" button')
    home(); fr.locator('#home a.btn.out', has_text='Trail info').click(); pg.wait_for_timeout(250)
    check(cur() == 'trails', 'landing page "Trail info and conditions" button')
    home(); fr.locator('.cta').click(); pg.wait_for_timeout(500)
    check(cur() == 'home', '"Find a trail" stays on home')
    fr.locator('.band a[data-give]').click(); pg.wait_for_timeout(300)
    check(cur() == 'about', 'Donate button -> About/Donate')
    for start, _ in PAGES:                        # every inner page menu -> every page
        home(); fr.locator('label.menubtn').click(); pg.wait_for_timeout(100)
        fr.locator('#hero nav a.l', has_text=dict(PAGES)[start]).click(); pg.wait_for_timeout(250)
        for target, tlabel in PAGES:
            fr.locator('#%s label.sh-menu' % cur()).click(); pg.wait_for_timeout(120)
            if target == PAGES[0][0] and start == PAGES[0][0]: pass
            ratio = fr.locator('#%s .mainnav a' % cur(), has_text=tlabel).first.evaluate(CONTRAST_JS)
            if ratio < 4.5: check(False, 'menu text unreadable on %s (contrast %.1f)' % (cur(), ratio))
            order = F.eval_on_selector_all('#%s .mainnav a' % cur(), 'e=>e.map(a=>a.textContent)')
            if order != EXPECTED_ORDER: check(False, 'nav order wrong on %s: %s' % (cur(), order))
            fr.locator('#%s .mainnav a' % cur(), has_text=tlabel).first.click(); pg.wait_for_timeout(220)
            if cur() != target: check(False, 'inner menu %s -> %s landed on %s' % (start, target, cur()))
    check(not [f for f in fails if f.startswith(('inner menu','menu text','nav order'))], 'inner-page menus: all 25 page-to-page jumps, readable, correct order')
    check(not errs, 'no JS or console errors %s' % (errs or ''))
    pg.close()

    # ---- B. normal browser: deep link, back button ----
    pg = b.new_page(viewport={'width':390,'height':844})
    pg.goto('file://' + SRC + '#trails'); pg.wait_for_timeout(300)
    check(pg.evaluate("document.body.dataset.page") == 'trails', 'deep link #trails opens Trail Info')
    pg.click('#trails label.sh-menu'); pg.click('#trails .mainnav a >> text="Volunteer"'); pg.wait_for_timeout(200)
    pg.go_back(); pg.wait_for_timeout(250)
    check(pg.evaluate("document.body.dataset.page") == 'trails', 'back button returns to previous page')
    pg.close()

    # ---- C. JavaScript OFF: site still shows and menus still open ----
    c = b.new_context(java_script_enabled=False, viewport={'width':390,'height':844}); n = c.new_page()
    n.goto('file://' + SRC + '#plan'); n.wait_for_timeout(300)
    check(n.is_visible('#plan h1') and not n.is_visible('#home'), 'JS off: #plan shows, home hidden')
    n.click('#plan label.sh-menu'); n.wait_for_timeout(150)
    check(n.is_visible('#plan .mainnav a >> text="Trail Info"') and n.locator('#plan .mainnav a').first.evaluate(CONTRAST_JS) >= 4.5, 'JS off: menu opens and is readable')
    n.goto('file://' + SRC); n.wait_for_timeout(300)
    check(n.is_visible('#hero'), 'JS off: home hero visible')
    c.close()

    # ---- D. desktop nav order ----
    d = b.new_page(viewport={'width':1280,'height':800}); d.goto('file://' + SRC); d.wait_for_timeout(300)
    check(d.eval_on_selector_all('#hero nav a.l', 'e=>e.map(a=>a.textContent)') == EXPECTED_ORDER, 'desktop hero nav order')
    b.close()

print('\n%s (%d failure%s)' % ('ALL PASS' if not fails else 'FAILED', len(fails), '' if len(fails) == 1 else 's'))
sys.exit(1 if fails else 0)
