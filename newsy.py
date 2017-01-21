import os, sys, json, datetime, hashlib, lxml
import newspaper, rethinkdb

NEWS_DIRECTORY = sys.argv[1] + '/'
DOWNLOAD_URL_ROOT = 'http://localhost:3000/'

## Connect to RethinkDB, where article metadata will be stored
md = rethinkdb.connect('historian', 28015)
# rethinkdb

class ArticleMetadata(object):
    def __init__(self, article, path):
        h = hashlib.sha256()
        h.update(article.title.encode('utf-8'))

        self.id = h.hexdigest()
        self.title = article.title
        self.authors = article.authors
        self.source = None
        
        self.published = article.publish_date.isoformat() if article.publish_date else None
        self.added = datetime.datetime.now().isoformat()
        self.filepath = path


## Read, parse, and extract information from the specified HTML file.
def extract(filename):
    article = newspaper.Article(DOWNLOAD_URL_ROOT + filename)

    article.download()
    article.parse()
    return 1, 2

    # return ArticleMetadata(article, NEWS_DIRECTORY + filename), article.text

def writeContent(filename, content):
    with open(filename + '.txt', 'w') as fp:
        fp.write(content)

def writeRecord(metadata):
    return rethinkdb.db('news').table('metadata').insert(metadata.__dict__, conflict="update").run(md)

## Load target files from news.json 
articles = []

with open(NEWS_DIRECTORY[:-1] + '.json') as fp:
   articles = json.loads(fp.read())['records']

## Get all filename for the news directory
# fn = ['{}.html'.format(article['_id']) for article in articles]

for article in articles[:5]:
    filename = '{}.html'.format(article['_id'])

    print(filename)

    try:
        metadata, content = extract(filename)
        # writeContent(NEWS_DIRECTORY + filename, content)
        # writeRecord(metadata)
    except:
        print('Difficulty parsing article ' + article['_id'])
