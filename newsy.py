import os, sys, json, datetime, hashlib, multiprocessing, math, time
import newspaper, rethinkdb
import shared.config

config = shared.config.load('newsy.ini')

NEWS_DIRECTORY = config['Disk']['NewsPath']
DOWNLOAD_URL_ROOT = config['Disk']['LocalNewsHost']

DB_HOST = config['Database']['Host']
DB_PORT = int(config['Database']['Port'])
DB_DB = config['Database']['Db']
DB_TABLE_NEWS = config['Database']['NewsTable']

NUM_PROCESSES = 4
SLEEP_TIME = 60     # seconds

## Connect to RethinkDB, where article metadata will be stored
"""
Container class for all infomration stored in the news table for a given
article.
"""
class ArticleMetadata(object):
    def __init__(self, article, source):
        h = hashlib.sha256()
        h.update(article.title.encode('utf-8'))

        self.id = h.hexdigest()
        self.title = article.title
        self.authors = article.authors
        self.source = source['source']
        self.url = source['url']
        
        self.published = article.publish_date.isoformat() if article.publish_date else None
        self.added = datetime.datetime.now().isoformat()
        self.filename = source['_id']

## Read, parse, and extract information from the specified HTML file.
def extract(filename, source):
    article = newspaper.Article('{}/{}'.format(DOWNLOAD_URL_ROOT, filename))

    try:
        article.download()
        article.parse()

        return ArticleMetadata(article, source), article.text
    except:
        print('Parse error for article {}'.format(filename))
        return

def writeContent(filename, content):
    with open(filename + '.txt', 'w') as fp:
        fp.write(content)

def writeRecord(db, metadata):
    return rethinkdb.db(DB_DB).table(DB_TABLE_NEWS).insert(metadata.__dict__, conflict="update").run(db)

"""
Subprocess that processes each article in serial. This process is designed to be 
parallelizable and is kicked off NUM_PROCESSES times below. It receives a shared queue
as an input that serves as a task queue.
"""
def handle_article(q, pid):
    md = rethinkdb.connect(DB_HOST, DB_PORT)

    while True:
        article = q.get()
        filename = '{}.html'.format(article['_id'])

        try:
            metadata, content = extract(filename, article)
            # First choice: publication timestamp from story. 
            # Fallback: value from API
            if metadata.published is None:
                metadata.published = article['publishedAt']
    
            # Ensure that the body isn't empty before saving this record. 
            # It's possible that we might get HTML but not be able to extract 
            # any text. In this case, we're currently electing to throw the 
            # article out since there's not going to be much we can learn from it.
            if len(content) > 0:
                writeContent(NEWS_DIRECTORY + filename, content)
                writeRecord(md, metadata)
        except Exception as e:
            print('Difficulty parsing article {}'.format(article['_id']))
        
## Load target files from news.json 
articles = multiprocessing.Queue()
added = set()

print('Launching child processes...')
for i in range(0, NUM_PROCESSES):
    p = multiprocessing.Process(target=handle_article, args=(articles, i))
    p.start()

print('Processing news stories...')
while True:
    print('Reading news stories...')
    count = 0

    with open(NEWS_DIRECTORY[:-1] + '.json') as fp:
        raw = json.loads(fp.read())['records']

        for article in raw:
            if article['_id'] not in added:
                added.add(article['_id'])
                articles.put(article)

                count += 1

    print('Added {} stories.'.format(count))
    time.sleep(SLEEP_TIME)