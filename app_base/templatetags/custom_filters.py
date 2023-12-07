from django import template

register = template.Library()


@register.filter
def get_key(dictionary, key):
    return dictionary.get(key, 0)


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.

    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %} outputs ?foo=one&bar=two&baz=99

    A RequestContext is required for access to the current querystring.
    """
    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


from decimal import Decimal


@register.filter
def remove_trailing_zeros(value):
    # Check if the value is a float or Decimal
    if isinstance(value, (float, Decimal)):
        return str(value).rstrip("0").rstrip(".") if "." in str(value) else str(value)
    return value
