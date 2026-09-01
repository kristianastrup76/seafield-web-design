import re, sys, json

def convert(src_path, out_path, title, description, default_color, prop_name="accentColor", extra_head="", extra_head_late=""):
    s = open(src_path, encoding='utf-8').read()

    # Extract the fonts link + style block from helmet
    helmet_match = re.search(r'<helmet>(.*?)</helmet>', s, re.S)
    helmet = helmet_match.group(1)
    fonts_link = re.search(r'(<link rel="preconnect".*?>\s*<link href="https://fonts\.googleapis\.com.*?>)', helmet, re.S).group(1)
    style_match = re.search(r'(<style>.*?</style>)', helmet, re.S).group(1)

    # Extract main content div (between </helmet> and </x-dc>)
    content_match = re.search(r'</helmet>\s*(.*?)\s*</x-dc>', s, re.S)
    content = content_match.group(1)

    # Replace template holes with literal default color
    content = content.replace('{{' + prop_name + '}}', default_color)
    content = content.replace('--accent: ' + '{{' + prop_name + '}}' + ';', f'--accent: {default_color};')

    # extra_head / extra_head_late carry page-specific SEO/meta/analytics tags
    # (Google tag, title/description, canonical, og/twitter, JSON-LD, etc.)
    # that aren't part of the design canvas itself. extra_head is emitted
    # right after the viewport meta (Google tag, title, description,
    # canonical, verification, OG/Twitter); extra_head_late after the fonts
    # link (JSON-LD blocks), matching where the live page carries them. When
    # omitted, falls back to a plain <title>/<meta description> pair so this
    # script still works for pages that don't need the extra tags.
    head_extra = extra_head.strip() if extra_head.strip() else (
        f'<title>{title}</title>\n<meta name="description" content="{description}">'
    )
    head_extra_late = f'\n{extra_head_late.strip()}' if extra_head_late.strip() else ''

    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_extra}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{fonts_link}{head_extra_late}
{style_match}
</head>
<body>
{content}
<script>
(function () {{
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {{
    els.forEach(function (el) {{ el.classList.add('is-visible'); }});
    return;
  }}
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (entry) {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }}
    }});
  }}, {{ threshold: 0.15, rootMargin: '0px 0px -40px 0px' }});
  els.forEach(function (el) {{ io.observe(el); }});

  // Deep-link fix: loading the page directly at a section anchor (e.g.
  // /#pricing) can scroll the browser to that section before or after this
  // script runs, so the IntersectionObserver's first check can miss
  // elements that are actually already on screen at first paint, leaving
  // them stuck invisible until the user scrolls. Do an explicit sweep once
  // the page (and any hash scroll) has settled, and reveal anything that's
  // already in view immediately rather than waiting on a scroll event.
  function isInViewport(el) {{
    var rect = el.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight;
    return rect.top < vh - 40 && rect.bottom > 0;
  }}
  function settleReveal() {{
    els.forEach(function (el) {{
      if (!el.classList.contains('is-visible') && isInViewport(el)) {{
        el.classList.add('is-visible');
        io.unobserve(el);
      }}
    }});
  }}
  settleReveal();
  window.addEventListener('load', function () {{
    requestAnimationFrame(function () {{ requestAnimationFrame(settleReveal); }});
  }});
  if (window.location.hash) {{
    setTimeout(settleReveal, 50);
    setTimeout(settleReveal, 300);
  }}
}})();
</script>
</body>
</html>
'''
    open(out_path, 'w', encoding='utf-8').write(out)
    print("wrote", out_path)

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
