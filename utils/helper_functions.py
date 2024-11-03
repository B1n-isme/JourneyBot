import re
from tools.geocode_tool import get_country_code

def parse_location(user_input):
    location_match = re.search(r"in ([a-zA-Z\s]+)", user_input, re.IGNORECASE)
    if location_match:
        city = location_match.group(1).strip()
        return f"{city}, {get_country_code(city) or 'US'}"
    return None
