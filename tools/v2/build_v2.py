"""Build index.html (the redesigned landing page, served at /) from index-old.html.

Usage: python tools/v2/build_v2.py [repo_dir]
The calendar demo, looks and admin are copied from index-old.html as they are, so any
change there reaches index.html by re-running this script (the git hooks in tools/v2/hooks do it).
"""
import re, sys, os
S = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(S))
src = open(os.path.join(W, 'index-old.html'), encoding='utf-8').read()
# the internal "Původní / Nová" switcher; True puts it back on both pages
SHOW_SWITCHER = False
css = open(os.path.join(S, 'v2.css'), encoding='utf-8').read().replace('.vz-switch', '.ver-switch')
logo = open(os.path.join(S, 'logo.svg'), encoding='utf-8').read().strip()
logo = re.sub(r'class="logo-svg"', 'class="v2-logo-svg"', logo)


def one(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:80])
    return s.replace(a, b)


# --- internal version switcher, shared by both pages (remove before publishing) ---
def switcher(active):
    if not SHOW_SWITCHER:
        return ''
    return ('<!-- INTERNAL: version switcher for comparing the landing page variants. Remove before publishing. -->\n'
            '<nav class="ver-switch" aria-label="Interní přepínač verzí" data-review-id="interni-prepinac-verzi"><span>Interní náhled</span>'
            '<a href="index.html" data-ver' + (' aria-current="page"' if active == 2 else '') + '>Nová</a>'
            '<a href="index-old.html" data-ver' + (' aria-current="page"' if active == 1 else '') + '>Původní</a></nav>\n'
            '<style>.ver-switch{position:fixed;left:14px;bottom:14px;z-index:95;display:flex;align-items:center;gap:4px;padding:4px 4px 4px 12px;border-radius:100px;background:rgba(10,10,10,.88);color:#fff;font:600 12.5px/1 system-ui,Arial,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.25)}'
            '.ver-switch span{opacity:.7;margin-right:6px}.ver-switch a{color:#fff;border:0;padding:7px 12px;border-radius:100px}.ver-switch a[aria-current]{background:#fff;color:#0a0a0a}'
            '@media print{.ver-switch{display:none}}</style>\n'
            '<script>document.querySelectorAll(".ver-switch a[data-ver]").forEach(function(a){a.addEventListener("click",function(){a.href=a.getAttribute("href").split("#")[0]+location.hash;});});</script>\n')


# the new page is index.html, served at /, so the old page is the one kept out of search
v1 = re.sub(r'<!-- INTERNAL: version switcher[\s\S]*?</script>\n', '', src)
v1 = one(v1, '\n</body>', '\n' + switcher(1) + '</body>')
if '<meta name="robots" content="noindex">' not in v1:
    v1 = re.sub(r'(<title>[^<]*</title>)', r'\1\n<meta name="robots" content="noindex">', v1, count=1)
open(os.path.join(W, 'index-old.html'), 'w', encoding='utf-8').write(v1)

s = re.sub(r'<!-- INTERNAL: version switcher[\s\S]*?</script>\n', '', src)
s = s.replace('<meta name="robots" content="noindex">\n', '')
s = one(s, '<link rel="preload" href="fonts/Inter-Variable-latin-ext.woff2"', '<link rel="preload" href="fonts/Satoshi-Variable.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="fonts/Inter-Variable-latin-ext.woff2"')
s = one(s, '\n</head>', '\n' + css + '</head>')

# --- hero: top bar + header replaced ---
a = s.index('<div class="top-bar"')
b = s.index('</header>', a) + len('</header>')
old = s[a:b]
h1 = re.search(r'<h1>([\s\S]*?)</h1>', old).group(1)
sub = re.search(r'<p class="subtitle">([\s\S]*?)</p>', old).group(1)
# v2 headline names the product: 'i své' gives way to 'adventním kalendářem'
h1, nh = re.subn(r'Letos obdarujte i[\s ]+své zákazníky\.', 'Letos obdarujte zákazníky <span class="v2-mark">adventním kalendářem</span>.', h1)
assert nh == 1, h1[-200:]
SHOTS = [('fotoskoda', 'Dům s okny', 's1', '--x:-8%;--y:30px;--w:250px;--r:-7deg;--d:7s'),
         ('chata', 'Zasněžená chalupa', 's2', '--x:-3%;--y:420px;--w:214px;--r:5deg;--d:8.5s;--dl:-3s'),
         ('hracky', 'Santova dílna', 's3', '--xr:-8%;--y:50px;--w:240px;--r:6deg;--d:7.5s;--dl:-1.5s'),
         ('snehulak', 'Sněhulák a sobi', 's4', '--xr:-3%;--y:430px;--w:214px;--r:-5deg;--d:9s;--dl:-4.5s')]
