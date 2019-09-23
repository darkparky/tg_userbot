from re import findall, match

def parse_arguments(message):
    options = {}

    # Handle boolean values
    for opt in findall(r"([.!]\S+)", message):
        if opt[0] == '.':
            options[opt[1:]] = True
        elif opt[0] == '!':
            options[opt[1:]] = False
        message = message.replace(opt, '')
    
    # Handle key/value pairs
    for opt in findall(r"(\S+):(\S+)", message):
        key, value = opt
        if value.isnumeric(): value = int(value)
        elif match(r"[Tt]rue|[Ff]alse", value): match(r"[Tt]rue", value)
        options[key] = value
        message = message.replace(':'.join(opt), '')

    return (options, message.strip())