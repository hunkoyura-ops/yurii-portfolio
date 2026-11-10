import os, sys
OUT = sys.argv[1]

ARROW = '<svg class="arrow" role="img" aria-label="to"><use href="#arrow"/></svg>'
ARROW_H = '<svg class="arrow" aria-hidden="true"><use href="#arrow"/></svg>'

SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="arrow" viewBox="0 0 26 20">
    <path d="M1.5 10h22M15 2l8.5 8-8.5 8" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="ok" viewBox="0 0 20 20">
    <circle cx="10" cy="10" r="9" fill="#1F6B45"/><path d="M5.8 10.4l2.8 2.8 5.6-6" fill="none" stroke="#F4EEDC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="hold" viewBox="0 0 20 20">
    <circle cx="10" cy="10" r="9" fill="#B3311B"/><path d="M10 5.4v5.4" stroke="#F4EEDC" stroke-width="2.2" stroke-linecap="round"/><circle cx="10" cy="14.2" r="1.3" fill="#F4EEDC"/>
  </symbol>
</svg>'''

def head(title, desc, path):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://hunkoyura.com{path}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://hunkoyura.com{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://hunkoyura.com/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://hunkoyura.com/og.jpg">
<meta name="theme-color" content="#12382C" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#F4EEDC" media="(prefers-color-scheme: light)">
<meta name="color-scheme" content="dark light">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script>try{{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8R37BRJNRV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-8R37BRJNRV');
</script>
</head>
<body>

{SPRITE}

<header class="wrap top">
  <a class="name" href="/">Yurii Hunko</a>
  <nav aria-label="Site">
    <a href="/#tools">Tools</a>
    <a href="/#contact">Contact</a>
    <button type="button" class="theme" id="theme-toggle" aria-label="Switch theme">Light</button>
  </nav>
</header>
'''

FOOT = '''
<script src="/site.js"></script>
</body>
</html>
'''

