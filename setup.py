import sys
import os
import shutil
import config
import random
import datetime

from ipaddress import IPv4Network

from app import db, app

from core.models import Paste, Owner, User, ServerMode

from db.addresses import networks
from db.agents import agents
from db.owners import owners
from db.titles import titles
from db.content import content
from db import generators

# Lab: seeding is deterministic. Every random choice comes from one
# random.Random(seed) instance and every seeded timestamp is SEED_EPOCH plus a
# drawn offset, so two boots with the same environment build byte-identical
# data (a control run and its paired run see the same site).
DEFAULT_SEED = 20240301
SEED_EPOCH = datetime.datetime(2024, 3, 1, 9, 0, 0)

# Lab: seeded volume, on top of upstream's admin/operator users and the
# DVGAUser owner with its two private pastes. Overridable per call, or by
# env DVGA_SEED_PASTES / DVGA_SEED_USERS.
DEFAULT_PASTES = 3000
DEFAULT_USERS = 150
PUBLIC_RATIO = 0.88
RESERVED_NAMES = ('admin', 'operator', 'dvgauser')
EMAIL_DOMAINS = ['example.com', 'example.org', 'example.net']

def env_int(name, default, minimum=None):
  raw = os.environ.get(name)
  if raw is None or raw.strip() == '':
    return default
  try:
    value = int(raw.strip())
  except ValueError:
    raise ValueError(f'{name} must be an integer, got {raw!r}') from None
  if minimum is not None and value < minimum:
    raise ValueError(f'{name} must be >= {minimum}, got {value}')
  return value

def seed_rng(seed=None):
  if seed is None:
    seed = env_int('DVGA_SEED', DEFAULT_SEED)
  return random.Random(seed)

def seed_timestamp(rng, max_days=180):
  """A fixed point in time: SEED_EPOCH plus a drawn whole-second offset."""
  return SEED_EPOCH + datetime.timedelta(seconds=rng.randrange(max_days * 86400))

def clean_up():
  if os.path.exists(config.WEB_UPLOADDIR):
    shutil.rmtree(config.WEB_UPLOADDIR)
    os.mkdir(config.WEB_UPLOADDIR)
  else:
    os.mkdir(config.WEB_UPLOADDIR)

  print('Reconstructing Database')
  if os.path.exists(config.SQLALCHEMY_FILE):
    try:
      os.remove(config.SQLALCHEMY_FILE)
    except OSError:
      pass
  return

def random_title(rng):
  return rng.choice(titles)

def random_content(rng):
  return rng.choice(content)

def random_owner(rng):
  return rng.choice(owners)

def random_address(rng):
  network = IPv4Network(rng.choice(networks))
  return str(network[rng.randrange(1, network.num_addresses - 1)])

def random_password(rng):
  weak_passwords = ['changeme']
  return rng.choice(weak_passwords)

def random_useragent(rng):
  user_agents = []
  for uas in agents:
    user_agents.append(uas)
  return rng.choice(user_agents)

def random_username(rng, taken):
  """A unique lower-case handle built from the first-name pool."""
  while True:
    first = random_owner(rng).lower()
    style = rng.randrange(4)
    if style == 0:
      name = f'{first}{rng.randrange(1, 100)}'
    elif style == 1:
      name = f'{first}.{rng.choice("abcdefghijklmnoprstvw")}'
    elif style == 2:
      name = f'{first}_{rng.choice("abcdefghijklmnoprstvw")}{rng.randrange(10)}'
    else:
      name = f'{rng.choice("abcdefghijklmnoprstvw")}{first}'
    name = name[:20]
    if name not in taken and name not in RESERVED_NAMES:
      taken.add(name)
      return name

def random_member_password(rng):
  alphabet = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  return ''.join(rng.choice(alphabet) for _ in range(14))

def seed_members(rng, n_users):
  """n_users site members, each with a User row, an Owner row of the same
  name, a few addresses and browsers, and a posting weight (a few members
  post a lot, most post a little)."""
  taken = set()
  members = []
  for _ in range(n_users):
    username = random_username(rng, taken)
    members.append({
      'user': User(username=username,
                   email=f'{username}@{rng.choice(EMAIL_DOMAINS)}',
                   password=random_member_password(rng)),
      'owner': Owner(name=username),
      'addresses': [random_address(rng) for _ in range(rng.randint(1, 3))],
      'agents': [random_useragent(rng) for _ in range(rng.randint(1, 2))],
      'weight': min(rng.paretovariate(1.2), 25.0),
    })
  return members

def random_paste(rng):
  """(title, content) for one seeded paste, dated from the seed epoch."""
  return generators.random_paste(rng, seed_timestamp(rng))

def pump_db(n_pastes: int = None, n_users: int = None, seed: int = None):
  """Create the schema and seed it.

  n_pastes / n_users: seeded pastes and members on top of upstream's rows;
  None means env DVGA_SEED_PASTES / DVGA_SEED_USERS, else 3000 / 150.
  seed: None means env DVGA_SEED, else DEFAULT_SEED.
  """
  if n_pastes is None:
    n_pastes = env_int('DVGA_SEED_PASTES', DEFAULT_PASTES, minimum=0)
  if n_users is None:
    n_users = env_int('DVGA_SEED_USERS', DEFAULT_USERS, minimum=0)
  if n_pastes < 0 or n_users < 0:
    raise ValueError('n_pastes and n_users must be >= 0')
  if n_pastes and not n_users:
    raise ValueError('seeding pastes needs at least one seeded user')
  print('Populating Database')
  rng = seed_rng(seed)
  with app.app_context():
    db.create_all()

    admin = User(username="admin", email="admin@blackhatgraphql.com", password=random_password(rng))
    operator = User(username="operator", email="operator@blackhatgraphql.com", password="password123")
    # create tokens for admin & operator

    db.session.add(admin)
    db.session.add(operator)

    owner = Owner(name='DVGAUser')
    db.session.add(owner)

    paste = Paste()
    paste.title = 'Testing Testing'
    paste.content = "My First Paste"
    paste.public = False
    paste.owner_id = owner.id
    paste.owner = owner
    paste.ip_addr = '127.0.0.1'
    paste.user_agent = 'User-Agent not set'
    db.session.add(paste)

    paste = Paste()
    paste.title = '555-555-1337'
    paste.content = "My Phone Number"
    paste.public = False
    paste.owner_id = owner.id
    paste.owner = owner
    paste.ip_addr = '127.0.0.1'
    paste.user_agent = 'User-Agent not set'
    db.session.add(paste)

    db.session.commit()

    members = seed_members(rng, n_users)
    for member in members:
      db.session.add(member['user'])
      db.session.add(member['owner'])

    weights = [m['weight'] for m in members]
    for _ in range(n_pastes):
      member = rng.choices(members, weights=weights)[0]
      title, body = random_paste(rng)
      paste = Paste()
      paste.title = title
      paste.content = body
      paste.public = rng.random() < PUBLIC_RATIO
      paste.owner = member['owner']
      paste.ip_addr = rng.choice(member['addresses'])
      paste.user_agent = rng.choice(member['agents'])
      db.session.add(paste)

    mode = ServerMode()
    mode.hardened = config.DVGA_LOCKED_MODE == 'hard'
    db.session.add(mode)

    db.session.commit()

    print('done')

if __name__ == '__main__':
  clean_up()
  pump_db()
  sys.exit()