# captions follow the look picker, so renaming a look there renames its hero preview too
def caption(k, fallback):
    m = re.search(r'data-theme="%s"[^>]*aria-label="([^"]*)"' % k, src)
    return m.group(1) if m else fallback


SHOTS = [(k, caption(k, cap), c, st) for k, cap, c, st in SHOTS]
shots = '\n'.join('      <a class="v2-shot %s" href="#ukazka" data-vzhled="%s" style="%s" aria-label="Ukázka vzhledu %s"><img src="img/hero/%s.webp" alt="" width="520" height="650" decoding="async"><span>%s</span></a>' % (c, k, st, cap, k, cap) for k, cap, c, st in SHOTS)
spark = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z"/></svg>'
links = ''.join('<a href="#%s">%s</a>' % x for x in [('ukazka', 'Vzhledy'), ('administrace', 'Administrace'), ('postup', 'Jak to probíhá'), ('srovnani', 'Proč my'), ('aplikace', 'Aplikace na míru')])
hero = ('<header class="v2-hero" data-review-id="header">\n'
        '  <div class="v2-stage">\n    <div class="v2-shots">\n' + shots + '\n    </div>\n'
        '    <span class="v2-spark" style="left:21%;top:70px" aria-hidden="true">' + spark + '</span>\n'
        '    <span class="v2-spark" style="right:22%;top:400px;animation-delay:-1.4s" aria-hidden="true">' + spark + '</span>\n'
        '    <span class="v2-spark" style="left:23%;top:660px;width:16px;height:16px;animation-delay:-2.2s" aria-hidden="true">' + spark + '</span>\n'
        '    <div class="v2-copy">\n      <h1>' + h1 + '</h1>\n      <p class="v2-sub">' + sub + '</p>\n'
        '      <div class="v2-ctas"><a class="v2-btn primary" href="#ukazka" data-review-id="da-ukazka">Prohlédnout vzhledy</a><a class="v2-btn ghost" href="#kontakt" data-review-id="hero-kontakt">Chci kalendář na míru →</a></div>\n'
        '      <p class="v2-proof"><span>Vlastní design</span><span>+10&nbsp;% obratu v prosinci</span><span>Bez licencí</span></p>\n'
        '    </div>\n  </div>\n</header>')
s = s[:a] + hero + s[b:]
navbar = ('<div class="v2-navbar" id="v2-navbar" data-review-id="sticky-nav"><div class="v2-nav"><a class="v2-logo" href="#" aria-label="PragueBest, na začátek">' + logo + '</a>\n'
          '    <nav class="v2-links" aria-label="Sekce stránky">' + links + '</nav>\n'
          '    <a class="v2-btn dark sm" href="#kontakt" data-review-id="nav-kontakt">Chci kalendář</a></div><i class="v2-prog" id="v2-prog" aria-hidden="true"></i></div>\n')
s = one(s, '<div class="container">\n', '<div class="container">\n' + navbar)

# --- comparison: the table becomes two plan cards, ours bigger and darker ---
t0 = s.index('<div class="table-wrap cmp-wrap"')
t1 = s.index('</table>', t0)
t1 = s.index('</div>', t1) + len('</div>')
rows = re.findall(r'<tr><td>([^<]*)</td><td[^>]*>([^<]*)</td><td class="us"[^>]*>([^<]*)</td></tr>', s[t0:t1])
assert len(rows) == 6, rows
x = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
ok = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
box = ''.join('<li>' + x + '<span><b>' + r[0] + '</b>' + r[1] + '</span></li>' for r in rows)
us = ''.join('<li>' + ok + '<span><b>' + r[0] + '</b>' + r[2] + '</span></li>' for r in rows)
cmp = ('<div class="v2-cmp" data-review-id="tabulka-srovnani">\n'
       '    <div class="v2-plan box"><h3>Krabicová SaaS služba</h3><ul>' + box + '</ul></div>\n'
       '    <div class="v2-plan us"><span class="v2-plan-tag">Doporučujeme</span><h3>Kalendář od PragueBest</h3><ul>' + us + '</ul><a class="v2-btn primary" href="#kontakt">Chci kalendář na míru</a></div>\n'
       '  </div>')
s = s[:t0] + cmp + s[t1:]

