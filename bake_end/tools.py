from django.forms import model_to_dict


def queryset_to_list(qs):
    """
    this will return python list<dict>
    """
    return [model_to_dict(q) for q in qs]