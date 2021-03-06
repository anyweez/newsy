import json, argparse, random, rethinkdb, re, pprint, arrow
import shared.config, utils.metrics, utils.groups

"""
Annotates a GeoJSON file with a metric. The specific metric can be specified by:
    - The base group (BASE_GROUP)
    - The compare group (COMPARE_GROUP)
    - The metric for comparison (METRIC_NAME)

For example, comparing 60_to_120_days_ago (base group) to now (compare group) using
the metric count_diff. All grouping / filtering functions are stored in utils.groups
and all metric computation functions are stored in utils.metrics.

This script also generates a set of output articles that should be displayed to 
contextualize the metric. Currently these are the 10 most recent articles from the 
compare group for each country.
"""

config = shared.config.load('newsy.ini')

# DB configuration information
DB_HOST = config['Database']['Host']
DB_PORT = int(config['Database']['Port'])
DB_DB = config['Database']['Db']
DB_TABLE_NEWS = config['Database']['NewsTable']

OUTPUT_BY_COUNTRY = config['Disk']['ArticlesByCountry']

# TODO: read these from cmd line params
BASE_GROUP = '25_to_35_days_ago'
COMPARE_GROUP = 'now_to_10_days_ago'
METRIC_NAME = 'rel_articles_per_day'

FILTER_BASE_GROUP = None        # Derived from groups[BASE_GROUP]
FILTER_COMPARE_GROUP = None     # Derived from groups[COMPARE_GROUP]

groups = {
    '([0-9]+)_to_([0-9]+)_days_ago': utils.groups.DAY_to_DAY_days_ago,
    'now_to_([0-9]+)_days_ago': utils.groups.now_to_DAY_days_ago
}

metrics = {
    'count_diff': utils.metrics.count_diff,
    'rel_articles_per_day': utils.metrics.rel_articles_per_day
}

geo = {}
mapping = {}

def wrap_group(groups, fn):
    def filter_group(c):
        return fn(c, *groups)
    
    return filter_group

## Make sure both group selectors are valid and store the functions
## that can be used to filter the record stream
for pattern, func in groups.items():
    match = re.search(pattern, BASE_GROUP)
    if match is not None:
        print('Base group matches ' + pattern)
        FILTER_BASE_GROUP = wrap_group(match.groups(), func)
    
    match = re.search(pattern, COMPARE_GROUP)
    if match is not None:
        print('Compare group matches ' + pattern)
        FILTER_COMPARE_GROUP = wrap_group(match.groups(), func)

## Load the GeoJSON file that we want to be annotating
with open(config['BaseData']['CountriesGeo']) as fp:
    geo = json.loads(fp.read())

## Load a mapping between country names and ID's in the GeoJSON file.
with open(config['BaseData']['CountriesMapping']) as fp:
    mapping = json.loads(fp.read())
    reverse_mapping = { name: code for code, name in mapping.items() }

## Read in all records and filter to make base and compare
group_base = []
group_compare = []

md = rethinkdb.connect(DB_HOST, DB_PORT)
cursor = rethinkdb.db(DB_DB).table(DB_TABLE_NEWS).run(md)

for doc in cursor:
    if FILTER_BASE_GROUP(doc):
        group_base.append(doc)

    if FILTER_COMPARE_GROUP(doc):
        group_compare.append(doc)

print('Base group size: {}'.format(len(group_base)))
print('Compare group size: {}'.format(len(group_compare)))

## Annotate the original GeoJSON file with new metrics
result = metrics[METRIC_NAME](group_base, group_compare)

for i, feature in enumerate(geo['features']):
    try:
        country = mapping[feature['id']]

        geo['features'][i]['properties']['diff'] = result[country] if country in result else None
        geo['features'][i]['properties']['id'] = feature['id']
    except KeyError:
        pass

# TODO: read filename from command line params
with open('annotated.json', mode='w') as fp:
    fp.write(json.dumps(geo))

recent = filter(lambda x: (arrow.now() - arrow.get(x['published'])).days < 2, group_compare)
recent = filter(lambda x: 'labels' in x, recent)

"""
Convert stored article objects to a public format containing just the essential info.
"""
def publish(article):
    # Currently choosing top country from list. Need to get smarter about this.
    country_name = article['labels']['countries'][0]

    return {
        'title': article['title'],
        'url': article['url'],
        'published': article['published'],
        'country': {
            'name': country_name,
            'performance': result[country_name],
        },
        'source': {
            'name': article['source']
        }
    }

recent = map(publish, recent)
recent = sorted(recent, key=lambda x: x['published'], reverse=True)

with open('{}/articles.json'.format(OUTPUT_BY_COUNTRY), 'w') as fp:
    fp.write(json.dumps(recent))
    print('Wrote articles.json')