import rethinkdb, sys, nltk, os, argparse, json
import static.countries as static
import shared.config
import shared.labels as labels
import labeler

## Load the core newsy configuration and start initializing the database connection, 
## the labeler, and any other information that'll be required to get the job done.
config = shared.config.load('newsy.ini')

NEWS_FILE_PATH = config['Disk']['NewsPath'] + config['Disk']['ExtractPattern']
DB_HOST = config['Database']['Host']
DB_PORT = int(config['Database']['Port'])
DB_DB = config['Database']['Db']
DB_TABLE_NEWS = config['Database']['NewsTable']

"""
Users can specify the labeling plugin to use via the command line; the default is 
currently 'explicit'. Performance stats will be produced at the end, which can be 
compared across various executions.
"""
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--using', help='the labeling plugin to use', default='explicit')
arg_parser.add_argument('--no-write', dest='write_to_db', action='store_false', default=True)
arg_parser.add_argument('--write-to', dest='table_name', help='the table name labels should be written to', default=DB_TABLE_NEWS)
cmd_args = arg_parser.parse_args()

# Returns a generator
def next_record():
    md = rethinkdb.connect(DB_HOST, DB_PORT)
    cursor = rethinkdb.db(DB_DB).table(cmd_args.table_name).run(md)

    for doc in cursor:
        try:
            with open(NEWS_FILE_PATH.format(doc['filename'])) as fp:
                yield doc, fp.read()
        except:
            print('File not found: {}'.format(NEWS_FILE_PATH.format(doc['filename'])))
            pass

"""
Action for writing the record to the database. If database writes have been disabled,
simply returns a no-op function.
"""
def update_record():
    def noop(record):
        pass

    if not cmd_args.write_to_db:
        return noop
    else:
        md = rethinkdb.connect(DB_HOST, DB_PORT)

        def add(record):
            rethinkdb.db(DB_DB).table(cmd_args.table_name).insert(record, conflict='update').run(md)

        return add

gen = next_record()
update = update_record()

results = { 'attempts': 0, 'found': 0, 'pct': 0.0 }

# Prepare the specified labeling algorithm
find_countries = labeler.prepare_algo(cmd_args.using)

## Process each individual record. The tighter we can keep this loop the better.
for doc, text in next_record():
    tokens = nltk.word_tokenize(text)
    countries = find_countries.search(tokens)

    if len(countries) > 0:
        labels.add(doc, 'countries', countries)
        update(doc) # db insert

print(json.dumps(find_countries.stats.__dict__))