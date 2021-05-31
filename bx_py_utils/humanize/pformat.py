import json
import pprint


def pformat(value):
    """
    Format given object: Try JSON fist and fallback to pformat()
    (JSON dumps are nicer than pprint.pformat() ;)
    """
    try:
        value = json.dumps(value, indent=4, sort_keys=True, ensure_ascii=False)
    except TypeError:
        # Fallback if values are not serializable with JSON:
        value = pprint.pformat(value, width=120)

    return value
