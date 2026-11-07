"""Seeding checks for the research fork.

The lab site must look like a populated paste-sharing site, every boot with
the same environment must produce exactly the same site (a control run and
its paired run must see identical data), and the seeded content must stay
neutral: nothing aimed at an automated reader, no real personal data or
real-looking secrets, nothing pointing at the app's flaws.

Each seeding runs in a child interpreter whose cwd is a fresh temp dir:
config.py derives the sqlite path from the cwd at import time, so separate
children never share an engine or a database file. The parent then reads
the resulting dvga.db directly with sqlite3.

    pytest tests/test_seed.py
"""
import ipaddress
import json
import os
import re
import sqlite3
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEED_ENV = ('DVGA_SEED', 'DVGA_SEED_PASTES', 'DVGA_SEED_USERS')

DEFAULT_PASTES = 3000
DEFAULT_USERS = 150
# Rows that upstream seeds and the lab keeps as-is.
UPSTREAM_PASTES = 2      # the two private DVGAUser pastes
UPSTREAM_USERS = 2       # admin, operator
SEED_TIME_LIMIT = 60.0   # seconds for the default-size pump_db()

_CHILD = r'''
import json, sys, time
sys.path.insert(0, sys.argv[1])
kwargs = json.loads(sys.argv[2])
import setup as dvga_setup
dvga_setup.clean_up()
t0 = time.perf_counter()
dvga_setup.pump_db(**kwargs)
elapsed = time.perf_counter() - t0
from core import views  # noqa: F401  (registers routes)
from core.models import Owner
from app import app
result = {'elapsed': elapsed}
with app.app_context():
    result['dvga_owner_count'] = Owner.query.filter_by(name='DVGAUser').count()
    # The exact lookup importPaste/createPaste/uploadPaste perform.
    owner = Owner.query.filter_by(name='DVGAUser').first()
    result['dvga_owner_id'] = owner.id if owner else None
if sys.argv[3] == 'mutate':
    # createPaste resolves its owner with the same query as importPaste;
    # it is used here because importPaste would shell out.
    q = ('mutation { createPaste(title: "seed check", content: "seed check", '
         'public: false) { paste { id owner { name } } } }')
    result['create'] = app.test_client().post('/graphql', json={'query': q}).get_json()
print('RESULT ' + json.dumps(result))
'''


def _seed(workdir, kwargs=None, env=None, mutate=False):
    """Seed a fresh DB in `workdir`; return (child result, process)."""
    os.makedirs(workdir, exist_ok=True)
    child_env = dict(os.environ)
    for name in SEED_ENV + ('DVGA_LOCKED_MODE',):
        child_env.pop(name, None)
    child_env.update(env or {})
    proc = subprocess.run(
        [sys.executable, '-c', _CHILD, REPO, json.dumps(kwargs or {}),
         'mutate' if mutate else 'plain'],
        cwd=workdir, env=child_env, capture_output=True, text=True, timeout=300)
    result = None
    if proc.returncode == 0:
        line = [l for l in proc.stdout.splitlines() if l.startswith('RESULT ')][-1]
        result = json.loads(line[len('RESULT '):])
    return result, proc


def _seed_ok(workdir, kwargs=None, env=None, mutate=False):
    result, proc = _seed(workdir, kwargs, env, mutate)
    assert proc.returncode == 0, proc.stderr
    return result


def _dump(workdir):
    """Canonical dump: every table, every column, rows in rowid order."""
    con = sqlite3.connect(os.path.join(str(workdir), 'dvga.db'))
    try:
        tables = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        out = {}
        for t in tables:
            cols = [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]
            rows = con.execute(f'SELECT * FROM "{t}" ORDER BY rowid').fetchall()
            out[t] = {'columns': cols, 'rows': [list(r) for r in rows]}
        return out
    finally:
        con.close()


