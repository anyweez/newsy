import static.countries as static
import labeler.base as labeler

## To add a new labeler:
##  1. Create a new class that inherits from labeler.Labeler. 
##  2. Note to self: CALL THE SUPER CONSTRUCTOR
##  3. Add the new class to the `algos` map below.

"""
Return countries that are explicitly mentioned by name, nothing more. There is a 
small set of synonyms ('Spanish' for Spain) that are also available for each country
but no deduction or fancy business happening here.
"""
class Explicit(labeler.Labeler):
    def __init__(self):
        labeler.Labeler.__init__(self)

    def find_labels(self, bag):
        result = []

        for label, terms in static.countries.items():
            if len([term for term in bag if term in terms]) > 0:
                result.append(label)

        return result


algos = {
    'explicit': Explicit
}

# 1. prepare algorithm `algo`. This should perform one-time setup tasks.
# 2. return an instance of an object that's got a .search property 

def prepare_algo(algo):
    try:
        return algos[algo]()
    except KeyError:
        raise Exception('Unknown labeling algorithm: {}'.format(algo))
