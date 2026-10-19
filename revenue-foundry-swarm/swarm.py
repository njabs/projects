"""Revenue Foundry: bounded recursive worker spawning, read-only GitHub discovery."""
import concurrent.futures as futures
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

MAX_WORKERS = min(12, max(1, int(os.getenv('RF_MAX_WORKERS', '4'))))
MAX_TASKS = 36
QUERIES = ['is:issue is:open "bounty" "$100"', 'is:issue is:open "bounty" "$200"', 'is:issue is:open "bounty" "typescript"', 'is:issue is:open "paid" "react"']
HEADERS = {'Accept': 'application/vnd.github+json', 'User-Agent': 'RevenueFoundry/0.2'}
if os.getenv('GITHUB_TOKEN'):
    HEADERS['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']

def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=18) as resp:
            return json.load(resp)
    except Exception as exc:
        return {'error': str(exc)}

def hunt(q):
    args = urllib.parse.urlencode({'q': q, 'per_page': 20, 'sort': 'updated'})
    result = fetch('https://api.github.com/search/issues?' + args)
    return result.get('items', []), result.get('error')

def assess(issue):
    title = issue.get('title', '')
    body = issue.get('body') or ''
    text = title + '\n' + body
    match = re.search(r'(?:\$|USD\s*)([1-9][0-9,]{1,6})\b', text, re.I)
    if not match or not re.search(r'\b(bounty|reward|paid)\b', text, re.I):
        return None
    amount = int(match.group(1).replace(',', ''))
    if amount < 25 or issue.get('pull_request') or issue.get('state') != 'open':
        return None
    if re.search(r'\b(CVE-\d+|exploit|malware)\b', title, re.I):
        return None
    return {'title': title[:180], 'url': issue.get('html_url'), 'advertised_usd': amount,
            'comments': issue.get('comments', 0), 'funding_verified': False,
            'south_africa_eligible': None, 'payment_verified': False,
            'status': 'UNVERIFIED — do not work until payer, scope and eligibility checked'}

def spawn_children(items, fn, max_workers):
    """Parent delegates bounded independent child tasks to worker pool."""
    with futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(fn, items))

def run():
    results = spawn_children(QUERIES, hunt, MAX_WORKERS)
    issues = {}
    errors = []
    for found, error in results:
        if error:
            errors.append(error)
        for item in found:
            if item.get('html_url'):
                issues[item['html_url']] = item
    candidates = [x for x in spawn_children(list(issues.values())[:MAX_TASKS], assess, MAX_WORKERS) if x]
    candidates.sort(key=lambda x: (x['comments'], -x['advertised_usd']))
    out = Path('rf-results')
    out.mkdir(exist_ok=True)
    (out / 'candidates.json').write_text(json.dumps({'earnings_zar': 0, 'paid_work_secured': 0,
        'workers_limit': MAX_WORKERS, 'candidates': candidates, 'errors': errors}, indent=2), encoding='utf-8')
    lines = ['# Revenue Foundry discovery swarm', '', '**Verified earnings: R0. Paid jobs secured: 0.**', '',
             'All opportunities are unverified. No payment, outreach or submissions performed.', '']
    for c in candidates[:20]:
        lines.append(f"- [{c['title']}]({c['url']}) — advertised USD {c['advertised_usd']}; {c['comments']} comments; UNVERIFIED")
    if errors:
        lines.append('\nAPI errors: ' + '; '.join(errors))
    (out / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"Found {len(candidates)} unverified candidates; verified earnings R0")

if __name__ == '__main__':
    run()