TOOLS = [
 dict(slug='brief-to-script', a='Brief', b='Script', status='Live', wip=False,
  line='A brand brief and a creator\'s tone go in. A timecoded script draft comes out.',
  desc='Turns a brand brief and a creator\'s tone into a timecoded script draft with hook, body, proof and call to action.',
  lede='Turns a brand brief and a creator\'s tone into a timecoded script draft: hook, body, proof and call to action, with on-screen text, a caption and hashtags.',
  facts=[('Modes','One creator, a whole batch in one pass, or saved presets for creators you work with often'),
         ('Export','Google Docs or a .doc file'),
         ('Safety net','Falls back to local templates when the AI is unavailable, so it never returns nothing'),
         ('Built with','Cloudflare Workers, Claude API')],
  specimen='''    <div class="specimen">
      <div class="specimen-bar">
        <div class="picker" id="style-picker">
          <span>Creator tone</span>
          <button type="button" aria-pressed="true" data-style="calm">Calm, talks to camera</button>
          <button type="button" aria-pressed="false" data-style="fast">Fast, jump cuts</button>
          <button type="button" aria-pressed="false" data-style="dry">Dry humor</button>
        </div>
        <span>Sample data</span>
      </div>
      <div class="flow">
        <div class="paper">
          <h3>Brief</h3>
          <div class="row"><span>Brand</span><span>Pebble, a reusable bottle</span></div>
          <div class="row"><span>Platform</span><span>Reels, 30 seconds</span></div>
          <div class="row"><span>Message</span><span>Keeps drinks cold all day</span></div>
          <div class="row"><span>CTA</span><span>Promo code push</span></div>
          <div class="row"><span>Tone</span><span id="tone-echo">Calm, talks to camera</span></div>
          <p class="note">Same brief, different creator. Change the tone and the script is rewritten in their voice.</p>
        </div>
        ARROWH
        <div class="paper" aria-live="polite">
          <h3>Script draft</h3>
          <div class="swap" id="script-out"></div>
        </div>
      </div>
    </div>''',
  actions='''    <div class="actions">
      <a class="open" href="https://brief-to-script.hunkoyura.workers.dev/" target="_blank" rel="noopener">Open Brief to Script ARROWH</a>
      <a class="src" href="https://github.com/hunkoyura-ops/brief-to-script" target="_blank" rel="noopener">View source on GitHub</a>
    </div>''',
  story=[
   ('Why it exists', '<p>Writing a script for one creator used to take me 15 to 20 minutes, and every creator on a campaign needs their own, in their own voice. The brief stays the same. Only the voice changes.</p><p>That is repetitive work with a clear pattern, so I built a tool for it.</p>'),
   ('What goes in, what comes out', '<p>You set the brand or product, the key message, the platform (Stories, TikTok, Reels or Shorts), the video length (15, 30 or 60 seconds), the creator\'s tone and the style of the call to action: a soft mention, a promo code push, link in bio or an app install.</p><p>Back comes a script on a timeline. Each beat has the spoken line and a cue for on-screen text. A caption and hashtags come with it. Drafts can be saved to a library, opened in Google Docs or downloaded as a .doc file.</p>'),
   ('Decisions I made', '<ul><li><b>It never returns nothing.</b> Requests go through my own backend, a Cloudflare Worker that calls the Claude API. If the AI is unavailable, the tool falls back to local templates.</li><li><b>The script has to fit the clock.</b> The prompt holds the text to a speaking-pace budget for the chosen length.</li><li><b>No invented facts.</b> The model may not make up claims about the product that are not in the brief.</li><li><b>Disclosure stays a human job.</b> The tool reminds you about the paid partnership label or #ad, and does not add it for you.</li><li><b>A draft is a draft.</b> I still edit every one before it goes out, usually the hook.</li></ul>')]),
 dict(slug='post-to-report', a='Post', b='Report', status='Live, team access', wip=False,
  line='Reads the stats from a creator\'s screenshot and builds the campaign report.',
  desc='Reads post stats from creator screenshots, holds impossible numbers for manual review and builds the campaign report for the brand.',
  lede='Reads the stats from a creator\'s screenshot and builds the campaign report for the brand. Anything that can\'t be true is held back for a person to check, with the reason attached.',
  facts=[('Reads','Views, reach, likes, comments, shares, saves'),
         ('Two views','By campaign, with totals and a written summary. By creator, across every campaign they did'),
         ('Checks','Likes above views, engagement over 100%, reach far beyond the follower count'),
         ('Built with','Node.js, Claude Vision, Railway. Creator profiles are plain arithmetic, no AI call')],
  specimen='''    <div class="specimen">
      <div class="specimen-bar">
        <div class="picker" id="shot-picker">
          <span>Screenshot</span>
          <button type="button" aria-pressed="true" data-shot="clean">Reads cleanly</button>
          <button type="button" aria-pressed="false" data-shot="odd">Misread numbers</button>
        </div>
        <span>Sample data</span>
      </div>
      <div class="flow">
        <div class="paper">
          <h3>Screenshot from the creator</h3>
          <div class="shot swap" id="shot-in"></div>
        </div>
        ARROWH
        <div class="paper" aria-live="polite">
          <h3>What the tool recorded</h3>
          <div class="swap" id="shot-out"></div>
        </div>
      </div>
    </div>''',
  actions='''    <div class="actions">
      <a class="open" href="https://post-tracker-simple-production.up.railway.app" target="_blank" rel="noopener">Open Post to Report ARROWH</a>
      <a class="src" href="https://github.com/hunkoyura-ops/post-tracker-simple" target="_blank" rel="noopener">View source on GitHub</a>
    </div>
    <p class="aside">The tool asks you to sign in. Access is limited to my team.</p>''',
  story=[
   ('Why it exists', '<p>Creators send screenshots of their stats, and I used to retype the numbers into a spreadsheet. It is slow, and one mistyped digit ends up in a report the brand reads.</p>'),
   ('What goes in, what comes out', '<p>You upload the screenshot. The tool reads views, reach, likes, comments, shares and saves, and files them under the campaign and the creator.</p><p>The campaign view shows total views and reach, the average engagement rate and a written conclusion: top performers, anomalies, recommendations. The creator view is a profile across every campaign, with each post and its engagement rate, so you can see who delivers every time and not only once.</p>'),
   ('Decisions I made', '<ul><li><b>A recognition error must not reach the brand.</b> Every reading passes a validation layer. More likes than views, engagement above 100%, reach more than 20 times the follower count, a negative value: any of these sends the record to a manual review queue with the reason written out.</li><li><b>Clean records go straight through.</b> The queue only holds what needs a person.</li><li><b>No reach metric, no guess.</b> If the tool cannot read views, reach or impressions at all, it asks for manual input.</li><li><b>Creator profiles use no AI.</b> They are local arithmetic, so they open instantly and cost nothing in API quota.</li></ul>')]),
 dict(slug='inbox-to-triage', a='Inbox', b='Triage', status='Live in n8n', wip=False,
  line='Sorts creator replies after outreach and leaves a draft answer in Gmail.',
  desc='An n8n automation that sorts creator replies by intent, extracts prices and deadlines, and leaves a draft answer in Gmail.',
  lede='After outreach the replies pile up and the good ones get lost. This sorts each one by what the creator wants, pulls out the specifics and leaves a draft answer in Gmail. Nothing is sent without me.',
  facts=[('Sorts into','Interested, negotiating, question, declined, spam'),
         ('Pulls out','Quoted prices, deadlines, open questions'),
         ('Guardrails','The model may not invent budgets or dates. A malformed answer gets logged, the flow keeps running'),
         ('Built with','n8n, Claude API, Gmail, Google Sheets')],
  specimen='''    <div class="specimen">
      <div class="specimen-bar">
        <span>Pick a reply</span>
        <span>Sample data</span>
      </div>
      <div class="flow">
        <div class="paper">
          <h3>Replies in the inbox</h3>
          <div class="mails" id="mails"></div>
        </div>
        ARROWH
        <div class="paper" aria-live="polite">
          <h3>After triage</h3>
          <div class="swap" id="mail-out"></div>
        </div>
      </div>
    </div>''',
  actions='''    <p class="aside">Runs inside my own n8n workspace, so there is no public link. <a class="src" href="https://github.com/hunkoyura-ops/Inbox-Triage" target="_blank" rel="noopener">View the workflow on GitHub</a></p>''',
  story=[
   ('Why it exists', '<p>After creator outreach, dozens of replies land in the inbox. Some creators are interested, some negotiate the price, some decline, some write off-topic. Sorting them by hand is half an hour a day of reading and copying into a spreadsheet, and the hot replies get lost among the rest.</p>'),
   ('The flow, step by step', '<ol><li>Gmail picks up a new email with the creators label.</li><li>Claude classifies the intent, sets a priority and extracts the creator\'s name, quoted prices, deadlines and questions.</li><li>A switch branches by category.</li><li>For substantive replies, Claude writes a draft answer. Declines and spam skip this step.</li><li>The result is logged to a Google Sheet.</li><li>The draft is saved to Gmail Drafts.</li></ol>'),
   ('Decisions I made', '<ul><li><b>A draft, not an auto-send.</b> Automating the last step is easy, but a mistake in a conversation with a creator costs more than the minute saved.</li><li><b>Direct API calls instead of ready-made nodes.</b> Claude is called through an HTTP request, which gives full control over the prompt and parameters.</li><li><b>Errors are handled, not hoped away.</b> If the model returns something other than JSON, the flow logs the problem and keeps running. The switch has a fallback for an unexpected category.</li><li><b>No invented terms.</b> The model is forbidden to make up budgets, deadlines or conditions that are not in the email. What is missing gets marked as needing clarification.</li></ul>')]),
 dict(slug='search-to-shortlist', a='Search', b='Shortlist', status='In progress', wip=True,
  line='Campaign criteria in, a ranked list of creators to write to out.',
  desc='A creator search tool in progress: campaign criteria in, a ranked shortlist of creators out.',
  lede='Building a shortlist by hand means hours of scrolling. This takes the criteria for a campaign and returns a ranked list of creators worth writing to.',
  facts=[('Takes','Platform, niche, audience size, engagement rate, location'),
         ('Returns','A ranked list, best fit first'),
         ('Status','Being built. The preview shows the intended result')],
  specimen='''    <div class="specimen">
      <div class="specimen-bar">
        <span>Design preview</span>
        <span>Sample data</span>
      </div>
      <div class="flow">
        <div class="paper">
          <h3>Criteria</h3>
          <div class="row"><span>Platform</span><span>TikTok</span></div>
          <div class="row"><span>Niche</span><span>Fitness</span></div>
          <div class="row"><span>Audience</span><span>10K to 50K</span></div>
          <div class="row"><span>Engagement</span><span>Above 4%</span></div>
          <div class="row"><span>Location</span><span>Poland</span></div>
        </div>
        ARROWH
        <div class="paper">
          <h3>Shortlist, best fit first</h3>
          <ol class="rank">
            <li><span class="n">1</span><div><b>Creator A</b><span class="sub">38K followers, 7.2% engagement</span></div><div class="fit" role="img" aria-label="Fit 94 of 100"><i style="width:94%"></i></div></li>
            <li><span class="n">2</span><div><b>Creator B</b><span class="sub">21K followers, 6.1% engagement</span></div><div class="fit" role="img" aria-label="Fit 86 of 100"><i style="width:86%"></i></div></li>
            <li><span class="n">3</span><div><b>Creator C</b><span class="sub">46K followers, 4.8% engagement</span></div><div class="fit" role="img" aria-label="Fit 71 of 100"><i style="width:71%"></i></div></li>
            <li><span class="n">4</span><div><b>Creator D</b><span class="sub">12K followers, 4.3% engagement</span></div><div class="fit" role="img" aria-label="Fit 58 of 100"><i style="width:58%"></i></div></li>
          </ol>
        </div>
      </div>
    </div>''',
  actions='',
  story=[
   ('Why it exists', '<p>Building a shortlist by hand means hours of scrolling through profiles, checking audience size and engagement one creator at a time. The criteria are known before the search starts, so the search itself can be done by a tool.</p>'),
   ('Where it stands', '<p>This one is not finished. The preview above shows the result I am building toward: you set the platform, niche, audience size, engagement rate and location, and get back a ranked list with the best fit first.</p>')]),
]

