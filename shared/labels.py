"""
Add the specified label to the record. The label name must be a string but the
value(s) can be anything JSON serializable. For example:

name: 'countries'
values: ['United States', 'Venezuela']

This function will overwrite any existing labels with the same name.
"""
def add(record, name, values):
    if 'labels' not in record:
        record['labels'] = {}
    record['labels'][label] = values