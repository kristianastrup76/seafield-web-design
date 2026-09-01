"""
Regenerates export/index.html from Main.dc.html (the design-canvas source).

Run this after any edit to Main.dc.html, then copy export/index.html over
index.html to publish:

    python3 build_index.py
    cp export/index.html index.html

The two HEAD blobs below (SEO/meta/analytics tags) live outside the design
canvas on purpose — they're not visual page content, so they don't belong in
Main.dc.html. Keeping them here, versioned, is what keeps this build step
from silently dropping them the way earlier direct edits to index.html did.
"""
import export_template as et

TITLE = "Seafield Web Design — Affordable websites for small businesses"
DESCRIPTION = "Fast, affordable, fixed-price websites for small businesses without one yet. Based in Fife, working across the UK."
DEFAULT_ACCENT = "#1c6e6a"

# Emitted right after the viewport meta: Google tag, title, description,
# canonical, Search Console verification, Open Graph + Twitter Card tags.
HEAD_EARLY = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18420338071"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-18420338071');
</script>
<title>Seafield Web Design — Affordable websites for small businesses</title>
<meta name="description" content="Fast, affordable, fixed-price websites for small businesses without one yet. Based in Fife, working across the UK.">
<link rel="canonical" href="https://seafieldwebdesign.co.uk/">
<meta name="google-site-verification" content="wNmIG83H9pTmOrHUT0hmplxtVUIGQHx5pZg4r1EUfCw" />
<meta property="og:type" content="website">
<meta property="og:site_name" content="Seafield Web Design">
<meta property="og:title" content="Seafield Web Design — Affordable websites for small businesses">
<meta property="og:description" content="Fast, affordable, fixed-price websites for small businesses without one yet. Based in Fife, working across the UK.">
<meta property="og:url" content="https://seafieldwebdesign.co.uk/">
<meta property="og:image" content="https://seafieldwebdesign.co.uk/homepage-hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Seafield Web Design — Affordable websites for small businesses">
<meta name="twitter:description" content="Fast, affordable, fixed-price websites for small businesses without one yet. Based in Fife, working across the UK.">
<meta name="twitter:image" content="https://seafieldwebdesign.co.uk/homepage-hero.jpg">
""".strip()

# Emitted after the Google Fonts link: the two JSON-LD structured-data blocks.
HEAD_LATE = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Seafield Web Design",
  "description": "Fast, affordable, fixed-price websites for small businesses without one yet. Based in Fife, working across the UK.",
  "url": "https://seafieldwebdesign.co.uk/",
  "email": "contact@seafieldwebdesign.co.uk",
  "areaServed": [
    "Kirkcaldy", "Dunfermline", "Glenrothes", "St Andrews", "Edinburgh", "Fife", "United Kingdom"
  ],
  "address": {
    "@type": "PostalAddress",
    "addressRegion": "Fife",
    "addressCountry": "GB"
  },
  "priceRange": "£149-£649",
  "sameAs": [
    "https://facebook.com/seafieldwebdesign",
    "https://instagram.com/seafieldwebdesign"
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do I need to buy my own domain name, or do you do that?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We handle it for you. Domain registration is included as part of your website package — we register a fitting .co.uk (or .com) address for your business and point it at your new site, so it's one less thing you need to sort out yourself."
      }
    },
    {
      "@type": "Question",
      "name": "Do I get a professional email address (e.g. info@mybusiness.co.uk)?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes — we can set up a professional email address on your own domain (like info@yourbusiness.co.uk) alongside your website, so you're not stuck sending business emails from a personal Gmail or Hotmail address."
      }
    },
    {
      "@type": "Question",
      "name": "What happens if I want to update text or photos later?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Every package includes one round of small text and photo swaps after launch, at no extra cost. Beyond that — a bigger redesign, new pages, that sort of thing — we're happy to help, billed simply by the hour rather than another fixed fee."
      }
    },
    {
      "@type": "Question",
      "name": "Who owns the website?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "You do — outright. The domain, the design, the content and the hosting account are all yours. The £18/month hosting fee keeps everything online, secure and backed up, but the site itself belongs to you, not us."
      }
    }
  ]
}
</script>
""".strip()

if __name__ == "__main__":
    et.convert(
        "Main.dc.html",
        "export/index.html",
        TITLE,
        DESCRIPTION,
        DEFAULT_ACCENT,
        prop_name="accentTeal",
        extra_head=HEAD_EARLY,
        extra_head_late=HEAD_LATE,
    )
