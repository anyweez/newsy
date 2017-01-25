
# Key is the actual label for the country. The value is a list of other
# words that are synonymous with the key (locations only, ideally).
countries = {
    'United States': ['US', 'America', 'American'],
    'Mexico': ['MX', 'Mexico', 'Mexican'],
    'Russia': ['USSR', 'Russian'],
    'Canada': ['Canadian'],
    'Brazil': ['Brazilian'],
    'United Kingdom': ['UK', 'England'],
    'China': ['Chinese'],
    'India': ['Indian']
}

## Return the countries where at least one of the synonyms (or the label itself)
## is found in the bag. The bag can contain single- or multi-word strings.
def find_countries(bag):
    result = []
    bag = list(map(lambda x: x.lower(), bag))

    for label, terms in countries.items():
        terms.append(label)
        terms = list(map(lambda x: x.lower(), terms))

        if len([term for term in bag if term in terms]) > 0:
            result.append(label)

    return result