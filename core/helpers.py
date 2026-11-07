import base64
import uuid
import os
from config import WEB_UPLOADDIR, DVGA_LOCKED_MODE
from jwt import decode

def run_cmd(cmd):
  return os.popen(cmd).read()

def initialize():
  return run_cmd('python3 setup.py')

def generate_uuid():
  return str(uuid.uuid4())[0:6]

def decode_base64(text):
  return base64.b64decode(text).decode('utf-8')

def get_identity(token):
  return decode(token, options={"verify_signature":False, "verify_exp":False}).get('identity')

def save_file(filename, text):
  try:
    f = open(WEB_UPLOADDIR + filename, 'w')
    f.write(text)
    f.close()
  except Exception as e:
    text = str(e)
  return text

# The level is read once from the environment (config.DVGA_LOCKED_MODE).
def is_level_easy():
  return DVGA_LOCKED_MODE == 'easy'

def is_level_hard():
  return DVGA_LOCKED_MODE == 'hard'

