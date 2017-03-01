"""
This script compares the performance of two different labeling algorithms
across a handful of important metrics. It runs each of the labelers on all
articles in the database so that the stats are relevant to the real dataset.

Global stats include:
    Truth set size (absolute and as a %)

Labeler stats include:
    Coverage (% with labels)
    Hits (#)
    Misses (#)
    Precision (% correctly labeled)
"""

import sys, rethinkdb, string, random, subprocess, tabulate
import shared.config, shared.labels

if len(sys.argv) is not 3:
    print('Usage: python3 compare.py <base> <compare>')
    sys.exit(1)

[base, compare] = sys.argv[1:3]

config = shared.config.load('newsy.ini')

DB_HOST = config['Database']['Host']
DB_PORT = int(config['Database']['Port'])
DB_DB = config['Database']['Db']
DB_TABLE_NEWS = config['Database']['NewsTable']
DB_TABLE_FEEDBACK = config['Database']['LabelTable']

md = rethinkdb.connect(DB_HOST, DB_PORT)

# 1. Stream all records existing table to two new temporary tables
# TODO: RethinkDB has built-in import commands that'd probably be a good bit faster
def clone_table(new_tables):
    cursor = rethinkdb.db(DB_DB).table(DB_TABLE_NEWS).run(md)

    # Create the new tables
    for table in new_tables:
        rethinkdb.db(DB_DB).table_create(table).run(md)

    count = 0
    # Copy content from old to new
    for article in cursor:
        count += 1
        for target in new_tables:
            rethinkdb.db(DB_DB).table(target).insert(article, conflict="update").run(md)

    return count

def load_truth():
    docs = [doc for doc in rethinkdb.db(DB_DB).table(DB_TABLE_FEEDBACK).run(md)]

    # Create a mapping between the doc id and the results
    mapping = {}
    for feedback in docs:
        if feedback['docid'] in mapping:
            mapping[feedback['docid']].append(feedback)
        else:
            mapping[feedback['docid']] = [feedback,]
    
    return mapping

class StepPrinter(object):
    def __init__(self):
        self.steps = [
            'Cloning news articles to experiment tables',
            'Loading truth set',
            'Running labelers',
            'Computing results',
            'Cleaning up',
        ]

        self.current = 0
    
    def next(self):
        print('[{} / {}] {}'.format(self.current + 1, len(self.steps), self.steps[self.current]))
        self.current += 1

"""
Store experimental results for a trial run. Can also generate comparison stats once two
rows have been added. 

Interface was designed to work well with `tabulate` for output.
"""
class StatsTable(object):
    NAME_INDEX = 0
    COVERAGE_INDEX = 1
    HITS_INDEX = 2
    MISSES_INDEX = 3
    PRECISION_INDEX = 4

    def __init__(self):
        self.headers = ['Name', 'Coverage (%)', 'Hits (#)', 'Misses (#)', 'Precision (%)']
        self.stats = []

    def add_row(self, name, coverage, hits, misses, precision):
        row = [None, None, None, None, None]

        row[self.NAME_INDEX] = name
        row[self.COVERAGE_INDEX] = coverage
        row[self.HITS_INDEX] = hits
        row[self.MISSES_INDEX] = misses
        row[self.PRECISION_INDEX] = precision

        self.stats.append(row)
    
    def gen_comparison(self):
        if len(self.stats) is not 2:
            raise Exception('Can only generate a comparison when two rows are provided')

        cov = self.stats[1][self.COVERAGE_INDEX] - self.stats[0][self.COVERAGE_INDEX]
        hits = self.stats[1][self.HITS_INDEX] - self.stats[0][self.HITS_INDEX]
        misses = self.stats[1][self.MISSES_INDEX] - self.stats[0][self.MISSES_INDEX]
        precision = self.stats[1][self.PRECISION_INDEX] - self.stats[0][self.PRECISION_INDEX]

        self.add_row('Difference', cov, hits, misses, precision)

"""
Compute stats for the specified base and compare tables, and generate a StatsTable object. Use 
truth data for measuring hits, misses, and precision.
"""
def stats(base_table, compare_table, truth):
    # TODO: get feedback data

    results = StatsTable()
    labels = ['Base ({})'.format(base), 'Compare ({})'.format(compare)]

    for i, table in enumerate([base_table, compare_table]):
        cursor = rethinkdb.db(DB_DB).table(table).run(md)

        stats_total_labeled = 0
        stats_total_count = 0

        stats_total_hits = 0
        stats_total_misses = 0

        stats_precision = 0.0
        stats_coverage = 0.0

        for record in cursor:
            stats_total_count += 1

            if shared.labels.has_labels(record):
                stats_total_labeled += 1
        
            # Check to see whether this record includes any feedback
            if record['id'] in truth:
                for feedback in truth[record['id']]:
                    label = feedback['label']
                    correct = feedback['correct']

                    attempted_labels = shared.labels.get(record, 'countries')

                    # If the label is present and correct, hit.
                    # If the label isn't present and is incorrect, hit.
                    # Otherwise miss.
                    if correct and label in attempted_labels:
                        stats_total_hits += 1
                    elif correct and label not in attempted_labels:
                        stats_total_misses += 1
                    elif not correct and label in attempted_labels:
                        stats_total_misses += 1
                    elif not correct and label not in attempted_labels:
                        stats_total_hits += 1
        
        stats_precision = stats_total_hits / (stats_total_hits + stats_total_misses)
        stats_coverage = stats_total_labeled / stats_total_count

        results.add_row(labels[i], stats_coverage, stats_total_hits, stats_total_misses, stats_precision)

    results.gen_comparison()
    return results

steps = StepPrinter()

tables = [
    'compare_{}_{}'.format(base, ''.join([random.choice(string.ascii_letters) for i in range(5)])), 
    'compare_{}_{}'.format(compare, ''.join([random.choice(string.ascii_letters) for i in range(5)])),
]

# 1. Create temporary tables
steps.next()
record_count = clone_table(tables)

# 2. Load the truth set
steps.next()
truth = load_truth()

# 3. Run each labeler on the target table
steps.next()
p_base = subprocess.Popen(['python3', 'label_country.py', '--using', base, '--write-to', tables[0]])
p_compare = subprocess.Popen(['python3', 'label_country.py', '--using', compare, '--write-to', tables[1]])

for process in [p_base, p_compare]:
    process.wait()

# 4. Compute stats
steps.next()
outcome = stats(tables[0], tables[1], truth)

# 5. Cleanup compare tables
steps.next()
for table in tables:
    rethinkdb.db(DB_DB).table_drop(table).run(md)

print('Experimental results')
print('=====================')
print('Truth set size: {} ({}%)\n'.format(len(truth), round(len(truth) * 100 / record_count, 2)))
print(tabulate.tabulate(outcome.stats, outcome.headers))