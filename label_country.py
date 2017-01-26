import rethinkdb, sys, nltk, os
import static.countries as static
# from nltk.text import TextCollection

NEWS_FILE_PATH = os.environ['HOME'] + '/git/scraper/news/{}.html.txt'

# Returns a generator
def next_record():
    md = rethinkdb.connect('historian', 28015)
    cursor = rethinkdb.db('news').table('metadata').run(md)

    for doc in cursor:
        try:
#            path = doc['filepath'].replace('/home', '/Users') + '.txt'
            with open(NEWS_FILE_PATH.format(doc['filename'])) as fp:
                yield doc, fp.read()
        except:
            print(NEWS_FILE_PATH.format(doc['filename']))
            pass

def update_record():
    md = rethinkdb.connect('historian', 28015)

    def add(record):
        rethinkdb.db('news').table('metadata').insert(record, conflict="update").run(md)

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

print(found / attempts)
