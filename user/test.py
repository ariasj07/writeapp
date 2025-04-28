import re

def convert(data):
    result = re.sub(r"\*\*\*\*(.*?)\*\*\*\*", r"""<h3 class="py-2">\1</h3>""", data)
    result = re.sub(r"\*\*\*(.*?)\*\*\*", r"<strong>\1</strong>", result)
    return result
    
