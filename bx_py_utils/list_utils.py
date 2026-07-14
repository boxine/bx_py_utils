def unique_list(seq):
    # https://stackoverflow.com/a/480227/35070
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