# --- tip cards: the bold lead is its own line, so drop the joining comma or dash after it ---
def _tip(m):
    rest = m.group(2)
    return m.group(1) + rest[:1].upper() + rest[1:]
u0 = s.index('<ul class="dots cols tip-list"')
u1 = s.index('</ul>', u0)
s = s[:u0] + re.sub(r'(</strong>)\s*[,\-–]\s*(\S)', lambda m: m.group(1) + m.group(2).upper(), s[u0:u1]) + s[u1:]
# --- tech window: no "window no. 25" story ---
s, nk = re.subn(r'<span>okénko č\.[\s ]*25[\s ]*·[\s ]*pod kapotou</span>', '<span>pod kapotou</span>', s)
assert nk == 1
s = one(s, '<span class="num">25</span>', '')
s, nc = re.subn(r'\n\s*<p class="xwin-cap">[^<]*</p>', '', s)
assert nc == 1
# --- PragueBest line icons (black with a pink accent) instead of numbers and generic glyphs ---
def ico(name):
    return '<img class="v2-ico" src="img/icons/' + name + '.svg" alt="" width="56" height="56" decoding="async">'
for name, start in [('hra', '<div class="perk"><h3>Hravost'), ('design', '<div class="perk"><h3>Vlastní design'), ('mereni', '<div class="perk"><h3>Měření'), ('kod', '<div class="perk"><h3>Funkce')]:
    s = one(s, start, start.replace('<div class="perk">', '<div class="perk v2-has-ico">' + ico(name)))
s = one(s, '<div class="callout" data-review-id="callout-vcas">', '<div class="callout v2-has-ico" data-review-id="callout-vcas">' + ico('raketa'))
s = one(s, '<div class="callout ok" data-review-id="callout-nejen-advent">', '<div class="callout ok v2-has-ico" data-review-id="callout-nejen-advent">' + ico('rok'))
s = one(s, '<div class="offer-card" data-review-id="nabidka-vyvoj">', '<div class="offer-card v2-has-ico" data-review-id="nabidka-vyvoj">' + ico('vyvoj'))
s = one(s, '<div class="offer-card" data-review-id="nabidka-audit">', '<div class="offer-card v2-has-ico" data-review-id="nabidka-audit">' + ico('audit'))
# --- 'we build contests and campaign pages too' belongs to custom apps, not the comparison ---
m = re.search(r'\n\s*<p>Stejně postavíme i[\s\S]*?</p>', s)
assert m and s.index('<section id="srovnani"') < m.start() < s.index('<section id="okenko"')
veta = m.group(0).strip().replace('<p>', '<p class="v2-tez">', 1)
s = s[:m.start()] + s[m.end():]
k = s.index('<section id="aplikace"')
e = s.index('</section>', k)
s = s[:e] + '  ' + veta + '\n' + s[e:]
# --- the hint above the look picker is redundant in v2 ---
s, nh = re.subn(r'\n\s*<p>Přepněte vzhled a(?:&nbsp;|\s)porovnejte je\. Dnešní okénko svítí\.</p>', '', s)
assert nh == 1
# --- drop eyebrow labels above headings ---
s, n = re.subn(r'\n\s*<span class="section-label">[^<]*</span>', '', s)
assert n == 8, n
# --- contact: the label becomes the heading, plus the two calls to action ---
s = one(s, '  <div class="keybox" data-review-id="cta">\n    <span class="label">Další krok</span>', '  <h2>Další <span class="accent">krok</span></h2>\n  <div class="keybox" data-review-id="cta">')
k = s.index('<section id="kontakt"')
e = s.index('</section>', k)
s = s[:e] + '  <div class="v2-ctas"><a class="v2-btn primary" href="mailto:produktaci@praguebest.cz">Napsat PragueBest</a><a class="v2-btn ghost" href="#ukazka">Prohlédnout vzhledy</a></div>\n' + s[e:]
f0 = s.index('<footer class="doc-footer" data-review-id="footer">')
f1 = s.index('</footer>', f0)
s = s[:f0] + '<footer class="doc-footer" data-review-id="footer">\n  <a class="v2-logo" href="#obsah" aria-label="PragueBest">' + logo + '</a>\n  <p>©2026 – S\u00a0láskou ke klientům <span class="v2-heart" aria-label="srdce">♥</span> vytvořilo studio <a href="https://www.praguebest.cz/">PragueBest</a></p>\n' + s[f1:]

