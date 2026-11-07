"""Generated paste bodies for the seed data: logs, meeting notes, lists, CSV.

Every function takes the seeding RNG and, where time matters, a `when`
datetime derived from the fixed seed epoch. Nothing here reads the clock or
the global `random` module, so the output is a pure function of the seed.
"""
import datetime
import re

from db.content import content, fill_values, snippets
from db.owners import owners
from db.titles import titles

_PLACEHOLDER = re.compile(r'\{\{(\w+)\}\}')

TITLE_SUFFIXES = [' (v2)', ' - draft', ' - final', ' backup', ' copy', ' fixed',
                  ' WIP', ' (old)', ' updated', ' for later', ' mk2']


def fill(rng, text):
  """Replace each {{name}} with one value drawn from fill_values[name];
  repeats of the same name in one text get the same value."""
  chosen = {}

  def pick(m):
    name = m.group(1)
    if name not in chosen:
      chosen[name] = rng.choice(fill_values[name])
    return chosen[name]

  return _PLACEHOLDER.sub(pick, text)


def _date(when):
  return when.strftime('%Y-%m-%d')


def _vary_title(rng, title, when):
  r = rng.random()
  if r < 0.25:
    return title + rng.choice(TITLE_SUFFIXES)
  if r < 0.35:
    return f'{title} {_date(when)}'
  return title


# --- fixed snippets ---------------------------------------------------------

def snippet_paste(rng, when):
  item = rng.choice(snippets)
  joined = fill(rng, rng.choice(item['titles']) + '\x00' + item['body'])
  title, body = joined.split('\x00', 1)
  return _vary_title(rng, title, when), body


# --- short notes ------------------------------------------------------------

def note_paste(rng, when):
  lines = rng.sample(content, rng.randint(1, 4))
  sep = rng.choice(['\n', '\n\n', ' '])
  return _vary_title(rng, rng.choice(titles), when), sep.join(lines)


# --- logs -------------------------------------------------------------------

_PATHS = ['/', '/login', '/cart', '/checkout', '/search', '/products',
          '/products/{id}', '/orders/{id}', '/static/app.css', '/static/app.js',
          '/api/items', '/api/items/{id}', '/api/basket', '/health', '/favicon.ico',
          '/blog', '/blog/{slug}', '/account', '/help']
_SLUGS = ['spring-sale', 'new-arrivals', 'care-guide', 'gift-ideas', 'store-hours',
          'shipping-update', 'winter-collection', 'repair-tips']
_STATUS = [200] * 14 + [201, 204, 301, 304, 304, 400, 404, 404, 500, 502]
_METHODS = ['GET'] * 8 + ['POST', 'POST', 'PUT', 'DELETE']
_APP_EVENTS = [
  ('INFO', 'worker started, concurrency={n}'),
  ('INFO', 'cache warmed: {n} keys'),
  ('INFO', 'scheduled job "nightly-digest" finished in {ms}ms'),
  ('INFO', 'connected to database pool size={n}'),
  ('WARN', 'slow query took {ms}ms (orders by customer)'),
  ('WARN', 'retrying upstream request, attempt {n}'),
  ('WARN', 'disk usage at {pct}% on /var'),
  ('ERROR', 'timeout talking to the image resizer after {ms}ms'),
  ('ERROR', 'could not parse date "31/02/2024" in row {n} of the spreadsheet'),
  ('INFO', 'config reloaded'),
  ('DEBUG', 'session cleanup removed {n} expired entries'),
]


def _fmt_event(rng, text):
  return text.format(n=rng.randint(2, 64), ms=rng.randint(120, 9000),
                     pct=rng.randint(71, 96))


def _access_line(rng, t):
  path = rng.choice(_PATHS).format(id=rng.randint(1, 5000), slug=rng.choice(_SLUGS))
  return '{} {} {} {} {}ms'.format(t.strftime('%Y-%m-%d %H:%M:%S'),
                                   rng.choice(_METHODS), path, rng.choice(_STATUS),
                                   rng.randint(2, 900))


