import rethinkdb, sys, nltk, os
import static.countries as static
import shared.config
# import shared.labels as labels

config = shared.config.load('newsy.ini')

NEWS_FILE_PATH = config['Disk']['NewsPath'] + config['Disk']['ExtractPattern']
DB_HOST = config['Database']['Host']
DB_PORT = int(config['Database']['Port'])
DB_DB = config['Database']['Db']
DB_TABLE_NEWS = config['Database']['NewsTable']

# Returns a generator
def next_record():
    md = rethinkdb.connect(DB_HOST, DB_PORT)
    cursor = rethinkdb.db(DB_DB).table(DB_TABLE_NEWS).run(md)

    for doc in cursor:
        try:
            with open(NEWS_FILE_PATH.format(doc['filename'])) as fp:
                yield doc, fp.read()
        except:
            print('File not found: {}'.format(NEWS_FILE_PATH.format(doc['filename'])))
            pass

def update_record():
    md = rethinkdb.connect(DB_HOST, DB_PORT)

    def add(record):
        rethinkdb.db(DB_DB).table(DB_TABLE_NEWS).insert(record, conflict="update").run(md)

    return add

def add_labels(record, label, values):
    if 'labels' not in record:
        record['labels'] = {}
    record['labels'][label] = values

gen = next_record()
update = update_record()

attempts = 0
found = 0

for doc, text in next_record():
    tokens = nltk.word_tokenize(text)
    countries = static.find_countries(tokens)

    if len(countries) > 0:
        add_labels(doc, 'countries', countries)
        update(doc)

        found += 1

    attempts += 1

print('Coverage: {}'.format(found / attempts))
