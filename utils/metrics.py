import arrow

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

# Convert the provided list of articles into a country-keyed dictionary instead. Each
# key will point to a list of articles that contained the specified country in its 
# set of labels.
def _flip(articles):
    flipped = {}

    for doc in articles:
        if 'labels' in doc:
            for country in doc['labels']['countries']:
                if country in flipped:
                    flipped[country].append(doc)
                else:
                    flipped[country] = [doc,]            

    return flipped

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

# Initial metric for newsy. This compares the number of articles published per day in the base set to
# the number of articles published per day in the compare set and returns the relative % difference. 
#
# If either set has no articles, the size will be assumed to be one so that the rate of increase / decrease 
# is equal to teh size of the other set. If both sets have a length of zero then the rate of growth is zero.
def rel_articles_per_day(base, compare):
    # Compute the relative articles per day score for the given base and compare set of
    # articles. This function is called multiple times, once per country.
    def get_score(base, compare):
        base_days = set()
        compare_days = set()

        for article in base:
            print(arrow.get(article['published']).format('YYYY-MM-DD'))
            when = arrow.get(article['published']).format('YYYY-MM-DD')
            base_days.add(when)

        for article in compare:
            when = arrow.get(article['published']).format('YYYY-MM-DD')
            compare_days.add(when)

        # If we had at least one article in the old set and one in the new set,
        # do the cleanest calculation. If not, degrade the calculation in various
        # ways (see else statements below).
        if len(base_days) > 0 and len(compare_days) > 0:
            base_per_day = len(base) / len(base_days)
            compare_per_day = len(compare) / len(compare_days)

            if base_per_day > 0:
                return compare_per_day / base_per_day
            else:
                return compare_per_day # assume denom of 1 if its actually 0
        # If no news was written in the base set, assume denom of 1. Math would disagree but
        # I THINK this should be fairly accurate from a human interaction perspective (large
        # but comprehendable growth rates; inifinite growth is mathematically correct but 
        # that means nothing).
        elif len(compare_days) > 0:
            return len(compare) / len(compare_days)
        # If no articles were written in the most recent set, we shrink to zero. This condition
        # almost isn't required but would throw an exception in the primary case as written if 
        # we allowed it there.
        elif len(base_days) > 0:
            return -1 * (len(base) / len(base_days))
        # If no articles were written at either point, just say zero (no growth). This shouldn't 
        # occur in practice because the value won't be computed unless there is at least one
        # article written at some point.
        else:
            return 0

    # Convert the list of articles into a country-keyed dictionary of articles.
    base_by_country = _flip(base)
    compare_by_country = _flip(compare)
    result = {}

    # Build a list of all available countries ('available' means at least one article was 
    # published for the country at some point).
    countries = set()
    for country, _ in base_by_country.items():
        countries.add(country)
    for country, _ in compare_by_country.items():
        countries.add(country)

    # Compute the score for each country.
    for country in countries:
        b = base_by_country[country] if country in base_by_country else []
        c = compare_by_country[country] if country in compare_by_country else []
        result[country] = get_score(b, c)
    
    return result