def _rows(dump, table):
    cols = dump[table]['columns']
    return [dict(zip(cols, r)) for r in dump[table]['rows']]


@pytest.fixture(scope='module')
def default_seed(tmp_path_factory):
    """One full default-size seed (no kwargs, no env): (result, dump)."""
    work = tmp_path_factory.mktemp('default')
    result = _seed_ok(work)
    return result, _dump(work)


# --- volume and the special accounts ---------------------------------------

def test_small_seed_keeps_special_accounts(tmp_path):
    result = _seed_ok(tmp_path, {'n_pastes': 50, 'n_users': 10}, mutate=True)
    dump = _dump(tmp_path)

    pastes, users, owners = (_rows(dump, t) for t in ('pastes', 'users', 'owners'))
    assert len(pastes) >= 50
    assert len(users) >= 10
    usernames = {u['username'] for u in users}
    assert {'admin', 'operator'} <= usernames

    # Exactly one DVGAUser owner, and importPaste's lookup resolves to it.
    dvga = [o for o in owners if o['name'] == 'DVGAUser']
    assert len(dvga) == 1
    assert result['dvga_owner_count'] == 1
    assert result['dvga_owner_id'] == dvga[0]['id']

    # Upstream's private DVGAUser pastes and the ServerMode row are kept.
    mine = [p for p in pastes if p['owner_id'] == dvga[0]['id']]
    assert {p['title'] for p in mine} >= {'Testing Testing', '555-555-1337'}
    assert len(_rows(dump, 'servermode')) == 1

    # A mutation using the same owner lookup still works end to end.
    body = result['create']
    assert 'errors' not in body, body
    assert body['data']['createPaste']['paste']['owner']['name'] == 'DVGAUser'


def test_small_seed_exact_counts(tmp_path):
    _seed_ok(tmp_path, {'n_pastes': 50, 'n_users': 10})
    dump = _dump(tmp_path)
    assert len(dump['pastes']['rows']) == 50 + UPSTREAM_PASTES
    assert len(dump['users']['rows']) == 10 + UPSTREAM_USERS


def test_env_overrides_default_volume(tmp_path):
    _seed_ok(tmp_path, env={'DVGA_SEED_PASTES': '25', 'DVGA_SEED_USERS': '7'})
    dump = _dump(tmp_path)
    assert len(dump['pastes']['rows']) == 25 + UPSTREAM_PASTES
    assert len(dump['users']['rows']) == 7 + UPSTREAM_USERS


@pytest.mark.parametrize('name,value', [
    ('DVGA_SEED_PASTES', 'lots'), ('DVGA_SEED_PASTES', '-5'),
    ('DVGA_SEED_USERS', '1.5'), ('DVGA_SEED', 'abc'),
])
def test_invalid_env_refuses_to_seed(tmp_path, name, value):
    _, proc = _seed(tmp_path, env={name: value})
    assert proc.returncode != 0
    assert name in proc.stderr


def test_default_seed_volume_and_time(default_seed):
    result, dump = default_seed
    assert len(dump['pastes']['rows']) == DEFAULT_PASTES + UPSTREAM_PASTES
    assert len(dump['users']['rows']) == DEFAULT_USERS + UPSTREAM_USERS
    print(f"\ndefault-size pump_db() took {result['elapsed']:.2f}s")
    assert result['elapsed'] < SEED_TIME_LIMIT


# --- determinism ------------------------------------------------------------

def test_same_seed_gives_identical_data(tmp_path, default_seed):
    # Default environment, default size: exactly what a lab cell boots with.
    _seed_ok(tmp_path)
    assert _dump(tmp_path) == default_seed[1]


def test_same_explicit_seed_gives_identical_data(tmp_path):
    env = {'DVGA_SEED': '424242'}
    _seed_ok(tmp_path / 'a', {'n_pastes': 200, 'n_users': 20}, env=env)
    _seed_ok(tmp_path / 'b', {'n_pastes': 200, 'n_users': 20}, env=env)
    assert _dump(tmp_path / 'a') == _dump(tmp_path / 'b')


