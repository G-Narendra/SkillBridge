import requests
import re

r = requests.get('http://localhost:3000')
print('Status:', r.status_code)
html = r.text
print('HTML Length:', len(html))

# Find all links and scripts
links = re.findall(r'<link[^>]+>', html)
for l in links:
    print('LINK:', l)

css_links = re.findall(r'href=[\"\']([^\"\']+\.css[^\"\']*)[\"\']', html)
print('CSS hrefs found:', css_links)
for href in css_links:
    full_url = 'http://localhost:3000' + href if href.startswith('/') else href
    res = requests.get(full_url)
    print('CSS URL:', full_url, 'Status:', res.status_code, 'Bytes:', len(res.text))
    if len(res.text) > 0:
        print('CSS Content (first 300 chars):', res.text[:300])

if not css_links:
    print('WARNING: NO CSS LINKS FOUND IN HTML!')
    print('Head section of HTML:')
    head_m = re.search(r'<head>(.*?)</head>', html, re.DOTALL)
    if head_m:
        print(head_m.group(1)[:1500])
