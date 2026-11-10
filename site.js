(function(){
  /* theme toggle */
  var root = document.documentElement;
  var toggle = document.getElementById('theme-toggle');
  function current(){
    var t = root.getAttribute('data-theme');
    if (t === 'light' || t === 'dark') return t;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  function label(){
    if (!toggle) return;
    var other = current() === 'light' ? 'dark' : 'light';
    toggle.textContent = other === 'light' ? 'Light' : 'Dark';
    toggle.setAttribute('aria-label', 'Switch to ' + other + ' theme');
  }
  if (toggle){
    toggle.addEventListener('click', function(){
      var next = current() === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      label();
    });
    label();
  }

  /* demos */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function swap(el, html){
    if (reduce || !el.innerHTML){ el.innerHTML = html; return; }
    el.classList.add('out');
    setTimeout(function(){ el.innerHTML = html; el.classList.remove('out'); }, 160);
  }
  function press(group, btn){
    group.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
  }

  /* Brief to Script */
  var scriptOut = document.getElementById('script-out');
  if (scriptOut){
    var scripts = {
      calm: {
        tone: 'Calm, talks to camera',
        beats: [
          ['0:00', 'Hook', 'I stopped buying water on the go a while back. This is why.', 'No more plastic bottles'],
          ['0:04', 'Body', 'This is Pebble. I fill it at home in the morning and it is still cold when I head back in the evening.', 'Cold all day'],
          ['0:16', 'Proof', 'I left it in the car at noon on purpose. The ice was still there at six.', 'Ice at 6 pm'],
          ['0:24', 'CTA', 'Code MILA gets you a discount. The link is in my bio.', 'Code MILA']
        ],
        caption: 'Cold water from morning to evening. Code MILA. #ad #pebblepartner'
      },
      fast: {
        tone: 'Fast, jump cuts',
        beats: [
          ['0:00', 'Hook', 'Warm water in your bag? No. Here is the fix.', 'The fix'],
          ['0:03', 'Body', 'Pebble. Fill it, close it, throw it in. Gym, desk, train, still cold.', 'Gym. Desk. Train.'],
          ['0:14', 'Proof', 'Ice in at eight. Ice still there at six. I checked.', '8 am to 6 pm'],
          ['0:23', 'CTA', 'Code MILA, link in bio, go.', 'Code MILA']
        ],
        caption: 'Tested it so you do not have to. Code MILA. #ad #pebblepartner'
      },
      dry: {
        tone: 'Dry humor',
        beats: [
          ['0:00', 'Hook', 'My emotional support bottle has a name now.', 'Meet Pebble'],
          ['0:04', 'Body', 'It does one thing. It keeps water cold. That makes it more reliable than most of my plans.', 'Does one thing'],
          ['0:15', 'Proof', 'I forgot it in the car all afternoon. It handled that better than I did.', 'Still cold'],
          ['0:24', 'CTA', 'Code MILA, if you also want a bottle that has its life together.', 'Code MILA']
        ],
        caption: 'The most stable thing I own. Code MILA. #ad #pebblepartner'
      }
    };
    var toneEcho = document.getElementById('tone-echo');
    var renderScript = function(key){
      var s = scripts[key];
      swap(scriptOut, s.beats.map(function(b){
        return '<div class="beat"><div class="when"><b>' + b[1] + '</b>' + b[0] + '</div>' +
               '<div><div class="say">' + b[2] + '</div><span class="screen">On screen: ' + b[3] + '</span></div></div>';
      }).join('') + '<p class="note">Caption: ' + s.caption + '</p>');
      toneEcho.textContent = s.tone;
    };
    var stylePicker = document.getElementById('style-picker');
    stylePicker.addEventListener('click', function(e){
      var b = e.target.closest('button'); if (!b) return;
      press(stylePicker, b); renderScript(b.dataset.style);
    });
    renderScript('calm');
  }

  /* Post to Report */
  var shotIn = document.getElementById('shot-in'), shotOut = document.getElementById('shot-out');
  if (shotIn && shotOut){
    var shots = {
      clean: {
        who: 'Creator A, Reel',
        rows: [['Views','48,200'],['Reach','31,900'],['Likes','3,410'],['Comments','126'],['Shares','284'],['Saves','512']],
        bad: [], held: false,
        title: 'Passed. Added to the campaign report.',
        notes: ['Engagement rate 13.6% of reach']
      },
      odd: {
        who: 'Creator B, Reel',
        rows: [['Views','12,400'],['Reach','9,800'],['Likes','18,900'],['Comments','84'],['Shares','140'],['Saves','210']],
        bad: ['Likes'], held: true,
        title: 'Held for manual review. Not in the report yet.',
        notes: ['Likes are higher than views, likely a misread', 'Engagement rate 197% of reach, not physically possible']
      }
    };
    var renderShot = function(key){
      var s = shots[key];
      swap(shotIn, '<div class="who"><i></i>' + s.who + '</div>' + s.rows.map(function(r){
        return '<div class="line"><span>' + r[0] + '</span><b>' + r[1] + '</b></div>';
      }).join(''));
      swap(shotOut, '<div class="metrics">' + s.rows.map(function(r){
        return '<div' + (s.bad.indexOf(r[0]) > -1 ? ' class="bad"' : '') + '><span>' + r[0] + '</span><b>' + r[1] + '</b></div>';
      }).join('') + '</div>' +
      '<div class="verdict' + (s.held ? ' held' : '') + '"><svg aria-hidden="true"><use href="#' + (s.held ? 'hold' : 'ok') + '"/></svg>' +
      '<div><strong>' + s.title + '</strong><ul>' + s.notes.map(function(n){ return '<li>' + n + '</li>'; }).join('') + '</ul></div></div>');
    };
    var shotPicker = document.getElementById('shot-picker');
    shotPicker.addEventListener('click', function(e){
      var b = e.target.closest('button'); if (!b) return;
      press(shotPicker, b); renderShot(b.dataset.shot);
    });
    renderShot('clean');
  }

  /* Inbox to Triage */
  var mailList = document.getElementById('mails'), mailOut = document.getElementById('mail-out');
  if (mailList && mailOut){
    var mails = [
      { from: 'Anna', text: 'Sounds great, I am in. When do you need the first draft?',
        cat: 'Interested', pri: 'High priority', found: 'Asks for the draft deadline',
        draft: 'Hi Anna, glad you are in. I will send the brief today. The first draft is due <em>deadline needed from you</em>.',
        end: 'Draft saved in Gmail, logged to the sheet. Not sent.' },
      { from: 'Tomas', text: 'My rate for a 30 second TikTok is 400 EUR, usage rights are extra.',
        cat: 'Negotiating', pri: 'High priority', found: 'Price 400 EUR per video. Usage rights not included',
        draft: 'Hi Tomas, thanks for the rate. Before I confirm, could you tell me what usage rights would add for <em>term needed from you</em>?',
        end: 'Draft saved in Gmail, logged to the sheet. Not sent.' },
      { from: 'Ines', text: 'Thanks for thinking of me, but I am fully booked until spring.',
        cat: 'Declined', pri: 'Low priority', found: 'Booked until spring',
        draft: '', end: 'Logged to the sheet only. No draft, no extra API call.' },
      { from: 'Growth Team', text: 'Boost your followers fast!!! Limited offer inside',
        cat: 'Spam', pri: 'No priority', found: 'Nothing relevant',
        draft: '', end: 'Logged to the sheet only. No draft, no extra API call.' }
    ];
    mailList.innerHTML = mails.map(function(m, i){
      return '<button type="button" aria-pressed="' + (i === 0) + '" data-i="' + i + '"><b>' + m.from + '</b><span>' + m.text + '</span></button>';
    }).join('');
    var renderMail = function(i){
      var m = mails[i];
      swap(mailOut,
        '<div class="tagline"><span class="tag">' + m.cat + '</span><span class="tag soft">' + m.pri + '</span></div>' +
        '<div class="row" style="border-top:0"><span>Message</span><span>' + m.text + '</span></div>' +
        '<div class="row"><span>Pulled out</span><span>' + m.found + '</span></div>' +
        (m.draft ? '<div class="draft"><small>Draft reply</small>' + m.draft + '</div>' : '') +
        '<p class="note">' + m.end + '</p>');
    };
    mailList.addEventListener('click', function(e){
      var b = e.target.closest('button'); if (!b) return;
      press(mailList, b); renderMail(+b.dataset.i);
    });
    renderMail(0);
  }
})();
