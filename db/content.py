# Content pools that setup.py draws from when seeding the paste site.

# Short one-line notes. Seeded "note" pastes join one to four of these.
content = [
  'Sixty-Four comes asking for bread',
  'He is good at eating pickles and telling women about his emotional problems.',
  'He used to get confused between soldiers and shoulders, but as a military man, he now soldiers responsibility.',
  'Pantyhose and heels are an interesting choice of attire for the beach.',
  'I checked to make sure that he was still alive.',
  'There is an art to getting your way, and spitting olive pits across the table is not it.',
  'One advanced diverted',
  'Too end instrument possession contrasted motionless',
  'Mind your own business!',
  'You are the Weakest Link! Goodbye!',
  'Will you pick me up at my place?',
  'What a big pumpkin!',
  'quick trip back to Tennessee for the weekend!',
  'I was excited to spend time with my wife without being interrupted by kids.',
  'What are some things you don’t like to do and why?',
  'These are used for cautioning someone to wait and not make a bad decision or take reckless action.',
  'I am always late and I do not care.',
  'They live in a beautiful house.',
  'Do you know that man with a big hat on?',
  'Where do you live?',
  'Why can you open the door?',
  'He reminds me of your brother.',
  'How big you are!',
  'What does your room look like?',
  'Will you be free tomorrow morning?',
  'The sun rises at the east.',
  'How big is your house?',
  'Renew the library card before the end of the month.',
  'The bakery on the corner closes early on Sundays.',
  'Bring the blue folder to the next appointment.',
  'The plant by the window needs water twice a week in summer.',
  'Left the umbrella at the cafe again.',
  'Call the landlord about the dripping tap.',
  'The bus timetable changes after the holidays.',
  'Try the lemon cake recipe with less sugar next time.',
  'Book club moved to Thursday this month.',
  'Pick up dry cleaning on the way home.',
  'The car is due for an oil change at the next service.',
  'Remember to back up the photos from the old phone.',
  'Return the borrowed drill to the neighbour.',
  'The new running route along the river is about five kilometres.',
  'Order more printer paper for the office.',
  'The cat refuses to eat the new food brand.',
  'Swap the winter tyres in April.',
  'The dentist asked to reschedule to next Tuesday.',
  'Look into evening pottery classes.',
  'The farmers market has the best strawberries in June.',
  'Need a new charger cable for the laptop.',
  'The hallway light flickers when it rains.',
  'Ask about the parking permit at the town hall.',
  'Practice the guitar chord change from G to C.',
  'The museum is free on the first Sunday of the month.',
  'Get birthday card for the team lead.',
  'Train tickets are cheaper if booked three weeks ahead.',
  'The soup was better the second day.',
  'Water the tomatoes in the morning, not at night.',
  'Clean the gutters before autumn.',
  'The lake path is muddy after rain, wear boots.',
  'Finished the jigsaw puzzle, two pieces missing.',
  'The streaming subscription renews on the 14th.',
  'Brought the wrong charger to the conference room.',
  'Coffee machine on the third floor is fixed.',
  'A good day starts with a short walk.',
  'Sketch the bookshelf layout before buying wood.',
  'Measured the window: 120 by 90 centimetres.',
  'The quiet carriage is always at the front of the train.',
  'Kids want pancakes on Saturday.',
  'Cancel the gym trial before it converts.',
  'The tram stop moved one block north during construction.',
  'Make extra ice for the party.',
  'Return the jacket, the sleeves are too short.',
  'Library has the second book on hold for me.',
  'Remember the bike lock key is in the kitchen drawer.',
  'Fog this morning was thick enough to hide the bridge.',
  'The neighbours are repainting the fence green.',
  'Pay the electricity bill before Friday.',
  'Try reading twenty pages before bed.',
  'The hiking trail closes at sunset.',
  'Lemon, honey and ginger for the sore throat.',
  'Swap shifts with the evening team next week.',
  'The printer only works if you select tray two.',
  'Meeting room B has the better projector.',
  'Bring snacks for the long drive.',
  'Find the warranty for the dishwasher.',
  'The blackbirds are nesting in the hedge again.',
  'Write down the recipe grandma made at the reunion.',
  'Need to defrost the freezer this weekend.',
  'The car park fills up by nine.',
  'Rain expected all week, postpone the barbecue.',
  'Laundry detergent is on sale at the supermarket.',
  'Stretch for ten minutes after every run.',
  'The puzzle book answers are in the back.',
  'Return library books by the 3rd.',
  'Look up the opening hours for the recycling centre.',
  'Charge the camera batteries before the trip.',
  'Pack the picnic blanket.',
  'Thank the neighbours for collecting the post.',
  'Coffee beans from the market were too bitter.',
  'Clean the bike chain after the muddy ride.',
  'Paint swatches: sage, sand, or pale grey.',
  'The clock in the kitchen is five minutes fast.',
  'Read the chapter on sourdough starters.',
  'Find a new podcast for the commute.',
  'Fix the squeaky door hinge with a bit of oil.',
  'Buy stamps for the holiday cards.',
  'The garden centre opens at eight on weekends.',
  'Tidy the desk drawer full of old cables.',
  'Seat reservations are worth it on the Friday train.',
  'The new cafe does a good flat white.',
  'Sign up for the community clean-up day.',
  'Write a thank-you note for the gift.',
]

