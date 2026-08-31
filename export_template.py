import re, sys, json

def convert(src_path, out_path, title, description, default_color, prop_name="accentColor"):
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

    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{fonts_link}
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
}})();
</script>
</body>
</html>
'''
    open(out_path, 'w', encoding='utf-8').write(out)
    print("wrote", out_path)

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
