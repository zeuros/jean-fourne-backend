

def queryset_to_list(qs):
    """
    this will return python list<dict>
    """
    return [dict(q) for q in qs]