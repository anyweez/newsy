
"""
All metrics should return a dict with keys set to the names of countries
and values set to whatever the specified metric should be for that country. 

Mapping country names back to GeoJSON ID's happens outside of this function;
here you only need to worry about the string that show up in the labels (normal
human-readable country names).
"""

def _increase(mapping, country):
    if country in mapping:
        mapping[country] += 1
    else:
        mapping[country] = 1

def count_diff(base, compare):
    b_count = {}
    c_count = {}
    result = {}

    # For each base document, iterate over its labels and
    for doc in base:
        if 'labels' in doc:
            for country in doc['labels']['countries']:
                _increase(b_count, country)

    for doc in compare:
        if 'labels' in doc:
            for country in doc['labels']['countries']:
                _increase(c_count, country)

    for key in set(b_count.keys()).union(set(c_count.keys())):
        b = b_count[key] if key in b_count else 0
        c = c_count[key] if key in c_count else 0
        result[key] = c - b

    return result