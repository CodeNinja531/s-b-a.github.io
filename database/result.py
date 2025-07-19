import tkinter as tk
from tkinter import ttk
import sqlite3

DB_PATH = "database\Sports day helper"

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
        self._populate_results(scrollable_frame)

    def _populate_results(self, parent):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT event_id, item, grade, gender, category FROM event WHERE status='Completed'")
        events = cursor.fetchall()
        for event_id, item, grade, gender, category in events:
            event_label = ttk.Label(parent, text=f"Event: {item} | Grade: {grade} | Gender: {gender} | Category: {category}",
                                    font=("Arial", 13, "bold"), foreground="#1e293b", padding=(0, 10, 0, 2))
            event_label.pack(anchor="w")
            if category == "racing":
                cursor.execute("""
                    SELECT rr.athlete_id, s.name, rr.time
                    FROM racing_result rr
                    LEFT JOIN participants p ON rr.athlete_id = p.athlete_id
                    LEFT JOIN stu_info s ON p.stu_id = s.stu_id
                    WHERE rr.event_id=? AND rr.types='final'
                    ORDER BY rr.time ASC
                """, (event_id,))
                results = cursor.fetchall()
                columns = ("Rank", "Name", "Athlete ID", "Time (s)")
                self._create_table(parent, columns, [
                    (i+1, name or "-", athlete_id, time)
                    for i, (athlete_id, name, time) in enumerate(results)
                ])
            elif category == "field":
                cursor.execute("""
                    SELECT fr.athlete_id, s.name, MAX(fr.distance) as best_distance
                    FROM field_result fr
                    LEFT JOIN participants p ON fr.athlete_id = p.athlete_id
                    LEFT JOIN stu_info s ON p.stu_id = s.stu_id
                    WHERE fr.event_id=? AND fr.types='final'
                    GROUP BY fr.athlete_id
                    ORDER BY best_distance DESC
                """, (event_id,))
                results = cursor.fetchall()
                columns = ("Rank", "Name", "Athlete ID", "Best Distance (m)")
                self._create_table(parent, columns, [
                    (i+1, name or "-", athlete_id, distance)
                    for i, (athlete_id, name, distance) in enumerate(results)
                ])
            elif category == "relay":
                cursor.execute("""
                    SELECT athlete_id, team, time
                    FROM relay_result
                    WHERE event_id=? AND types='overall'
                    ORDER BY time ASC
                """, (event_id,))
                results = cursor.fetchall()
                columns = ("Rank", "Team", "Time (s)")
                self._create_table(parent, columns, [
                    (i+1, team, time)
                    for i, (athlete_id, team, time) in enumerate(results)
                ])
        conn.close()

    def _create_table(self, parent, columns, rows):
        frame = ttk.Frame(parent)
        frame.pack(anchor="w", fill="x", pady=(0, 15))
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=min(10, len(rows)+1))
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="x", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResultDisplayApp(root)
    root.mainloop()
