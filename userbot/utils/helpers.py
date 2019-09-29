from re import findall, match

def parse_arguments(message):
    options = {}

    # Handle boolean values
    for opt in findall(r"\s+([.!]\S+)\s+", message):
        if opt[0] == '.':
            options[opt[1:]] = True
        elif opt[0] == '!':
            options[opt[1:]] = False
        message = message.replace(opt, '')
    
    # Handle key/value pairs
    for opt in findall(r"\s+(\S+):(\S+)\s+", message):
        key, value = opt
        if value.isnumeric(): value = int(value)
        elif match(r"[Tt]rue|[Ff]alse", value): match(r"[Tt]rue", value)
        options[key] = value
        message = message.replace(':'.join(opt), '')

    return (options, message.strip())

def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d

def extract_urls(message):
    matches = findall(r'(https?://\S+)', str(message))
    return list(matches)