def log_paste(rng, when):
  kind = rng.randrange(4)
  t = when
  lines = []
  n = rng.randint(8, 24)
  if kind == 0:
    service = rng.choice(fill_values['service'])
    title = rng.choice([f'{service} logs', f'{service} log excerpt',
                        f'logs from {_date(when)}', 'weird log lines', 'log dump'])
    for _ in range(n):
      t += datetime.timedelta(seconds=rng.randint(1, 90))
      if rng.random() < 0.7:
        lines.append(_access_line(rng, t))
      else:
        level, text = rng.choice(_APP_EVENTS)
        lines.append(f"{t.strftime('%Y-%m-%d %H:%M:%S')} {level:5} {service}: "
                     f"{_fmt_event(rng, text)}")
  elif kind == 1:
    title = rng.choice(['build output', 'failing build', 'ci log', 'test run output'])
    lines.append(f"[{t.strftime('%H:%M:%S')}] build started on {rng.choice(fill_values['branch'])}")
    passed = 0
    for i in range(n):
      t += datetime.timedelta(seconds=rng.randint(1, 20))
      mod = rng.choice(['dates', 'export', 'parser', 'basket', 'search', 'layout',
                        'units', 'money', 'calendar', 'images'])
      ok = rng.random() < 0.9
      passed += ok
      lines.append(f"[{t.strftime('%H:%M:%S')}] test_{mod}.py::test_case_{i + 1} "
                   f"{'PASSED' if ok else 'FAILED'}")
    lines.append(f"[{t.strftime('%H:%M:%S')}] {passed} passed, {n - passed} failed")
  elif kind == 2:
    title = rng.choice(['cron output', 'backup log', 'nightly job log'])
    for _ in range(n):
      t += datetime.timedelta(minutes=rng.choice([10, 10, 10, 60]))
      size = rng.randint(80, 4200)
      lines.append(f"{t.strftime('%b %d %H:%M:%S')} backup.sh: archived "
                   f"{rng.choice(fill_values['dir'])} ({size} MB) "
                   f"{rng.choice(['ok', 'ok', 'ok', 'skipped, unchanged'])}")
  else:
    title = rng.choice(['journalctl output', 'service restart loop', 'systemd log'])
    unit = rng.choice(fill_values['service'])
    for _ in range(n):
      t += datetime.timedelta(seconds=rng.randint(1, 30))
      msg = rng.choice([f'Started {unit} worker.', f'{unit}.service: Main process exited, status=1/FAILURE',
                        f'{unit}.service: Scheduled restart job, restart counter is at {rng.randint(1, 9)}.',
                        f'Stopped {unit} worker.', 'Reached target Multi-User System.',
                        f'{unit}[{rng.randint(800, 9000)}]: listening on 127.0.0.1:{rng.choice(fill_values["port"])}'])
      lines.append(f"{t.strftime('%b %d %H:%M:%S')} host{rng.randint(1, 4)} {msg}")
  return title, '\n'.join(lines)


# --- meeting notes ----------------------------------------------------------

_TEAMS = ['team', 'design', 'platform', 'support', 'marketing', 'ops', 'product',
          'committee', 'book club', 'garden club', 'PTA', 'band']
_TOPICS = ['budget for next quarter', 'holiday rota', 'new office seating plan',
           'website redesign', 'onboarding checklist', 'customer feedback themes',
           'release schedule', 'summer party venue', 'hiring plan', 'documentation gaps',
           'support ticket backlog', 'monthly newsletter', 'fundraiser dates',
           'equipment orders', 'room bookings', 'training sessions']
_NOTES = ['agreed to keep the current schedule for now',
          'numbers look better than last month',
          'need more data before deciding',
          'most people prefer the earlier slot',
          'two options shortlisted, vote next week',
          'concern about the timeline, will revisit',
          'quick win: update the shared calendar',
          'no objections raised',
          'parked until after the holidays',
          'feedback was mostly positive']
