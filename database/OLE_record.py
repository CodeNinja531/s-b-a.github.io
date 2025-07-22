import sqlite3
import pandas as pd
from collections import defaultdict
import os
from openpyxl import load_workbook

DB_PATH = "database/Sports day helper"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Query to get class, clno, student name, event, gender, grade, and ranking
query = """
SELECT
    stu_info.class AS Class,
    stu_info.clno AS Clno,
    stu_info.name AS Name,
    event.item AS Event,
    event.gender AS Gender,
    event.grade AS Grade,
    leaderboard.rank AS Ranking
FROM leaderboard
JOIN participants ON leaderboard.athlete_id = participants.athlete_id AND leaderboard.event_id = participants.event_id
JOIN stu_info ON participants.stu_id = stu_info.stu_id
JOIN event ON leaderboard.event_id = event.event_id
ORDER BY stu_info.class, stu_info.clno, stu_info.name, leaderboard.rank
"""

cursor.execute(query)
rows = cursor.fetchall()

# Helper to convert rank to award string
def rank_to_award(rank):
    if rank == 1:
        return "Champion"
    elif rank == 2:
        return "1st Runner-up"
    elif rank == 3:
        return "2nd Runner-up"
    elif rank == 4:
        return "4th Place"
    elif rank == 5:
        return "5th Place"
    else:
        return f"{rank}th Place"

# Group by student (class, clno, name)
student_awards = defaultdict(list)
for row in rows:
    key = (row[0], row[1], row[2])  # (Class, Clno, Name)
    # Compose event name: Boy's/Girl's <grade> Grade <event>
    gender = row[4]
    if gender.lower() == "boy":
        gender_str = "Boy's"
    elif gender.lower() == "girl":
        gender_str = "Girl's"
    else:
        gender_str = f"{gender}'s"
    event_full = f"{gender_str} {row[5]} Grade {row[3]}"
    award_str = rank_to_award(row[6])
    student_awards[key].append((award_str, event_full))

def class_sort_key(cls):
    # Assumes class format like '1A', '2B', etc.
    # Splits into (grade:int, section:str)
    import re
    m = re.match(r"(\d+)([A-D])", cls)
    if m:
        grade = int(m.group(1))
        section = m.group(2)
        return (grade, section)
    return (999, cls)  # fallback for unexpected format

# Prepare data for Excel
excel_rows = []
# Sort students by class, clno, name
sorted_students = sorted(student_awards.items(), key=lambda x: (class_sort_key(x[0][0]), int(x[0][1]), x[0][2]))
for (cls, clno, name), awards in sorted_students:
    # Only show up to 5 awards per student
    awards = awards[:5]
    # Format: <award> in <event name>
    award_lines = [f"{a[0]} in {a[1]}" for a in awards]
    award_cell = '\n'.join(award_lines) if award_lines else ''
    excel_rows.append([cls, clno, name, 'participant', award_cell])
    # Add a blank line after each student
    excel_rows.append(['', '', '', '', ''])

output_file = 'OLE.xlsx'
if os.path.exists(output_file):
    os.remove(output_file)

df = pd.DataFrame(excel_rows, columns=['Class', 'Clno', 'Name', 'Role', 'Award'])

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    pd.DataFrame([["Sports Day OLE Record"]]).to_excel(writer, index=False, header=False)
    df.to_excel(writer, index=False, startrow=1)


wb = load_workbook(output_file)
ws = wb.active
ws.merge_cells('A1:E1')

# Set title font style
from openpyxl.styles import Font
ws['A1'].font = Font(size=20, bold=True)

ws.freeze_panes = 'A3'

from openpyxl.utils import get_column_letter
for col in range(1, 6):
    max_length = 0
    col_letter = get_column_letter(col)
    for cell in ws[col_letter]:
        try:
            cell_value = str(cell.value)
        except:
            cell_value = ""
        if cell_value:
            max_length = max(max_length, len(cell_value))
    ws.column_dimensions[col_letter].width = max_length + 2

wb.save(output_file)

conn.close()