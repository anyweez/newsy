import os, sys, json, datetime, hashlib, lxml
import newspaper, rethinkdb

NEWS_DIRECTORY = sys.argv[1] + '/'
DOWNLOAD_URL_ROOT = 'http://localhost:3000/'

## Connect to RethinkDB, where article metadata will be stored
md = rethinkdb.connect('historian', 28015)
# rethinkdb

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
    article = newspaper.Article(DOWNLOAD_URL_ROOT + filename)

    article.download()
    article.parse()
    
    return ArticleMetadata(article, source), article.text

def writeContent(filename, content):
    with open(filename + '.txt', 'w') as fp:
        fp.write(content)

def writeRecord(metadata):
    return rethinkdb.db('news').table('metadata').insert(metadata.__dict__, conflict="update").run(md)

## Load target files from news.json 
articles = []

with open(NEWS_DIRECTORY[:-1] + '.json') as fp:
   articles = json.loads(fp.read())['records']

## Iterate over each, one at a time, and parse. Create metadata records for
## each story.
for i, article in enumerate(articles):
    filename = '{}.html'.format(article['_id'])

    try:
        metadata, content = extract(filename, article)
        writeContent(NEWS_DIRECTORY + filename, content)
        writeRecord(metadata)
    except Exception as e:
        print('Difficulty parsing article ' + article['_id'])
        print(e)
    
    sys.stdout.write('{} / {}\r'.format(i + 1, len(articles)))