# Values for the {{name}} placeholders in snippet bodies and titles.
fill_values = {
  'port': ['3000', '5000', '8000', '8080', '8081', '8443', '9000', '4000'],
  'service': ['orders', 'inventory', 'billing', 'catalog', 'notifier', 'reports',
              'search', 'scheduler', 'thumbnailer', 'mailer', 'gateway', 'ledger'],
  'project': ['garden-planner', 'recipe-box', 'trip-log', 'budget-buddy', 'bookshelf',
              'photo-sorter', 'habit-tracker', 'weather-dash', 'chore-wheel', 'tide-times',
              'run-stats', 'plant-water'],
  'pyver': ['3.9', '3.10', '3.11', '3.12'],
  'nodever': ['18', '20', '21'],
  'n': ['3', '5', '7', '10', '12', '20', '25', '50'],
  'dir': ['projects', 'work', 'src', 'code', 'dev', 'repos'],
  'city': ['Lisbon', 'Kyoto', 'Oslo', 'Porto', 'Krakow', 'Ghent', 'Bergen', 'Lyon',
           'Valencia', 'Tallinn', 'Ljubljana', 'Galway'],
  'host': ['app', 'web', 'staging', 'docs', 'shop', 'blog', 'status', 'files'],
  'color': ['#2b6cb0', '#2f855a', '#c05621', '#6b46c1', '#b83280', '#2c7a7b'],
  'branch': ['main', 'develop', 'feature/search', 'fix/date-format', 'release/1.4'],
}

