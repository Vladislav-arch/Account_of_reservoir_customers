async def wrap_in_pre_tag(text):
    lines = text.split('\n')
    wrapped_lines = ['<pre>{}</pre>'.format(line) for line in lines]
    return '\n'.join(wrapped_lines)