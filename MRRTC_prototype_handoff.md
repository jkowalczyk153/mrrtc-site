# MRRTC website prototype: locked, build on this

Status: LOCKED as the current prototype, updated 2026-10-01 (real logo in, nav order and menu bugs fixed, smoke test added). This is the version going to hosting. File: `MRRTC_website_prototype.html` (single self-contained HTML, images embedded). Other chats should start from this file and extend it. Do not redesign or rebuild from scratch unless the user asks.

## What's in it

Pages (all in one file, switched by nav):
- Home: locked hero rotator, gold bar, status map section with trail timetable list, railroad-history block, donate/volunteer band
- Trail Map (`#map`): large status map, how to read it, link to the interactive Google My Map, "coming later" filter chips
- Trail Info (`#trails`): five trail profiles, sample trail conditions
- Plan My Visit (`#plan`): three suggested long rides, each with a status bar and Heads up / Good to know / Coming soon / Not yet planned flags, plus shorter rides
- About / Donate (`#about`): mission, board member list, funding note, donate placeholder, contact
- Volunteer (`#volunteer`): simple form (prototype only)

Nav order everywhere: Trail Map, Plan My Visit, Trail Info, About / Donate, Volunteer.

## Locked, don't change without asking

- The hero rotator block (from `mrrtc-hero-rotator.html`), used verbatim: 3 slides, 6 s each, crossfade, pause on hover/focus, swipe, dots + arrows, photo credit, gold bar below. Only additions: nav links wired to pages, "Find a trail" scrolls to the map, a Menu button on phones.
- The status map image (Map B v6) and its look. New maps follow `MRRTC_map_style_guide.md`.
- Home page order: rotator, then the map immediately after.

## How it's built (read before editing)

- Edit the HTML directly (targeted string replacements). The original build scripts are not saved, and images are base64 inside the file, so don't try to regenerate it.
- Routing: each page is a `<section class="page" id="...">`. Two layers work together so the site still shows without JavaScript: CSS `:target` plus a `data-page` attribute set by a small script. To add a page: add the section, add its id to the `pages` array in the script, add a `body[data-page=...]` CSS rule next to the others, and add nav links in the hero nav and the solid header.
- Inner pages each start with a solid header (`.sitehead`). The home page uses the rotator's own overlay nav.
- Mobile menus use a hidden checkbox plus label (`.mt`, `.menubtn`, `.sh-menu`), not JavaScript.
- Class names to avoid reusing: the rotator owns `.hero .nav .copy .cta .controls .dots .dot .arrow .credit .slide .wordmark .bar`. Site styles use `.sitehead .hbar .band .st .btn .sec .ph1 .ride .flag .pill .strip`.
- Fonts and colors come from the rotator's placeholder Direction 1: gold #EDCA49, green #458C58, navy #48525C; Iowan Old Style/Palatino serif headings, system sans body. Buttons use a darker green #2F6B40 for contrast.
- Test any change with JavaScript off, at phone width, and in a sandboxed iframe. An earlier version showed blank in the Claude app viewer because pages were hidden until a script ran.

## Placeholders and open items

- Logo: real logo is in (circular PNG, 200px, embedded once as the CSS variable `--logo`, used by `.brand i` and `.wordmark i`). Source was small and soft; swap in a bigger PNG or SVG when the board supplies one. Hero version sits on a white ring for contrast.
- Photos: rotator photos credit Stuart Green / Trailspotting.com (permission confirmed). The Troy depot, Ashuelot, Monadnock and Peterborough photos lower on the site also use his work; the Troy caption now credits him without the "permission needed" note. Fort Hill has no photo yet.
- Parking details, trail conditions, and the Heads up / Good to know notes are sample content until the board confirms them.
- Mileage is approximate (apportioned from board-deck totals by map geometry). The Brattleboro bridge is drawn as in progress, which is a guess to confirm.
- Not built yet: Bellows Falls connector line, Fort Hill 8.5 vs 2.5 mi West Connector clarification, real donation flow, working volunteer form, map filters (parking, restrooms, food, sights).
- "Open the interactive map" links to the viewer version of the board's Google My Map, not the edit link.

## REQUIRED before delivering ANY edit: run the smoke test

File: `mrrtc_smoke_test.py` (same folder). Run: `python3 mrrtc_smoke_test.py MRRTC_website_prototype.html`. Must print ALL PASS. If it fails, fix and rerun before telling the user it's done. If you add a page or nav item, update `PAGES` in the test too.

It also checks NO WHITE TAIL on every page at 360/390/440px: footer is the last thing in the document, nothing renders below it, the bottom edge is footer-dark. Keep the `html{background}` + flex-column `body>main{flex:1}` guard in the CSS (see "no-white-tail guard"). Any new page or section must end above the footer.

It checks, inside a sandboxed iframe at phone width (how the Claude app viewer runs it): every hero and inner-page menu link, landing page buttons, Find a trail, Donate, readable menu text (contrast), nav order, no JS errors. Also checks deep links and Back in a normal browser, and that the site works with JavaScript off, plus desktop nav order.

Lessons from past bugs (all JavaScript or CSS routing):
- Never rely on the browser's own `#hash` navigation for page links. The app viewer's sandbox blocks it. Every page link must call `e.preventDefault()` and `show(page)` in the script. History is updated with `pushState` in a try/catch only as a bonus.
- Mobile menu CSS for the hero (`.mt:checked~nav...`) must stay scoped under `.hero`, or it restyles the inner-page menus (dark box, invisible text).
- Testing at top level in a normal browser is not enough. Always test in the sandboxed iframe.
- Back button may leave the site inside the app viewer. That's expected there.

## Hosting

Not hosted yet. Netflix-approved paths: Jetpack or Posit Connect, via #ntech-help. Netlify, Vercel, GitHub Pages and similar are not approved for Netflix work. Ask #security-help which path is OK for a public non-Netflix volunteer site. The page has a no-index tag for now; remove it when the site goes live.

## Map update workflow

User builds the map in Google Maps (red unplanned, yellow in progress, green rehabilitated, scale bar, town labels on, closeups of tricky spots). Claude redraws it in the branded style per the style guide, flags estimated mileage, and swaps the new image into the Home and Trail Map pages.

## White tail (2026-10-01)

User saw several screens of white below the footer on iPhone Safari (GitHub Pages). Not reproducible in Chromium, so a defensive guard was added: footer-dark `html` background, `overflow-x:clip`, flex-column body so the footer always ends the page, closed `<dialog>` forced hidden. If it still shows on a phone, get a fresh screen recording or screenshot and look for iOS-specific causes.
