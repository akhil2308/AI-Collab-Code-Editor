import re

def extract_all_code(content: str) -> list:
    """
    ```python
    
    ```
    """
    pattern = r"```.*?\n(.*?)```"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return content
