
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
    
    'The Bahamas': { 'Bahamian' },
    'Bahrain': set(),
    'Bangladesh': { 'Bangladeshi' },
    'Barbados': set(),
    'Belarus': set(),
    'Belgium': { 'Belgian' },
    'Belize': set(),
    'Benin': set(),
    'Bhutan': { 'Bhutani' },
    'Bolivia': { 'Bolivian' },
    'Bosnia and Herzegovina': { 'Bosnia', 'Herzegovina' },
    'Botswana': { 'Botswanan' },
    'Brazil': { 'Brazilian' },
    'Brunei': set(),
    'Bulgaria': { 'Bulgarian' },
    'Burkina Faso': set(),
    'Burma': set(),
    'Burundi': set(),

    'Cambodia': { 'Cambodian' },
    'Cameroon': { 'bbb' },
    'Canada': { 'Canadian' },
    'Cabo Verde': set(),
    'Central African Republic': set(),
    'Chad': set(),
    'Chile': { 'Chileans' },
    'China': { 'Chinese' },
    'Colombia': { 'Colombians' },
    'Comoros': set(),
    'Democratic Republic of the Congo': { 'Congo' },
    'Costa Rica': { 'Costa Rican' },
    'Cote d\'Ivoire': { 'Ivory Coast' },
    'Croatia': { 'Croatian' },
    'Cuba': { 'Cuban' },
    'Curacao': set(),
    'Cyprus': set(),
    'Czechia': set(),

    'Denmark': { 'Danish' },
    'Djibouti': set(),
    'Dominica': set(),
    'Dominican Republic': set(),

    'East Timor': { 'Timor-Leste' },
    'Ecuador': { 'Ecuadorians' },
    'Egypt': { 'Egyptians' },
    'El Salvador': set(),
    'Equatorial Guinea': { 'Guinea' },
    'Eritrea': set(),
    'Estonia': set(),
    'Ethiopia': set(),

    'Fiji': { 'Fijian' },
    'Finland': set(),
    'France': { 'French' },

    'Gabon': set(),
    'Gambia': set(),
    'Georgia': { 'Georgian' },
    'Germany': { 'German' },
    'Ghana': set(),
    'Greece': { 'Greek' },
    'Grenada': set(),
    'Guatemala': { 'Guatemalan' },
    'Guinea': set(),
    'Guyana': set(),

    'Haiti': { 'Haitian' },
    'Holy See': { 'Vatican City', 'Vatican' },
    'Honduras': { 'Honduran' },
    'Hong Kong': set(),
    'Hungary': { 'Hungarian' },

    'Iceland': { 'Icelandic' },
    'India': { 'Indian' },
    'Indonesia': { 'Indonesian' },
    'Iran': { 'Iranian' },
    'Iraq': { 'Iraqi' },
    'Ireland': { 'Irish' },
    'Israel': { 'Israeli' },
    'Italy': { 'Italian' },

    'Japan': { 'Japanese' },
    'Jamaica': { 'Jamaican' },
    'Jordan': { 'Jordanian' },

    'Kazakhstan': set(),
    'Kenya': { 'Kenyan' },
    'Kiribati': set(),
    'Kosovo': set(),
    'Kuwait': set(),
    'Kyrgyzstan': set(),
    
    'Laos': { 'Laotian' },
    'Latvia': { 'Latvian' },
    'Lebanon': { 'Lebanese' },
    'Lesotho': set(),
    'Liberia': { 'Liberian' },
    'Libya': { 'Libyan' },
    'Liechtenstein': set(),
    'Lithuania': { 'Lithuanian' },
    'Luxembourg': set(),

    'Macau': { 'bbb' },
    'Macedonia': { 'bbb' },
    'Madagascar': { 'bbb' },
    'Malawi': { 'bbb' },
    'Malaysia': { 'bbb' },
    'Maldives': { 'bbb' },
    'Mali': { 'bbb' },
    'Malta': { 'bbb' },
    'Marshall Islands': { 'bbb' },
    'Mauritania': { 'bbb' },
    'Mauritius': { 'bbb' },
    'Mexico': { 'bbb' },
    'Micronesia': { 'bbb' },
    'Moldova': { 'bbb' },
    'Monaco': { 'bbb' },
    'Mongolia': { 'bbb' },
    'Montenegro': { 'bbb' },
    'Morocco': { 'bbb' },
    'Mozambique': { 'bbb' },

    'Namibia': { 'Namibian' },
    'Nauru': set(),
    'Nepal': { 'Nepalese' },
    'Netherlands': { 'Dutch' },
    'New Zealand': set(),
    'Nicaragua': { 'Nicaraguan' },
    'Niger': set(),
    'Nigeria': { 'Nigerian' },
    'North Korea': set(),
    'Norway': { 'Norwegian' },

    'Oman': set(),

    'Pakistan': { 'Pakistani' },
    'Palau': set(),
    'Palestinian Territories': set(),
    'Panama': { 'Panamanian' },
    'Papau New Guinea': set(),
    'Paraguay': set(),
    'Peru': { 'Peruvian' },
    'Philippines': set(),
    'Poland': set(),
    'Portugal': { 'Portuguese' },

    'Qatar': set(),

    'Romania': { 'Romanian' },
    'Russia': { 'Russian' },
    'Rwanda': set(),


    'Saint Kitts and Nevis': { 'Saint Kitts' },
    'Saint Lucia': set(),
    'Saint Vincent and the Grenadines': { 'Saint Vincent' },
    'Samoa': { 'Samoan' },
    'San Marino': set(),
    'Sao Tome and Principe': { 'Sao Tome' },
    'Saudi Arabia': { 'Saudi Arabian' },
    'Senegal': set(),
    'Serbia': { 'Serbian' },
    'Seychelles': set(),
    'Sierra Leone': set(),
    'Singapore': set(),
    'Sint Maarten': set(),
    'Slovakia': { 'Slovakian' },
    'Slovenia': { 'Slovenia' },
    'Solomon Islands': set(),
    'Somalia': { 'Somalian' },
    'South Africa': { 'South African' },
    'South Korea': { 'South Korean' },
    'South Sudan': { 'South Sudanese' },
    'Spain': { 'Spanish' },
    'Sri Lanka': { 'Sri Lankan' },
    'Sudan': { 'Sudanese' },
    'Suriname': set(),
    'Swaziland': set(),
    'Sweden': { 'Swedish' },
    'Switzerland': { 'Swiss' },
    'Syria': { 'Syrian' },

    'Taiwan': { 'bbb' },
    'Tajikistan': { 'bbb' },
    'Tanzania': { 'bbb' },
    'Thailand': { 'bbb' },
    'Timor-Leste': { 'bbb' },
    'Togo': set(),
    'Tonga': set(),
    'Trinidad and Tobago': { 'Trinidad' },
    'Tunisia': set(),
    'Turkey': { 'Turkish' },
    'Turkmenistan': set(),
    'Tuvalu': set(),
    
    'Uganda': { 'Ugandan' },
    'Ukraine': { 'Ukrainian' },
    'United Arab Emirates': set(),
    'United Kingdom': { 'British', 'UK' },
    'Uruguay': set(),
    'United States': { 'US', 'America', 'American' },
    'Uzbekistan': set(),

    'Vanuatu': set(),
    'Venezuela': { 'Venezuelan' },
    'Vietnam': { 'Vietnamese' },

    'Yemen': set(),

    'Zambia': { 'Zambian' },
    'Zimbabwe': set(),
}

for label, terms in countries.items():
    terms.add(label)

## Return the countries where at least one of the synonyms (or the label itself)
## is found in the bag. The bag can contain single- or multi-word strings.
def find_countries(bag):
    result = []
    bag = list(map(lambda x: x.lower(), bag))

    for label, terms in countries.items():
        if len([term for term in bag if term in terms]) > 0:
            result.append(label)

    return result