import re


def rison_dumps(obj):
    """Encode as RISON, a URL-safe encoding format.
    Decoder and spec can be found at https://github.com/Nanonid/rison .
    """

    if obj is True:
        return '!t'
    if obj is False:
        return '!f'
    if obj is None:
        return '!n'

    if isinstance(obj, str):
        if re.match(r'^[a-zA-Z_.][-a-zA-Z0-9_.]+$', obj):
            return obj  # no quoting necessary!

        return "'" + re.sub(r"([!'])", r'!\1', obj) + "'"

    if isinstance(obj, dict):
        return '(' + ','.join(rison_dumps(k) + ':' + rison_dumps(v) for k, v in sorted(obj.items())) + ')'

    if isinstance(obj, (list, tuple)):
        return '!(' + ','.join(rison_dumps(v) for v in obj) + ')'

    if isinstance(obj, int):
        return str(obj)

    raise TypeError(f'Unsupported object {obj!r} of type {type(obj).__name__}')