# --- layered snow canvas ---
snow = r'''<canvas class="v2-snow" id="v2-snow" aria-hidden="true"></canvas>
<script>
// Layered snow and gold sparks: far, mid and near layers with their own size, speed and sway.
(function () {
  var c = document.getElementById('v2-snow');
  if (!c || !c.getContext || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  var x = c.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2), W = 0, H = 0, flakes = [], run = true;
  var LAYERS = [{ n: 34, r: [1, 2], v: [12, 22], a: .55 }, { n: 22, r: [2.2, 3.4], v: [24, 38], a: .7 }, { n: 9, r: [4.5, 7], v: [40, 58], a: .9 }];
  var COLORS = ['#ffffff', '#ffffff', '#c9a227', '#e30613'];
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function resize() {
    W = innerWidth; H = innerHeight; c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    var k = Math.max(.45, Math.min(1.2, W / 1280));
    flakes = [];
    LAYERS.forEach(function (L, li) {
      for (var i = 0; i < Math.round(L.n * k); i++) flakes.push({ x: rnd(0, W), y: rnd(-H, H), r: rnd(L.r[0], L.r[1]), v: rnd(L.v[0], L.v[1]), a: L.a, ph: rnd(0, 6.28), sw: rnd(8, 22) * (li + 1) / 2, col: COLORS[(Math.random() * COLORS.length) | 0], star: li === 2 && Math.random() < .5 });
    });
  }
  function star(f, px) {
    x.beginPath();
    for (var i = 0; i < 8; i++) { var ang = i * Math.PI / 4, rr = i % 2 ? f.r * .38 : f.r; x.lineTo(px + Math.cos(ang) * rr, f.y + Math.sin(ang) * rr); }
    x.closePath(); x.fill();
  }
  var last = 0;
  function frame(t) {
    if (!run) return;
    var dt = Math.min(.05, (t - last) / 1000 || 0); last = t;
    x.clearRect(0, 0, W, H);
    for (var i = 0; i < flakes.length; i++) {
      var f = flakes[i]; f.y += f.v * dt; f.ph += dt * .8;
      if (f.y > H + 10) { f.y = -10; f.x = rnd(0, W); }
      var px = f.x + Math.sin(f.ph) * f.sw;
      x.globalAlpha = f.col === '#e30613' ? f.a * .35 : f.col === '#c9a227' ? f.a * .55 : f.a;
      x.fillStyle = f.col;
      if (f.col === '#ffffff') { x.shadowColor = 'rgba(120,90,60,.35)'; x.shadowBlur = 3; } else x.shadowBlur = 0;
      if (f.star) star(f, px); else { x.beginPath(); x.arc(px, f.y, f.r, 0, 6.283); x.fill(); }
    }
    requestAnimationFrame(frame);
  }
  resize(); addEventListener('resize', resize);
  document.addEventListener('visibilitychange', function () { run = !document.hidden; if (run) requestAnimationFrame(function (t) { last = t; frame(t); }); });
  requestAnimationFrame(function (t) { last = t; frame(t); });
})();
</script>
'''
pick = """<script>
// Sticky bar: solid background once the page scrolls, reading progress and the current section.
(function () {
  var bar = document.getElementById('v2-navbar'), prog = document.getElementById('v2-prog'), links = [].slice.call(bar.querySelectorAll('.v2-links a'));
  var secs = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  function on() {
    var y = scrollY, h = document.documentElement.scrollHeight - innerHeight, cur = -1;
    bar.classList.toggle('is-stuck', y > 30);
    prog.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    secs.forEach(function (sec, i) { if (sec && sec.getBoundingClientRect().top < innerHeight * 0.35) cur = i; });
    links.forEach(function (a, i) { a.classList.toggle('is-on', i === cur); });
  }
  addEventListener('scroll', on, { passive: true }); addEventListener('resize', on); on();
})();
// Hero previews: clicking one selects that look in the demo below and scrolls to it.
document.querySelectorAll('.v2-shot[data-vzhled]').forEach(function (a) {
  a.addEventListener('click', function (e) {
    var b = document.querySelector('button[data-theme="' + a.getAttribute('data-vzhled') + '"]');
    if (!b) return;
    e.preventDefault(); b.click();
    var klid = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.getElementById('ukazka').scrollIntoView({ behavior: klid ? 'auto' : 'smooth', block: 'start' });
    history.replaceState(null, '', '#ukazka');
  });
});
</script>
"""
s = one(s, '\n</body>', '\n' + pick + snow + switcher(2) + '</body>')
open(os.path.join(W, 'index.html'), 'w', encoding='utf-8').write(s)
print('ok', len(s))
