import itertools


def dedupe_lines(lines, *, cut_marker='...cut {count} lines...'):
    """
    Collapse runs of 4+ identical consecutive items to first, a cut marker, and last.

    >>> list(dedupe_lines(['a', 'a', 'a', 'a']))
    ['a', '...cut 2 lines...', 'a']

    >>> list(dedupe_lines(['a', 'a', 'a', 'a'], cut_marker='[{count} dupes removed]'))
    ['a', '[2 dupes removed]', 'a']
    """
    for _value, group in itertools.groupby(lines):
        run = list(group)
        if len(run) < 4:
            yield from run
        else:
            yield run[0]
            yield cut_marker.format(count=len(run) - 2)
            yield run[-1]


def dedupe_text(text, *, cut_marker='...cut {count} lines...'):
    """
    Collapse runs of 4+ identical lines in a text block to "first", "a cut marker", and "last".

    >>> print(dedupe_text('''first line
    ... same stuff
    ... same stuff
    ... same stuff
    ... same stuff
    ... end line'''))
    first line
    same stuff
    ...cut 2 lines...
    same stuff
    end line
    """
    lines = text.splitlines()
    deduped = dedupe_lines(lines, cut_marker=cut_marker)
    return '\n'.join(deduped)


def unique_list(seq):
    """
    >>> unique_list([2, 6, 6, 6, 1, 2, 1])
    [2, 6, 1]
    """
    # https://stackoverflow.com/a/480227/35070
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
