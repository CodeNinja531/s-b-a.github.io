import tkinter as tk
from tkinter import ttk
import sqlite3

DB_PATH = "database\Sports day helper"

def update_leaderboard():
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    cursor.execute("DELETE FROM leaderboard")
    cursor.execute("SELECT event_id, item, grade, gender, category FROM event WHERE status='Completed'")

    events = cursor.fetchall()
    for event_id, item, grade, gender, category in events:
        if category == "racing":
            # fastest player
            cursor.execute("""
                SELECT racing_result.athlete_id, s.name, MIN(racing_result.time) as best_time, s.house
                FROM racing_result
                LEFT JOIN participants p ON racing_result.athlete_id = p.athlete_id
                LEFT JOIN stu_info s ON p.stu_id = s.stu_id
                WHERE racing_result.event_id=? AND racing_result.types='final'
                GROUP BY racing_result.athlete_id
                ORDER BY best_time ASC
            """, (event_id,))
            results = cursor.fetchall()

            for rank, (athlete_id, name, time, house) in enumerate(results, 1):
                cursor.execute("""
                    INSERT INTO leaderboard (event_id, athlete_id, rank, house)
                    VALUES (?, ?, ?, ?)
                """, (event_id, athlete_id, rank, house))

        elif category == "field":
            cursor.execute("""
                SELECT fr.athlete_id, s.name, MAX(fr.distance) as best_distance, s.house
                FROM field_result fr
                LEFT JOIN participants p ON fr.athlete_id = p.athlete_id
                LEFT JOIN stu_info s ON p.stu_id = s.stu_id
                WHERE fr.event_id=? AND fr.types='final'
                GROUP BY fr.athlete_id
                ORDER BY best_distance DESC
            """, (event_id,))

            results = cursor.fetchall()
            for rank, (athlete_id, name, distance, house) in enumerate(results, 1):
                cursor.execute("""
                    INSERT INTO leaderboard (event_id, athlete_id, rank, house)
                    VALUES (?, ?, ?, ?)
                """, (event_id, athlete_id, rank, house))

        elif category == "relay":
            cursor.execute("""
                SELECT team, time
                FROM relay_result
                WHERE event_id=? AND types='overall'
                ORDER BY time ASC
            """, (event_id,))

            results = cursor.fetchall()
            for rank, (team, time) in enumerate(results, 1):
                cursor.execute("""
                    INSERT INTO leaderboard (event_id, athlete_id, rank, house)
                    VALUES (?, ?, ?, ?)
                """, (event_id, team, rank, team))
                
    connect.commit()
    connect.close()

class ResultDisplayApp:
    def __init__(self, master):
        self.master = master
        master.title("Completed Event Results")
        master.geometry("900x700")
        master.resizable(False, False)
        master.grid_columnconfigure(0, weight=1)
        self._create_header(master)
        self._create_results_area(master)

    def _create_header(self, master):
        header_frame = ttk.Frame(master, padding="15")
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        ttk.Label(header_frame, text="Completed Event Results", font=("Arial", 20, "bold"), foreground="#4F46E5").grid(row=0, column=0, pady=5)
        ttk.Label(header_frame, text="Displaying results for all completed events.", font=("Arial", 10), foreground="#4B5563").grid(row=1, column=0, pady=0)

    def _create_results_area(self, master):
        results_frame = ttk.Frame(master, padding="10")
        results_frame.grid(row=1, column=0, sticky="nsew")
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        canvas = tk.Canvas(results_frame)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        # Make the canvas expand vertically with the window
        master.grid_rowconfigure(1, weight=1)
        self._populate_results(scrollable_frame)

    def _populate_results(self, parent):
        connect = sqlite3.connect(DB_PATH)
        cursor = connect.cursor()
        # Get all completed events
        cursor.execute("SELECT event_id, item, grade, gender, category FROM event WHERE status='Completed'")
        events = cursor.fetchall()
        for event_id, item, grade, gender, category in events:
            event_label = ttk.Label(parent, text=f"Event: {item} | Grade: {grade} | Gender: {gender} | Category: {category}",
                                    font=("Arial", 13, "bold"), foreground="#1e293b", padding=(0, 10, 0, 2))
            event_label.pack(anchor="w")
            # Display leaderboard for this event (directly from leaderboard table)
            cursor.execute("""
                SELECT athlete_id, rank, house
                FROM leaderboard
                WHERE event_id=?
                ORDER BY rank ASC
            """, (event_id,))
            results = cursor.fetchall()
            # Try to get name for athlete_id if possible (for racing/field)
            display_rows = []
            for athlete_id, rank, house in results:
                name = "-"
                if category in ("racing", "field"):
                    cursor.execute("SELECT s.name FROM participants p LEFT JOIN stu_info s ON p.stu_id = s.stu_id WHERE p.athlete_id=? LIMIT 1", (athlete_id,))
                    name_row = cursor.fetchone()
                    if name_row and name_row[0]:
                        name = name_row[0]
                if category == "racing" or category == "field":
                    display_rows.append((rank, name, athlete_id, house))
                elif category == "relay":
                    display_rows.append((rank, athlete_id, house))
            if category == "racing":
                columns = ("Rank", "Name", "Athlete ID", "House")
                self._create_table(parent, columns, display_rows)
            elif category == "field":
                columns = ("Rank", "Name", "Athlete ID", "House")
                self._create_table(parent, columns, display_rows)
            elif category == "relay":
                columns = ("Rank", "Team", "House")
                self._create_table(parent, columns, display_rows)
        connect.close()

    def _create_table(self, parent, columns, rows):
        frame = ttk.Frame(parent)
        frame.pack(anchor="w", fill="x", pady=(0, 15))
        # Set height to exactly fit all rows (minimum 1 for header)
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=max(1, len(rows)))
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="x", expand=True)

if __name__ == "__main__":
    update_leaderboard()
    root = tk.Tk()
    app = ResultDisplayApp(root)
    root.mainloop()
