# global_vars.py
# Centralized global variables for easy configuration
from datetime import datetime

date_for_age_comparison = datetime(2024, 9, 1)

debug_gmails = [
    's20201033@carmelss.edu.hk',
    's20011313@carmelss.edu.hk',
    's20122020@carmelss.edu.hk',
    's20229999@carmelss.edu.hk',
    's20242009@carmelss.edu.hk'
]

database_path = 'D:/Ching/VS code/s-b-a.github.io/database/Sports day helper'

racing_events_data = {
    'A': ["100m", "200m", "400m", "800m", "1500m"],
    'B': ["100m", "200m", "400m", "800m", "1500m"],
    'C': ["60m", "100m", "200m", "400m", "800m", "1500m"]
}

field_events_data = {
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
