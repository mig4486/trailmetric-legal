from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).parent
PAGES = json.loads((ROOT / 'content.json').read_text(encoding='utf-8-sig'))
BASE = 'https://mig4486.github.io/trailmetric-legal/'
LABELS = {'en': ['Privacy', 'Terms', 'Support'], 'ru': ['Конфиденциальность', 'Условия', 'Поддержка']}

def render(lang, page=None):
    prefix = '../' if lang == 'ru' else ''
    doc = page[lang] if page else None
    title = doc['title'] if doc else ('Support & legal' if lang == 'en' else 'Поддержка и документы')
    slug = page['slug']+'.html' if page else 'index.html'
    alt = '../'+slug if lang == 'ru' else 'ru/'+slug
    canonical = BASE + ('ru/' if lang == 'ru' else '') + slug
    nav = ''.join(f'<a href="{p["slug"]}.html"'+(' aria-current="page"' if p==page else '')+f'>{label}</a>' for p,label in zip(PAGES,LABELS[lang]))
    if doc:
        toc_title = 'On this page' if lang == 'en' else 'На этой странице'
        toc = ''.join(f'<li><a href="#section-{i}">{escape(h)}</a></li>' for i,(h,_) in enumerate(doc['sections'],1))
        body = '<aside class="toc"><h2>'+toc_title+'</h2><ol>'+toc+'</ol></aside>'
        body += ''.join(f'<section id="section-{i}"><h2>{escape(h)}</h2><p>{text}</p></section>' for i,(h,text) in enumerate(doc['sections'],1))
        intro = doc['intro']
    else:
        intro = 'Your activity. Your data.' if lang == 'en' else 'Ваши активности. Ваши данные.'
        descriptions = ['How location, sensors, health exports and support messages are handled.', 'App Store licence, responsible use and your rights.', 'Recording, maps, Bluetooth sensors and contacting us.'] if lang == 'en' else ['Геопозиция, датчики, экспорт здоровья и обращения в поддержку.', 'Лицензия App Store, безопасное использование и ваши права.', 'Запись, карты, Bluetooth-датчики и связь с нами.']
        body = '<div class="cards">'+''.join(f'<a class="card" href="{p["slug"]}.html"><h2>{label}<span aria-hidden="true"> ↗</span></h2><p>{text}</p></a>' for p,label,text in zip(PAGES,LABELS[lang],descriptions))+'</div>'
        body += '<section><h2>'+('Need help?' if lang=='en' else 'Нужна помощь?')+'</h2><p><a class="contact" href="mailto:tgstartup@icloud.com">tgstartup@icloud.com</a></p></section>'
    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · TrailMetric</title><meta name="description" content="{escape(intro,quote=True)}">
<meta name="color-scheme" content="dark light"><link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{BASE+slug}"><link rel="alternate" hreflang="ru" href="{BASE+'ru/'+slug}">
<link rel="stylesheet" href="{prefix}style.css"><link rel="icon" type="image/svg+xml" href="{prefix}mark.svg"></head>
<body><a class="skip" href="#main">{"Skip to content" if lang=="en" else "К содержанию"}</a>
<header><div class="top"><a class="brand" href="index.html"><img src="{prefix}mark.svg" alt="" width="36" height="36"><span>TrailMetric</span></a><a class="language" href="{alt}" lang="{'en' if lang=='ru' else 'ru'}">{'English' if lang=='ru' else 'Русский'}</a></div>
<nav aria-label="{'Documents' if lang=='en' else 'Документы'}">{nav}</nav></header>
<main id="main"><p class="eyebrow">{"SUPPORT & LEGAL" if lang=='en' else "ПОДДЕРЖКА И ДОКУМЕНТЫ"}</p><h1>{escape(title)}</h1><p class="intro">{escape(intro)}</p>{body}</main>
<footer><p>© 2026 Tigran Gevorgyan · TrailMetric</p><p><a href="mailto:tgstartup@icloud.com">tgstartup@icloud.com</a></p><p><a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Apple Standard EULA</a> · <a href="privacy.html">{LABELS[lang][0]}</a></p></footer></body></html>'''
    folder = ROOT/'ru' if lang == 'ru' else ROOT
    folder.mkdir(exist_ok=True)
    (folder/slug).write_text(html,encoding='utf-8')

for language in ['en','ru']:
    render(language)
    for page in PAGES:
        render(language,page)
(ROOT/'.nojekyll').touch()
print('Generated 8 HTML pages.')

