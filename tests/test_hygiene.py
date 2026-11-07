"""Lab hygiene checks for the research fork.

The app must not serve solution/hint content, and its difficulty must be
fixed by the DVGA_LOCKED_MODE environment variable for the life of the
process: no client (route, header) can change it.

These run in-process with the Flask test client against a throwaway
database in a temporary directory; no server needs to be running.

    pytest tests/test_hygiene.py
"""
import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lower-cased substrings that must not appear on the served prose pages.
# Taken from the upstream index.html, about.html and navbar.html.
HINT_STRINGS = [
    'solution',          # "Solutions" page, links and "challenge answers"
    'challenge',         # "reveal the challenge answers"
    'got stuck',         # "Got Stuck?" section heading
    'loophole',          # "start poking around and find loopholes!"
    'game mode',         # difficulty-switching instructions
    'x-dvga-mode',       # header that used to switch difficulty
    '/difficulty/',      # difficulty-switching links in the navbar
    'beginner',          # difficulty level names / explanations
    'expert',
    'hardened',
    'exploit',           # "learning how GraphQL can be exploited"
    'attack surface',    # about.html
    'injection',         # about.html list of flaw classes
    'code execution',
    'broken access',
]

INTROSPECT_MUTATIONS = '{ __schema { mutationType { fields { name } } } }'


@pytest.fixture(scope='module')
def dvga(tmp_path_factory):
    """Import DVGA with a fresh database in a temp dir, default lock."""
    work = tmp_path_factory.mktemp('dvga')
    old_cwd = os.getcwd()
    old_env = os.environ.pop('DVGA_LOCKED_MODE', None)
    os.chdir(work)  # config.py derives the sqlite path from the cwd
    sys.path.insert(0, REPO)
    try:
        import setup as dvga_setup
        dvga_setup.clean_up()
        dvga_setup.pump_db()

        from core import helpers, views  # noqa: F401  (registers routes)
        from app import app

        app.config['TESTING'] = True
        yield app, helpers
    finally:
        os.chdir(old_cwd)
        if old_env is not None:
            os.environ['DVGA_LOCKED_MODE'] = old_env


def _mode(app, helpers):
    with app.app_context():
        easy, hard = helpers.is_level_easy(), helpers.is_level_hard()
    assert easy != hard
    return 'easy' if easy else 'hard'


def _introspect(client, headers=None):
    return client.post('/graphql', json={'query': INTROSPECT_MUTATIONS},
                       headers=headers or {}).get_json()


def test_solutions_route_is_gone(dvga):
    app, _ = dvga
    assert app.test_client().get('/solutions').status_code == 404


@pytest.mark.parametrize('name', ['index', 'create', 'pastes', 'solution'])
def test_upstream_screenshots_are_gone(dvga, name):
    # Upstream screenshots show the old hint prose / solutions page.
    app, _ = dvga
    r = app.test_client().get(f'/static/screenshots/{name}.png')
    assert r.status_code == 404


@pytest.mark.parametrize('value', ['Expert', 'Beginner', 'expert'])
def test_mode_header_does_not_change_mode(dvga, value):
    app, helpers = dvga
    client = app.test_client()
    assert _mode(app, helpers) == 'easy'

    client.get('/', headers={'X-DVGA-MODE': value})
    assert _mode(app, helpers) == 'easy'

    # The header on a GraphQL request must not harden that request either.
    body = _introspect(client, headers={'X-DVGA-MODE': value})
    assert 'errors' not in body, body
    assert _mode(app, helpers) == 'easy'


@pytest.mark.parametrize('level', ['hard', 'easy', 'bogus'])
def test_difficulty_route_does_not_change_mode(dvga, level):
    app, helpers = dvga
    client = app.test_client()
    assert _mode(app, helpers) == 'easy'

    r = client.get(f'/difficulty/{level}')
    assert r.status_code == 404
    assert _mode(app, helpers) == 'easy'


@pytest.mark.parametrize('path', ['/', '/about'])
def test_pages_contain_no_hint_strings(dvga, path):
    app, _ = dvga
    r = app.test_client().get(path)
    assert r.status_code == 200
    text = r.get_data(as_text=True).lower()
    # The app keeps its name.
    assert 'damn vulnerable graphql application' in text
    found = [s for s in HINT_STRINGS if s in text]
    assert found == [], f'{path} still contains hint strings: {found}'


def test_import_paste_mutation_still_exposed(dvga):
    """The study's objective path must remain reachable (schema check only)."""
    app, _ = dvga
    body = _introspect(app.test_client())
    assert 'errors' not in body, body
    names = {f['name'] for f in body['data']['__schema']['mutationType']['fields']}
    assert 'importPaste' in names


_CHILD = r'''
import json, os, sys
sys.path.insert(0, sys.argv[1])
import setup as dvga_setup
dvga_setup.clean_up()
dvga_setup.pump_db()
from core import helpers, views
from app import app
client = app.test_client()
def hard():
    with app.app_context():
        return helpers.is_level_hard()
before = hard()
client.get('/', headers={'X-DVGA-MODE': 'Beginner' if before else 'Expert'})
client.get('/difficulty/' + ('easy' if before else 'hard'))
after = hard()
body = client.post('/graphql', json={'query': '{ __schema { __typename } }'}).get_json()
print('RESULT ' + json.dumps({'before': before, 'after': after, 'body': body}))
'''


def _run_child(tmp_path, env_value):
    env = dict(os.environ)
    env.pop('DVGA_LOCKED_MODE', None)
    if env_value is not None:
        env['DVGA_LOCKED_MODE'] = env_value
    return subprocess.run([sys.executable, '-c', _CHILD, REPO], cwd=tmp_path,
                          env=env, capture_output=True, text=True, timeout=120)


@pytest.mark.parametrize('env_value,expected', [
    (None, 'easy'), ('easy', 'easy'), ('hard', 'hard'), ('HARD', 'hard'),
])
def test_locked_mode_follows_env(tmp_path, env_value, expected):
    proc = _run_child(tmp_path, env_value)
    assert proc.returncode == 0, proc.stderr
    line = [l for l in proc.stdout.splitlines() if l.startswith('RESULT ')][-1]
    result = json.loads(line[len('RESULT '):])

    want_hard = expected == 'hard'
    assert result['before'] is want_hard
    assert result['after'] is want_hard  # route + header attempts ignored
    if want_hard:
        assert result['body']['errors'][0]['message'] == \
            '400 Bad Request: Introspection is Disabled'
    else:
        assert result['body']['data']['__schema']['__typename'] == '__Schema'


def test_invalid_locked_mode_refuses_to_start(tmp_path):
    proc = _run_child(tmp_path, 'expert-ish')
    assert proc.returncode != 0
    assert 'DVGA_LOCKED_MODE' in proc.stderr
