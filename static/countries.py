
# Key is the actual label for the country. The value is a list of other
# words that are synonymous with the key (locations only, ideally).
countries = {
    'Afghanistan': { 'Afghani' },
    'Albania': { 'Albanian' },
    'Algeria': { 'Algeria' },
    'Andorra': { 'Andorra' },
    'Angola': { 'Angolan' },
    'Antigua and Barbuda': { 'Andorra' },
    'Argentina': { 'Andorra' },
    'Armenia': { 'Andorra' },
    'Aruba': { 'Aruban' },
    'Australia': { 'Australian' },
    'Austria': { 'Austrian' },
    'Azerbaijan': { 'Azerbaijani' },

    'United States': { 'US', 'America', 'American' },
    'Mexico': { 'MX', 'Mexico', 'Mexican' },
    'Russia': { 'USSR', 'Russian' },
    'Canada': { 'Canadian' },
    'Brazil': { 'Brazilian' },
    'United Kingdom': { 'UK', 'England' },
    'China': { 'Chinese' },
    'India': { 'Indian' }
}

for label, terms in countries.items():
    countries[label].add(label)
    countries[label] = set(map(lambda x: x.lower(), countries[label]))

## Return the countries where at least one of the synonyms (or the label itself)
## is found in the bag. The bag can contain single- or multi-word strings.
def find_countries(bag):
    result = []
    bag = list(map(lambda x: x.lower(), bag))

    for label, terms in countries.items():
        if len([term for term in bag if term in terms]) > 0:
            result.append(label)

    return result