# Pastes with a fixed body (code, configs, recipes, longer notes). Each has a
# few titles. {{name}} placeholders are filled from fill_values.
snippets = [
  {'titles': ['fizzbuzz', 'fizzbuzz in python', 'interview warmup'],
   'body': '''for i in range(1, 101):
    out = ''
    if i % 3 == 0:
        out += 'Fizz'
    if i % 5 == 0:
        out += 'Buzz'
    print(out or i)
'''},
  {'titles': ['sum a csv column', 'csv totals', 'python csv helper'],
   'body': '''import csv

def column_total(path, column):
    total = 0.0
    with open(path, newline='') as fh:
        for row in csv.DictReader(fh):
            try:
                total += float(row[column])
            except (KeyError, ValueError):
                continue
    return total

print(column_total('expenses.csv', 'amount'))
'''},
  {'titles': ['retry decorator', 'retry with backoff', 'python retry'],
   'body': '''import functools
import time

def retry(times={{n}}, delay=0.5, factor=2.0, errors=(Exception,)):
    def wrap(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except errors:
                    if attempt == times:
                        raise
                    time.sleep(wait)
                    wait *= factor
        return inner
    return wrap
'''},
  {'titles': ['dataclass example', 'python dataclasses', 'inventory item model'],
   'body': '''from dataclasses import dataclass, field

@dataclass
class Item:
    name: str
    price: float
    tags: list = field(default_factory=list)

    @property
    def label(self):
        return f'{self.name} ({self.price:.2f})'

items = [Item('mug', 8.5, ['kitchen']), Item('lamp', 24.0)]
for it in sorted(items, key=lambda i: i.price):
    print(it.label)
'''},
  {'titles': ['argparse skeleton', 'cli template', 'python cli starter'],
   'body': '''import argparse

def main():
    parser = argparse.ArgumentParser(description='Resize photos in a folder.')
    parser.add_argument('folder')
    parser.add_argument('--width', type=int, default=1200)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    print(f'would resize {args.folder} to {args.width}px' if args.dry_run
          else f'resizing {args.folder}')

if __name__ == '__main__':
    main()
'''},
  {'titles': ['flatten a nested list', 'flatten helper'],
   'body': '''def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], (5, 6)])))  # [1, 2, 3, 4, 5, 6]
'''},
  {'titles': ['word count', 'word frequency', 'top words in a file'],
   'body': '''import collections
import re

def top_words(path, n={{n}}):
    with open(path, encoding='utf-8') as fh:
        words = re.findall(r"[a-z']+", fh.read().lower())
    return collections.Counter(words).most_common(n)

for word, count in top_words('chapter1.txt'):
    print(f'{word:15} {count}')
'''},
  {'titles': ['timer context manager', 'how long did that take'],
   'body': '''import time
from contextlib import contextmanager

@contextmanager
def timed(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f'{label}: {time.perf_counter() - start:.3f}s')

with timed('sort'):
    sorted(range(1_000_000), reverse=True)
'''},
  {'titles': ['debounce', 'js debounce', 'debounce util'],
   'body': '''function debounce(fn, wait = 250) {
  let timer = null;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), wait);
  };
}

window.addEventListener('resize', debounce(() => {
  console.log('resized to', window.innerWidth);
}));
'''},
  {'titles': ['load json with fetch', 'async fetch example'],
   'body': '''async function loadForecast(city) {
  const res = await fetch(`/api/forecast?city=${encodeURIComponent(city)}`);
  if (!res.ok) {
    throw new Error(`forecast failed: ${res.status}`);
  }
  const data = await res.json();
  return data.days.map(d => ({ date: d.date, high: d.max, low: d.min }));
}

loadForecast('{{city}}').then(console.table).catch(console.error);
'''},
  {'titles': ['groupBy with reduce', 'group array by key'],
   'body': '''const groupBy = (list, key) =>
  list.reduce((acc, item) => {
    const k = typeof key === 'function' ? key(item) : item[key];
    (acc[k] ||= []).push(item);
    return acc;
  }, {});

const books = [
  { title: 'The Long Road', genre: 'travel' },
  { title: 'Small Gardens', genre: 'home' },
  { title: 'Night Trains', genre: 'travel' },
];
console.log(groupBy(books, 'genre'));
'''},
  {'titles': ['sleep in js', 'js utils', 'small helpers'],
   'body': '''export const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

export const clamp = (n, min, max) => Math.min(Math.max(n, min), max);

export const chunk = (arr, size) =>
  Array.from({ length: Math.ceil(arr.length / size) }, (_, i) =>
    arr.slice(i * size, i * size + size));

export const uniq = arr => [...new Set(arr)];
'''},
  {'titles': ['go hello server', 'minimal go http server'],
   'body': '''package main

import (
\t"fmt"
\t"log"
\t"net/http"
)

func main() {
\thttp.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
\t\tfmt.Fprintln(w, "ok")
\t})
\tlog.Println("listening on :{{port}}")
\tlog.Fatal(http.ListenAndServe(":{{port}}", nil))
}
'''},
  {'titles': ['read lines in go', 'go bufio scanner'],
   'body': '''package main

import (
\t"bufio"
\t"fmt"
\t"os"
)

func main() {
\tf, err := os.Open("notes.txt")
\tif err != nil {
\t\tpanic(err)
\t}
\tdefer f.Close()
\tscanner := bufio.NewScanner(f)
\tn := 0
\tfor scanner.Scan() {
\t\tn++
\t\tfmt.Printf("%4d  %s\\n", n, scanner.Text())
\t}
}
'''},
  {'titles': ['rust gcd', 'gcd in rust', 'rust practice'],
   'body': '''fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn lcm(a: u64, b: u64) -> u64 {
    a / gcd(a, b) * b
}

fn main() {
    let pairs = [(12, 18), (35, 14), (100, 75), ({{n}}, 30)];
    for (a, b) in pairs.iter() {
        println!("gcd({}, {}) = {}, lcm = {}", a, b, gcd(*a, *b), lcm(*a, *b));
    }
}
'''},
  {'titles': ['monthly sales query', 'sales by month sql', 'report query'],
   'body': '''SELECT date_trunc('month', o.created_at) AS month,
       count(*)                          AS orders,
       sum(o.total)                      AS revenue,
       round(avg(o.total), 2)            AS avg_order
FROM orders o
WHERE o.status = 'paid'
  AND o.created_at >= now() - interval '12 months'
GROUP BY 1
ORDER BY 1;
'''},
  {'titles': ['orders table', 'schema for orders', 'create table'],
   'body': '''CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status      TEXT NOT NULL DEFAULT 'pending',
    total       NUMERIC(10, 2) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX orders_customer_idx ON orders (customer_id);
CREATE INDEX orders_created_idx ON orders (created_at);
'''},
  {'titles': ['find duplicates sql', 'duplicate rows'],
   'body': '''-- rows that share the same sku
SELECT sku, count(*) AS copies
FROM products
GROUP BY sku
HAVING count(*) > 1
ORDER BY copies DESC;
'''},
  {'titles': ['backup script', 'nightly backup', 'tar backup'],
   'body': '''#!/usr/bin/env bash
set -euo pipefail

SRC="$HOME/{{dir}}"
DEST="/mnt/backup"
STAMP=$(date +%Y-%m-%d)

mkdir -p "$DEST"
tar -czf "$DEST/{{dir}}-$STAMP.tar.gz" -C "$HOME" {{dir}}
# keep the last 14 archives
ls -1t "$DEST"/{{dir}}-*.tar.gz | tail -n +15 | xargs -r rm --
echo "backup done: $DEST/{{dir}}-$STAMP.tar.gz"
'''},
  {'titles': ['lowercase filenames', 'rename files loop'],
   'body': '''#!/usr/bin/env bash
for f in *; do
  lower=$(echo "$f" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
  if [ "$f" != "$lower" ]; then
    mv -n -- "$f" "$lower"
  fi
done
'''},
  {'titles': ['biggest folders', 'disk usage top 10', 'where did my disk go'],
   'body': '''du -h --max-depth=1 ~ 2>/dev/null | sort -hr | head -n 10
df -h /
find ~/Downloads -type f -size +200M -printf '%s\\t%p\\n' | sort -nr | head
'''},
  {'titles': ['git aliases', 'my gitconfig', 'gitconfig'],
   'body': '''[alias]
    st = status -sb
    co = checkout
    br = branch --sort=-committerdate
    lg = log --oneline --graph --decorate -20
    amend = commit --amend --no-edit
    unstage = restore --staged
[pull]
    rebase = true
[init]
    defaultBranch = main
'''},
  {'titles': ['git cheatsheet', 'git commands I forget'],
   'body': '''git switch -c {{branch}}           # new branch
git restore --staged file.txt      # unstage
git stash push -m "wip"            # park changes
git stash pop
git log --oneline -- path/to/file  # history of one file
git rebase -i HEAD~3               # tidy last three commits
git cherry-pick abc1234
git reflog                         # find lost commits
git clean -nd                      # dry run before cleaning
'''},
  {'titles': ['center with flexbox', 'css centering', 'flex layout'],
   'body': '''.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.card {
  max-width: 32rem;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}
'''},
  {'titles': ['dark mode css', 'css variables theme'],
   'body': ''':root {
  --bg: #ffffff;
  --fg: #1a202c;
  --accent: {{color}};
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a202c;
    --fg: #e2e8f0;
  }
}

body {
  background: var(--bg);
  color: var(--fg);
}
a { color: var(--accent); }
'''},
  {'titles': ['Dockerfile', 'python dockerfile', 'Dockerfile for {{service}}'],
   'body': '''FROM python:{{pyver}}-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE {{port}}
CMD ["gunicorn", "-b", "0.0.0.0:{{port}}", "app:app"]
'''},
  {'titles': ['docker compose', 'compose file', 'local dev compose'],
   'body': '''services:
  {{service}}:
    build: .
    ports:
      - "{{port}}:{{port}}"
    depends_on:
      - db
      - cache
    volumes:
      - ./:/app
  db:
    image: postgres:16
    volumes:
      - dbdata:/var/lib/postgresql/data
  cache:
    image: redis:7

volumes:
  dbdata:
'''},
  {'titles': ['nginx reverse proxy', 'nginx site config', 'nginx conf'],
   'body': '''server {
    listen 80;
    server_name {{host}}.example.com;

    location /static/ {
        alias /srv/{{project}}/static/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:{{port}};
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
'''},
  {'titles': ['systemd unit', 'service file', '{{service}}.service'],
   'body': '''[Unit]
Description={{service}} worker
After=network.target

[Service]
Type=simple
User=app
WorkingDirectory=/srv/{{service}}
ExecStart=/srv/{{service}}/venv/bin/python -m {{service}}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
'''},
  {'titles': ['.gitignore', 'gitignore for node', 'node gitignore'],
   'body': '''node_modules/
dist/
coverage/
.cache/
*.log
.DS_Store
.idea/
.vscode/
'''},
  {'titles': ['.editorconfig', 'editorconfig'],
   'body': '''root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
'''},
  {'titles': ['Makefile', 'makefile for python project'],
   'body': '''.PHONY: install test lint run

install:
\tpython -m venv .venv
\t.venv/bin/pip install -r requirements.txt

test:
\t.venv/bin/pytest -q

lint:
\t.venv/bin/ruff check .

run:
\t.venv/bin/flask --app {{project}} run --port {{port}}
'''},
  {'titles': ['ci workflow', 'ci yaml', 'test workflow'],
   'body': '''name: tests
on:
  push:
    branches: [{{branch}}]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "{{pyver}}"
      - run: pip install -r requirements.txt
      - run: pytest -q
'''},
  {'titles': ['pyproject.toml', 'pyproject', 'package metadata'],
   'body': '''[project]
name = "{{project}}"
version = "0.4.2"
requires-python = ">={{pyver}}"
dependencies = [
  "flask>=3.0",
  "requests>=2.31",
]

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[tool.ruff]
line-length = 100
'''},
  {'titles': ['package.json', 'npm scripts'],
   'body': '''{
  "name": "{{project}}",
  "version": "1.2.0",
  "private": true,
  "type": "module",
  "engines": { "node": ">={{nodever}}" },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest run",
    "lint": "eslint src"
  }
}
'''},
  {'titles': ['tmux.conf', 'tmux config'],
   'body': '''set -g mouse on
set -g base-index 1
set -g history-limit 50000
set -g status-style bg=default
bind r source-file ~/.tmux.conf \\; display "reloaded"
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
'''},
  {'titles': ['vimrc', 'minimal vimrc'],
   'body': '''set number relativenumber
set expandtab shiftwidth=4 tabstop=4
set ignorecase smartcase
set incsearch hlsearch
set clipboard=unnamedplus
syntax on
filetype plugin indent on
let mapleader = ","
'''},
  {'titles': ['crontab', 'my cron jobs'],
   'body': '''# m h dom mon dow command
15 2 * * *   /home/app/bin/backup.sh >> /var/log/backup.out 2>&1
*/10 * * * * /home/app/bin/sync-photos.sh
0 7 * * 1    /home/app/bin/weekly-report.sh
@reboot      /home/app/bin/mount-shares.sh
'''},
  {'titles': ['regex cheatsheet', 'regex notes'],
   'body': '''^        start of line
$        end of line
\\d       digit        \\D not a digit
\\w       word char    \\W not a word char
\\s       whitespace
[a-z]    range        [^a-z] anything but
a*  a+  a?   zero+, one+, optional
a{2,4}   between two and four
(?:...)  group without capture
(?=...)  lookahead
'''},
  {'titles': ['README template', 'readme skeleton'],
   'body': '''# {{project}}

Small tool for keeping track of things around the house.

## Setup

    python -m venv .venv
    .venv/bin/pip install -r requirements.txt

## Usage

    .venv/bin/python -m {{project}} --help

## Notes

- data lives in data/ as plain CSV
- nothing is sent anywhere
'''},
  {'titles': ['feature flags json', 'settings.json', 'app settings'],
   'body': '''{
  "theme": "system",
  "language": "en",
  "pageSize": {{n}},
  "features": {
    "newEditor": true,
    "weeklyDigest": false,
    "betaCharts": true
  },
  "accentColor": "{{color}}"
}
'''},
  {'titles': ['k8s deployment', 'deployment.yaml', 'kubernetes manifest'],
   'body': '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{service}}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {{service}}
  template:
    metadata:
      labels:
        app: {{service}}
    spec:
      containers:
        - name: {{service}}
          image: registry.example.com/{{service}}:1.8.3
          ports:
            - containerPort: {{port}}
          resources:
            limits:
              memory: 256Mi
              cpu: 250m
'''},
  {'titles': ['java hello', 'temperature converter java'],
   'body': '''public class Convert {
    static double toFahrenheit(double c) {
        return c * 9 / 5 + 32;
    }

    public static void main(String[] args) {
        for (int c = -10; c <= 40; c += 10) {
            System.out.printf("%4d C = %6.1f F%n", c, toFahrenheit(c));
        }
    }
}
'''},
  {'titles': ['neovim keymaps', 'init.lua snippet'],
   'body': '''vim.g.mapleader = ' '
local map = vim.keymap.set
local tb = require('telescope.builtin')
map('n', ' ff', tb.find_files)
map('n', ' fg', tb.live_grep)
map('n', ' e', vim.cmd.Explore)
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.tabstop = 4
'''},
  {'titles': ['powershell big files', 'find large files windows'],
   'body': '''Get-ChildItem -Path $HOME -Recurse -File -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending |
  Select-Object -First {{n}} FullName, @{Name='MB'; Expression={[math]::Round($_.Length / 1MB, 1)}}
'''},
  {'titles': ['spreadsheet formulas', 'excel formulas I use'],
   'body': '''=SUMIFS(C:C, A:A, ">="&DATE(2024,1,1), B:B, "groceries")
=XLOOKUP(E2, A:A, C:C, "not found")
=TEXT(A2, "yyyy-mm")
=IFERROR(B2/C2, 0)
=UNIQUE(FILTER(A2:A200, B2:B200="open"))
=ROUND(AVERAGE(D2:D31), 1)
'''},
  {'titles': ['unit conversions', 'kitchen conversions'],
   'body': '''1 cup flour     ~ 120 g
1 cup sugar     ~ 200 g
1 cup butter    ~ 225 g
1 tbsp          = 15 ml
1 tsp           = 5 ml
180 C           = 350 F
200 C           = 400 F
1 oz            ~ 28 g
'''},
  {'titles': ['pancakes', 'Saturday pancakes', 'pancake recipe'],
   'body': '''Pancakes (makes about 10)

200 g flour
2 tsp baking powder
1 tbsp sugar
pinch of salt
2 eggs
300 ml milk
30 g melted butter

Method:
1. Whisk the dry things together.
2. Beat eggs with milk and butter, pour into the dry mix, stir until just combined.
3. Rest 10 minutes.
4. Medium heat, a little butter, about 3 tbsp batter per pancake.
5. Flip when bubbles appear. Serve with fruit or syrup.
'''},
  {'titles': ['banana bread', 'banana bread recipe'],
   'body': '''Banana bread

3 very ripe bananas
75 g melted butter
150 g brown sugar
1 egg
1 tsp vanilla
1 tsp baking soda
pinch of salt
190 g flour
handful of walnuts (optional)

Mash bananas, stir in butter, sugar, egg and vanilla.
Add soda, salt and flour, fold until no dry bits remain.
Loaf tin, 175 C for 55-60 minutes. Cool before slicing.
'''},
  {'titles': ['chili', 'vegetable chili', 'big pot chili'],
   'body': '''Vegetable chili (serves 6)

2 onions, chopped
3 garlic cloves
2 peppers, diced
2 tsp cumin, 1 tsp smoked paprika, chili flakes to taste
2 tins chopped tomatoes
2 tins beans (kidney + black), drained
1 tin sweetcorn
1 square dark chocolate

Soften onions 10 min, add garlic and peppers, then spices for a minute.
Add tomatoes, beans and a splash of water. Simmer 40 minutes.
Stir in corn and chocolate at the end. Better the next day.
'''},
  {'titles': ['guacamole', 'guac'],
   'body': '''2 ripe avocados
1/2 small red onion, very finely chopped
1 tomato, seeds out, diced
juice of 1 lime
handful of coriander
salt

Mash avocado with lime and salt, keep it a bit chunky.
Fold in onion, tomato and coriander. Taste, add more lime.
'''},
  {'titles': ['overnight oats', 'breakfast prep'],
   'body': '''Overnight oats (one jar)

50 g oats
150 ml milk
2 tbsp yoghurt
1 tsp chia seeds
1 tsp honey
berries on top

Mix everything except berries, lid on, fridge overnight.
Add berries in the morning.
'''},
  {'titles': ['tomato soup', 'roast tomato soup'],
   'body': '''Roast tomato soup

1 kg tomatoes, halved
1 red onion, quartered
4 garlic cloves, unpeeled
olive oil, salt, pepper
500 ml vegetable stock
basil

Roast tomatoes, onion and garlic at 200 C for 35 minutes.
Squeeze garlic out of skins, blend everything with stock.
Season, warm through, basil on top.
'''},
  {'titles': ['pesto pasta', 'quick pesto'],
   'body': '''Pesto

1 big bunch basil
1 garlic clove
40 g pine nuts, toasted
40 g parmesan
100 ml olive oil
squeeze of lemon

Blitz everything except oil, then stream in oil.
Toss with pasta and a splash of the cooking water.
'''},
  {'titles': ['chocolate chip cookies', 'cookie recipe'],
   'body': '''Cookies (about 16)

115 g soft butter
100 g brown sugar
50 g white sugar
1 egg
1 tsp vanilla
180 g flour
1/2 tsp baking soda
1/2 tsp salt
150 g chocolate chips

Cream butter and sugars, beat in egg and vanilla.
Stir in flour, soda and salt, then chips.
Chill 30 min. Bake at 180 C for 10-12 min, edges golden, middles soft.
'''},
  {'titles': ['lentil curry', 'dal', 'weeknight dal'],
   'body': '''Red lentil dal

200 g red lentils, rinsed
1 onion, 2 garlic cloves, thumb of ginger
1 tsp turmeric, 1 tsp cumin seeds, 1 tsp garam masala
1 tin coconut milk
400 ml water
spinach, lime

Fry cumin seeds, then onion until soft, then garlic and ginger.
Add turmeric, lentils, coconut milk and water. Simmer 20-25 minutes.
Stir in garam masala and spinach. Lime to finish.
'''},
  {'titles': ['cold brew', 'cold brew ratio'],
   'body': '''Cold brew concentrate

100 g coarse ground coffee
800 ml cold water

Stir, cover, leave on the counter 14-16 hours.
Strain through a paper filter.
Dilute 1:1 with water or milk. Keeps a week in the fridge.
'''},
  {'titles': ['focaccia', 'easy focaccia'],
   'body': '''Focaccia

500 g bread flour
400 ml warm water
7 g instant yeast
10 g salt
olive oil, flaky salt, rosemary

Mix flour, water, yeast and salt into a sticky dough. Rest 30 min.
Four sets of stretch and folds, 30 min apart.
Oiled tray, stretch to fit, rise 1 hour.
Dimple with oily fingers, top with salt and rosemary.
230 C for 20-25 minutes.
'''},
  {'titles': ['weekly workout plan', 'training plan', 'gym schedule'],
   'body': '''Mon - easy run 30 min
Tue - upper body: push-ups 3x12, rows 3x10, shoulder press 3x10
Wed - rest or walk
Thu - intervals: 6 x 400 m, 90 s rest
Fri - lower body: squats 3x10, lunges 3x8 each, deadlifts 3x8
Sat - long run, slow, 60-75 min
Sun - stretching / yoga 20 min
'''},
  {'titles': ['garden planting schedule', 'what to sow when', 'veg patch plan'],
   'body': '''March   - sow tomatoes and peppers indoors, chit potatoes
April   - plant first early potatoes, sow peas, salad leaves
May     - harden off tomatoes, sow beans and courgettes
June    - plant out squash, keep sowing lettuce every 2 weeks
July    - feed tomatoes weekly, pinch out side shoots
August  - harvest, sow winter salad
Sept    - plant garlic at the end of the month
'''},
  {'titles': ['trip to {{city}}', '{{city}} itinerary', 'weekend in {{city}}'],
   'body': '''Day 1
- arrive around noon, drop bags at the guesthouse
- walk the old town, find lunch near the market
- sunset from the viewpoint above the river

Day 2
- museum in the morning (closed Mondays)
- tram out to the beach / park
- dinner: the small place with the set menu

Day 3
- bakery breakfast, last souvenirs
- train back at 15:40
'''},
  {'titles': ['session notes', 'campaign notes', 'game night notes'],
   'body': '''Session 7

- party reached the lighthouse at dusk
- the keeper wants the missing lens found before the storm
- Bram traded the silver compass for a map of the caves
- Wren is still cursed (disadvantage on stealth)
- next time: caves under the cliffs, bring rope and torches
'''},
  {'titles': ['book notes', 'reading notes', 'chapter summary'],
   'body': '''Notes - "Small Habits, Long Roads"

ch1: start with something so small you cannot say no to it
ch2: tie new habits to things you already do (after coffee, before bed)
ch3: track it, but forgive missed days; never miss twice
ch4: environment beats willpower - put the guitar on a stand
ch5: progress is boring in the middle, keep going
'''},
  {'titles': ['plant care', 'plant watering schedule', 'houseplants'],
   'body': '''monstera      - water when top 3 cm dry, bright indirect light
snake plant   - every 2-3 weeks, can take low light
pothos        - weekly, trim leggy vines
fiddle leaf   - do not move it, water weekly, wipe leaves
herbs (sill)  - basil daily in summer, rosemary drier
'''},
  {'titles': ['poem draft', 'a few lines', 'untitled poem'],
   'body': '''morning on the platform
the fog is still deciding
whether to be rain

a dog in a yellow coat
sits as if it bought a ticket
and knows the stop
'''},
  {'titles': ['moving checklist', 'moving house'],
   'body': '''[ ] book the van for the 14th
[ ] change address with the bank and the doctor
[ ] meter readings on the day
[ ] label boxes by room
[ ] keep a box of essentials: kettle, mugs, chargers, towels
[ ] measure the doorway for the sofa
[ ] return keys to the agency
'''},
  {'titles': ['wedding speech draft', 'toast draft'],
   'body': '''Good evening everyone.

For those who do not know me, I have known the groom since we were both
terrible at football in the same school team.

He is the friend who shows up with soup when you are sick
and a ladder when you are moving.

So please raise your glasses: to long walks, good soup
and a very happy life together.
'''},
  {'titles': ['standup update', 'status update', 'weekly update'],
   'body': '''Done
- migrated {{service}} settings page to the new layout
- fixed date formatting on exported reports

Doing
- pagination for the search results
- review of the onboarding copy

Blocked
- waiting on design for the empty states
'''},
  {'titles': ['release notes', 'changelog', 'CHANGELOG'],
   'body': '''## 1.4.0

### Added
- dark theme follows the system setting
- export to CSV from the reports page

### Changed
- faster startup when the library is large
- clearer error when a file cannot be read

### Fixed
- dates near midnight showed the wrong day
- scroll position lost after closing a dialog
'''},
  {'titles': ['interview questions', 'questions to ask'],
   'body': '''Questions to ask them

- what does a normal week look like?
- how is work planned and who decides priorities?
- how do you handle on-call / weekend work?
- what did the last person in this role move on to?
- what would success look like after six months?
'''},
  {'titles': ['keyboard shortcuts', 'shortcuts I keep forgetting'],
   'body': '''Ctrl+Shift+T   reopen closed tab
Ctrl+L         focus address bar
Ctrl+Shift+V   paste without formatting
Win+Shift+S    screenshot region
Alt+Tab        switch window
Ctrl+Alt+T     terminal
Ctrl+R         search shell history
'''},
]