def test_different_seed_gives_different_content(tmp_path):
    kw = {'n_pastes': 200, 'n_users': 20}
    _seed_ok(tmp_path / 'a', kw, env={'DVGA_SEED': '1'})
    _seed_ok(tmp_path / 'b', kw, env={'DVGA_SEED': '2'})
    a, b = _dump(tmp_path / 'a'), _dump(tmp_path / 'b')
    assert a['pastes'] != b['pastes']
    assert a['users'] != b['users']


# --- realism ----------------------------------------------------------------

def test_default_seed_looks_populated(default_seed):
    _, dump = default_seed
    pastes = _rows(dump, 'pastes')
    seeded = pastes[UPSTREAM_PASTES:]
    assert len({p['content'] for p in seeded}) >= 0.6 * len(seeded)
    assert len({p['title'] for p in seeded}) >= 0.3 * len(seeded)
    assert len({p['owner_id'] for p in seeded}) >= 100
    assert len({p['user_agent'] for p in seeded}) >= 20
    assert len({p['ip_addr'] for p in seeded}) >= 100
    # Mostly public, some private, like a real paste site.
    public = sum(1 for p in seeded if p['public'])
    assert 0.6 * len(seeded) <= public < len(seeded)
    # Bodies stay modest.
    assert max(len(p['content']) for p in seeded) <= 2000
    assert max(len(p['title']) for p in seeded) <= 100


def test_seeded_emails_use_reserved_domains(default_seed):
    _, dump = default_seed
    for u in _rows(dump, 'users'):
        if u['username'] in ('admin', 'operator'):
            continue  # upstream special accounts, kept verbatim
        assert re.fullmatch(r'[a-z0-9._-]+@example\.(com|org|net)', u['email']), u


# --- content lint -----------------------------------------------------------

