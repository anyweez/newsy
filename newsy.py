import os, sys, json, datetime, hashlib, multiprocessing, math
import newspaper, rethinkdb
import shared.config

config = shared.config.load('newsy.ini')

NEWS_DIRECTORY = config['Disk']['NewsPath']
DOWNLOAD_URL_ROOT = config['Disk']['LocalNewsHost']

DB_HOST = config['Database']['Host']
DB_PORT = int(config['Database']['Port'])
DB_DB = config['Database']['Db']
DB_TABLE_NEWS = config['Database']['NewsTable']

NUM_PROCESSES=4

## Connect to RethinkDB, where article metadata will be stored

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

def handle_article(article_list):
    md = rethinkdb.connect(DB_HOST, DB_PORT)

    for article in article_list:
        filename = '{}.html'.format(article['_id'])

        try:
            metadata, content = extract(filename, article)
            writeContent(NEWS_DIRECTORY + filename, content)
            writeRecord(md, metadata)
        except Exception as e:
            print('Difficulty parsing article {}'.format(article['_id']))
        
## Load target files from news.json 
articles = []

print('Reading news stories...')
with open(NEWS_DIRECTORY[:-1] + '.json') as fp:
   articles = json.loads(fp.read())['records']

## Iterate over each, one at a time, and parse. Create metadata records for
## each story.
segment_length = math.ceil(len(articles) / NUM_PROCESSES)
jobs = []

print('Launching child processes...')
for i in range(0, NUM_PROCESSES):
    start = segment_length * i
    end = segment_length * (i + 1)

    p = multiprocessing.Process(target=handle_article, args=(articles[start:end],))
    jobs.append(p)
    p.start()

print('Processing news stories...')
for job in jobs:
    job.join()