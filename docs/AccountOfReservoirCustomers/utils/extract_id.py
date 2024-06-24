import re


async def extract_id(info_string):
    if info_string:
        match = re.search(r'🆔Id:\s+(\d+)', info_string)

        if match:
            return int(match.group(1))
        else:
            return None