_ACTIONS = ['send the summary to everyone', 'book the room for next month',
            'draft the proposal', 'collect quotes from three suppliers',
            'update the shared spreadsheet', 'ask facilities about the heating',
            'write up the FAQ', 'check the budget with finance',
            'set up the next meeting', 'review the draft and comment',
            'order the new chairs', 'contact the venue']


def meeting_paste(rng, when):
  when = when.replace(hour=rng.randint(9, 16), minute=rng.choice([0, 15, 30, 45]), second=0)
  team = rng.choice(_TEAMS)
  title = rng.choice([f'{team} meeting {_date(when)}', f'{team} sync notes',
                      f'notes from {team} meeting', f'minutes {_date(when)}',
                      f'retro {_date(when)}'])
  people = rng.sample(owners, rng.randint(3, 6))
  topics = rng.sample(_TOPICS, rng.randint(2, 4))
  lines = [f"Meeting - {when.strftime('%a %d %b %Y, %H:%M')}",
           'Attendees: ' + ', '.join(people), '', 'Agenda']
  lines += [f'{i}. {t}' for i, t in enumerate(topics, 1)]
  lines += ['', 'Notes']
  for t in topics:
    lines.append(f'- {t}: {rng.choice(_NOTES)}')
  lines += ['', 'Actions']
  for a in rng.sample(_ACTIONS, rng.randint(2, 4)):
    lines.append(f'- {rng.choice(people)}: {a}')
  return title, '\n'.join(lines)


# --- lists ------------------------------------------------------------------

_CHORES = ['vacuum the stairs', 'clean the oven', 'sort the recycling', 'change bed sheets',
           'descale the kettle', 'wipe kitchen cupboards', 'mow the lawn', 'fix the shelf',
           'take old clothes to the charity shop', 'clean the windows', 'water the garden',
           'empty the dehumidifier', 'tidy the garage', 'wash the car', 'defrost the freezer',
           'reply to the school email', 'book a haircut', 'renew the passport photo',
           'call the plumber', 'pay the water bill', 'update the calendar',
           'print the train tickets', 'return the parcel', 'replace the smoke alarm battery']
_GROCERIES = ['milk', 'eggs', 'bread', 'butter', 'apples', 'bananas', 'onions', 'garlic',
              'tomatoes', 'spinach', 'rice', 'pasta', 'chickpeas', 'lentils', 'oats',
              'yoghurt', 'cheddar', 'coffee', 'tea', 'olive oil', 'lemons', 'carrots',
              'potatoes', 'peppers', 'tinned tomatoes', 'frozen peas', 'dish soap',
              'toilet paper', 'bin bags', 'sponges', 'cat food', 'flour', 'sugar',
              'honey', 'peanut butter', 'tortillas', 'avocados', 'basil']
_PACKING = ['passport', 'charger', 'adapter plug', 'headphones', 'toothbrush', 'sunscreen',
            'rain jacket', 'walking shoes', 'swimsuit', 'book', 'snacks', 'water bottle',
            'sunglasses', 'medication', 'spare socks', 'notebook', 'camera', 'travel pillow']
_WATCH = ['The Quiet Harbour', 'Seven Bridges', 'Paper Moons', 'North of the River',
          'The Long Weekend', 'Glass Orchard', 'A House by the Dunes', 'Winter Crossing',
          'The Map Room', 'Lanterns', 'Salt and Stone', 'Under the Viaduct',
          'The Clockmaker', 'Blue Hour', 'Field Notes', 'Second Spring']


