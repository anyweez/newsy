import arrow

## Return any documents created between `start` and `end`
## days ago
def DAY_to_DAY_days_ago(doc, start, end):
    start = int(start)
    end = int(end)

    if doc['published'] is None:
        return False

    now = arrow.utcnow()
    pub = arrow.get(doc['published']).datetime

    diff = (now - pub).days

    return diff >= start and diff <= end

def now_to_DAY_days_ago(doc, end):
    return DAY_to_DAY_days_ago(doc, 0, end)