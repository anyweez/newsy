import rethinkdb, sys, nltk
import static.countries as static
# from nltk.text import TextCollection

# Returns a generator
def next_record():
    md = rethinkdb.connect('historian', 28015)
    cursor = rethinkdb.db('news').table('metadata').run(md)

    for doc in cursor:
        try:
            path = doc['filepath'].replace('/home', '/Users') + '.txt'
            with open(path) as fp:
                yield doc, fp.read()
        except:
            pass

def update_record():
    md = rethinkdb.connect('historian', 28015)

    def add(record):
        print(rethinkdb.db('news').table('metadata').insert(record, conflict="update").run(md))

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
        # print(doc['title'])
        # print(countries)
        found += 1

    attempts += 1

    add_labels(doc, 'countries', countries)
    # if attempts > 40:
    #     sys.exit(0)

print(found / attempts)