def list_paste(rng, when):
  kind = rng.randrange(4)
  if kind == 0:
    title = rng.choice(['todo', 'TODO', 'to do this week', 'weekend chores', 'house jobs',
                        f'todo {_date(when)}'])
    items = rng.sample(_CHORES, rng.randint(4, 10))
    body = '\n'.join(f"[{'x' if rng.random() < 0.35 else ' '}] {i}" for i in items)
  elif kind == 1:
    title = rng.choice(['shopping list', 'groceries', 'supermarket', 'shopping',
                        f'shopping {when.strftime("%a")}'])
    items = rng.sample(_GROCERIES, rng.randint(5, 14))
    body = '\n'.join(f'- {i}' + (f' x{rng.randint(2, 4)}' if rng.random() < 0.2 else '')
                     for i in items)
  elif kind == 2:
    city = rng.choice(fill_values['city'])
    title = rng.choice(['packing list', f'packing for {city}', 'what to bring'])
    body = '\n'.join(f'[ ] {i}' for i in rng.sample(_PACKING, rng.randint(6, 14)))
  else:
    title = rng.choice(['watchlist', 'to read', 'films to watch', 'book list',
                        'recommendations from the group'])
    picks = rng.sample(_WATCH, rng.randint(4, 9))
    body = '\n'.join(f'{i}. {t}' + (f' - {rng.choice(owners)} says it is good'
                                     if rng.random() < 0.3 else '')
                     for i, t in enumerate(picks, 1))
  return title, body


# --- CSV --------------------------------------------------------------------

def csv_paste(rng, when):
  kind = rng.randrange(4)
  rows = rng.randint(6, 15)
  day = when.date()
  out = []
  if kind == 0:
    title = rng.choice(['expenses', 'monthly expenses', 'spending.csv'])
    out.append('date,category,amount')
    for _ in range(rows):
      day += datetime.timedelta(days=rng.randint(0, 3))
      cat = rng.choice(['groceries', 'transport', 'eating out', 'utilities', 'books', 'gifts'])
      out.append(f'{day.isoformat()},{cat},{rng.randint(300, 9000) / 100:.2f}')
  elif kind == 1:
    city = rng.choice(fill_values['city'])
    title = rng.choice([f'{city} temperatures', 'weather log', 'temps.csv'])
    out.append('date,min_c,max_c,rain_mm')
    for _ in range(rows):
      day += datetime.timedelta(days=1)
      lo = rng.randint(-3, 16)
      out.append(f'{day.isoformat()},{lo},{lo + rng.randint(3, 12)},{rng.choice([0, 0, 0, 1.2, 3.5, 8.0])}')
  elif kind == 2:
    title = rng.choice(['running log', 'runs.csv', 'training log'])
    out.append('date,km,minutes,notes')
    for _ in range(rows):
      day += datetime.timedelta(days=rng.randint(1, 3))
      km = rng.randint(30, 180) / 10
      out.append(f'{day.isoformat()},{km:.1f},{int(km * rng.uniform(5.0, 6.8))},'
                 f'{rng.choice(["easy", "hills", "tempo", "with the club", "windy", ""])}')
  else:
    title = rng.choice(['inventory', 'stock count', 'inventory.csv'])
    out.append('sku,item,qty,location')
    for i in range(rows):
      item = rng.choice(['mug', 'notebook', 'tote bag', 'candle', 'poster', 'pen set',
                         'coaster', 'tea towel', 'keyring', 'postcard'])
      out.append(f'SKU-{rng.randint(1000, 9999)},{item},{rng.randint(0, 240)},'
                 f'{rng.choice(["A1", "A2", "B1", "B4", "C3", "store room"])}')
  return title, '\n'.join(out)


# Paste kinds and their share of the seed.
KINDS = [
  (snippet_paste, 34),
  (note_paste, 18),
  (list_paste, 16),
  (log_paste, 12),
  (meeting_paste, 10),
  (csv_paste, 10),
]


def random_paste(rng, when):
  """(title, content) for one seeded paste."""
  fn = rng.choices([k[0] for k in KINDS], weights=[k[1] for k in KINDS])[0]
  return fn(rng, when)