def status(t):
    return f'<span class="status{" wip" if t["wip"] else ""}">{t["status"]}</span>'

# ---------- home ----------
rows = ''
for t in TOOLS:
    rows += f'''    <a class="entry" href="/{t['slug']}/">
      <h2>{t['a']} {ARROW} {t['b']}</h2>
      <p>{t['line']}</p>
      {status(t)}
    </a>
'''
home = head('Tools for influencer marketing by Yurii Hunko',
            'Four tools for the routine parts of influencer marketing: script drafts, campaign reports, reply triage and creator search.', '/') + f'''
<main class="wrap">

  <section class="intro">
    <h1>Four tools for the routine parts of influencer marketing.</h1>
    <p>Writing scripts, retyping stats from screenshots, sorting replies, scrolling for creators. I built a tool for each. Every one of them leaves the final call to a person.</p>
  </section>

  <section class="index" id="tools" aria-label="Tools">
{rows}  </section>

  <section class="reach" id="contact">
    <p>Questions? Write to me.</p>
    <a href="mailto:i@hunkoyura.com">i@hunkoyura.com</a>
  </section>

  <footer class="foot">© 2026 Yurii Hunko</footer>

</main>
''' + FOOT
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(home)

# ---------- tool pages ----------
for i,t in enumerate(TOOLS):
    nxt = TOOLS[(i+1)%len(TOOLS)]
    facts = ''.join(f'        <div><dt>{k}</dt><dd>{v}</dd></div>\n' for k,v in t['facts'])
    story = ''.join(f'''  <section class="story">
    <h2>{h}</h2>
    <div class="prose">{body}</div>
  </section>
''' for h,body in t['story'])
    page = head(f"{t['a']} to {t['b']}, a tool by Yurii Hunko", t['desc'], f"/{t['slug']}/") + f'''
<main class="wrap">

  <a class="back" href="/#tools"><svg class="arrow" aria-hidden="true"><use href="#arrow"/></svg> All tools</a>

  <section class="tool">
    <div class="tool-head">
      <h1>{t['a']} {ARROW} {t['b']}</h1>
      {status(t)}
    </div>
    <div class="tool-body">
      <p class="lede">{t['lede']}</p>
      <dl class="facts">
{facts}      </dl>
    </div>

{t['specimen'].replace('ARROWH', ARROW_H)}

{t['actions'].replace('ARROWH', ARROW_H)}
  </section>

{story}
  <a class="next" href="/{nxt['slug']}/">
    <span>Next tool</span>
    <strong>{nxt['a']} {ARROW} {nxt['b']}</strong>
  </a>

  <footer class="foot">© 2026 Yurii Hunko</footer>

</main>
''' + FOOT
    d = os.path.join(OUT, t['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(page)

# sitemap
urls = ['/'] + [f"/{t['slug']}/" for t in TOOLS]
open(os.path.join(OUT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>https://hunkoyura.com{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT,'robots.txt'),'w').write('User-agent: *\nAllow: /\n\nSitemap: https://hunkoyura.com/sitemap.xml\n')
print('built', len(TOOLS)+1, 'pages')
