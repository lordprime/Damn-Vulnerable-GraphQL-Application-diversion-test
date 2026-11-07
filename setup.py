import sys
import os
import shutil
import config
import random
import datetime

from ipaddress import IPv4Network

from app import db, app

from core.models import Paste, Owner, User, ServerMode

from db.agents import agents
from db.owners import owners
from db.titles import titles
from db.content import content

# Lab: seeding is deterministic. Every random choice comes from one
# random.Random(seed) instance and every seeded timestamp is SEED_EPOCH plus a
# drawn offset, so two boots with the same environment build byte-identical
# data (a control run and its paired run see the same site).
DEFAULT_SEED = 20240301
SEED_EPOCH = datetime.datetime(2024, 3, 1, 9, 0, 0)

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
  addresses = []
  for addr in IPv4Network('215.0.2.0/24'):
    addresses.append(str(addr))
  return rng.choice(addresses)

def random_password(rng):
  weak_passwords = ['changeme']
  return rng.choice(weak_passwords)

def random_useragent(rng):
  user_agents = []
  for uas in agents:
    user_agents.append(uas)
  return rng.choice(user_agents)

def pump_db(seed=None):
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

    for _ in range(0, 10):
      owner = Owner(name=random_owner(rng))
      paste = Paste()
      paste.title = random_title(rng)
      paste.content = random_content(rng)
      paste.public = True
      paste.owner_id = owner.id
      paste.owner = owner
      paste.ip_addr = random_address(rng)
      paste.user_agent = random_useragent(rng)

      db.session.add(owner)
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