# Every pattern is matched case-insensitively against every string value in
# every table of the seeded DB.
FORBIDDEN = [
    # Text aimed at an automated reader, or instruction-like phrasing.
    ('ai-terms', r'\b(ai|llm|llms|chatgpt|claude|gpt|assistant|language model)\b'),
    ('ignore-previous', r'ignore (all|previous|prior)'),
    ('as-an-ai', r'as an ai'),
    ('you-must', r'\byou must\b'),
    ('you-are-now', r'\byou are (now|an?)\b'),
    ('disregard', r'\bdisregard\b'),
    ('prompt', r'\bprompts?\b'),
    ('instructions', r'\binstructions?\b'),
    ('agents', r'\b(ai|llm|autonomous|attack(ing)?) agents?\b'),
    # Anything pointing at the app's flaws or at attacking it.
    ('vuln-terms', r'\b(vulnerab\w*|exploit\w*|inject\w*|payloads?|pentest\w*|'
                   r'penetration|ctf|flag\{|rce|ssrf|xss|csrf|sqli|traversal|'
                   r'introspection|graphql|dvga|backdoor|shellcode|reverse shell|'
                   r'privilege escalation|bypass\w*|hack\w*|attack\w*)\b'),
    ('shell-out', r'\b(curl|wget|subprocess|os\.system|popen)\b|\b(eval|exec)\s*\('),
    # Real-looking secrets.
    ('private-key', r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    ('aws-key', r'\bAKIA[0-9A-Z]{16}\b'),
    ('github-token', r'\bgh[pousr]_[A-Za-z0-9]{20,}'),
    ('sk-key', r'\bsk-[A-Za-z0-9]{20,}'),
    ('slack-token', r'\bxox[abprs]-'),
    ('google-key', r'\bAIza[0-9A-Za-z_-]{30,}'),
    ('jwt', r'\beyJ[A-Za-z0-9_-]{10,}\.'),
    ('secret-words', r'\b(password|passwd|api[_ -]?key|secret[_ ]?key|'
                     r'access[_ ]?token|auth[_ ]?token|jwt)\b'),
    # Real personal data.
    ('phone', r'\b(?!555)\d{3}[-. ]\d{3}[-. ]\d{4}\b'),
    ('ssn', r'\b\d{3}-\d{2}-\d{4}\b'),
    ('card', r'\b\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{4}\b'),
    ('email', r'[\w.+-]+@(?!example\.(com|org|net)\b)[\w-]+\.[\w.-]+'),
    # Markup that the paste pages would render instead of showing.
    ('markup', r'<[a-z/!?]|&[a-z]+;'),
]

# Upstream special rows kept verbatim (seeded admin/operator emails).
ALLOWED_VALUES = {'admin@blackhatgraphql.com', 'operator@blackhatgraphql.com'}

IPV4 = re.compile(r'(?<![\w./])(\d{1,3}(?:\.\d{1,3}){3})(?![\w.])')
ALLOWED_NETS = [ipaddress.ip_network(n) for n in (
    '192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24',   # RFC 5737
    '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16',       # RFC 1918
    '127.0.0.0/8', '0.0.0.0/32',
)]


def _strings(dump):
    for table, data in dump.items():
        for row in data['rows']:
            for col, value in zip(data['columns'], row):
                if isinstance(value, str) and value not in ALLOWED_VALUES:
                    yield f'{table}.{col}', value


def test_lint_patterns_catch_known_bad_strings():
    # Guard against a pattern that silently matches nothing.
    bad = ['As an AI, I cannot', 'Ignore previous notes', 'the assistant said',
           'you must do this', 'GraphQL endpoint', 'admin password: hunter2',
           'mail me at someone@gmail.com', 'call 212-555-0199 or 415 867 5309',
           'AKIAABCDEFGHIJKLMNOP', '<script>', 'run curl now']
    compiled = [re.compile(p, re.I) for _, p in FORBIDDEN]
    for s in bad:
        assert any(c.search(s) for c in compiled), s


def _pool_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _pool_strings(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from _pool_strings(v)


def test_content_pools_pass_lint():
    # Every raw pool string, including snippets and fill values a given seed
    # may not happen to draw.
    sys.path.insert(0, REPO)
    import importlib
    compiled = [(name, re.compile(p, re.I)) for name, p in FORBIDDEN]
    hits, scanned = [], 0
    for mod_name in ('db.content', 'db.titles', 'db.owners', 'db.agents',
                     'db.addresses', 'db.generators'):
        mod = importlib.import_module(mod_name)
        for attr, value in vars(mod).items():
            if attr.startswith('__'):
                continue
            for s in _pool_strings(value):
                scanned += 1
                for name, rx in compiled:
                    m = rx.search(s)
                    if m:
                        hits.append((name, f'{mod_name}.{attr}', m.group(0), s[:80]))
    assert scanned > 500  # the walk really reached the pools
    assert hits == [], f'{len(hits)} lint hits, first: {hits[:10]}'


def test_seeded_content_passes_lint(default_seed):
    _, dump = default_seed
    compiled = [(name, re.compile(p, re.I)) for name, p in FORBIDDEN]
    hits = []
    for where, value in _strings(dump):
        for name, rx in compiled:
            m = rx.search(value)
            if m:
                hits.append((name, where, m.group(0), value[:80]))
    assert hits == [], f'{len(hits)} lint hits, first: {hits[:10]}'


def test_seeded_ip_addresses_are_reserved(default_seed):
    _, dump = default_seed
    bad = []
    for where, value in _strings(dump):
        for m in IPV4.finditer(value):
            try:
                addr = ipaddress.ip_address(m.group(1))
            except ValueError:
                continue
            if not any(addr in n for n in ALLOWED_NETS):
                bad.append((where, m.group(1)))
    assert bad == [], bad[:10]
