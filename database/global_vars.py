# global_vars.py
# Centralized global variables for easy configuration
from datetime import datetime

date_for_age_comparison = datetime(2024, 9, 1)

racing_events = {
    'A': ["100m", "200m", "400m", "800m", "1500m"],
    'B': ["100m", "200m", "400m", "800m", "1500m"],
    'C': ["60m", "100m", "200m", "400m", "800m", "1500m"]
}

field_events = {
    'A': ["High Jump", "Javelin", "Long Jump", "Shot Put"],
    'B': ["High Jump", "Javelin", "Long Jump", "Shot Put"],
    'C': ["High Jump", "Long Jump", "Shot Put", "Softball"]
}

house_colors = {
    'Virtue': 'red',
    'Trust': 'green',
    'Loyalty': 'purple',
    'Intellect': 'blue'
}
