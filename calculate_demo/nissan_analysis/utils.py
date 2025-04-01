
import re

def parse_accounting_number(val):
    """
    Parse accounting-style numbers, e.g. "(123.45)" to -123.45
    Handles comma separators and whitespace.
    """
    if isinstance(val, str):
        val = val.strip()
        if re.match(r'^\(\s*\d+(\.\d+)?\s*\)$', val):
            return -float(val.strip('()').replace(',', '').strip())
        return float(val.replace(',', '').strip())
    return float(val)
