"""
Base functionality that should be shared by all labelers, including a common interface and 
stats calculation / reporting.
"""
class Labeler(object):
    def __init__(self):
        self.stats = LabelStats()

    def search(self, bag):
        result = self.find_labels(bag)

        self._bump_stats(bag, result)
        return result

    """
    This method needs to be implemented by each labeler. Aside from any sort of (optional) 
    initialization, this is the only functionality that a labeler actually needs to implement.
    """
    def find_labels(self, bag):
        raise NotImplementedError

    def _bump_stats(self, bag, result):
        if len(result) > 0:
            self.stats.found += 1
        
        self.stats.attempts += 1
        self.stats.coverage_pct = self.stats.found / self.stats.attempts

class LabelStats(object):
    def __init__(self):
        self.attempts = 0           # Total number of searches
        self.found = 0              # Searches resulting in at least one match
        self.coverage_pct = 0.0     # found / attempts