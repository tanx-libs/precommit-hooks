import re
import sys
from typing import Optional

REGEX_PATTERN = r'(?i)(?:"|\')(?:0x|[0-9a-f]{2})(?:[a-f0-9]{64}|[a-f0-9]{62})(?:"|\')(?! *# *noqa:keycheck|.*#noqa:keycheck)'

def check_regex_match(filename: str, regex: str) -> Optional[str]:
    matches =[]
    with open(filename, 'r') as f:
        content = f.read()
    match = re.findall(regex, content)
    if match:
        for i in match:
            matches.append(f'Found a sensitive key in {filename}: {i}')
    if len(matches)>0:
        return '\n'.join(matches)
    return None


def main():
    regex = REGEX_PATTERN
    files = sys.argv[1:]
    results = []
    for filename in files:
        result = check_regex_match(filename, regex)
        if result:
            results.append(result)
    if len(results) > 0:
        print('\n'.join(results))
        print('\n to ignore this check, add " # noqa:keycheck" ')
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()