import re


async def extract_date(text):
    date_pattern = r'Дата: (\d{4}-\d{2}-\d{2})'
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)
    else:
        return None