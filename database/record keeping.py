import tkinter as tk
from tkinter import ttk, messagebox
import functools
import datetime
import sqlite3

DB_PATH = "database\Sports day helper"

class RecordKeeperApp:
    def __init__(self, master):
        self.master = master
        master.title("Record Keeper Tools")
        master.geometry("700x650")
        master.resizable(False, False)
        master.grid_columnconfigure(0, weight=1)

        self.racing_events = {
            'A': ["100m", "200m", "400m", "800m", "1500m"],
            'B': ["100m", "200m", "400m", "800m", "1500m"],
            'C': ["60m", "100m", "200m", "400m", "800m", "1500m"]
        }
        self.field_events = {
            'A': ["High Jump", "Javelin", "Long Jump", "Shot Put"],
            'B': ["High Jump", "Javelin", "Long Jump", "Shot Put"],
            'C': ["High Jump", "Long Jump", "Shot Put", "Softball"]
        }
        self.relay_events = ["4x100", "4x400", "8x100"]

        # --- Tkinter Variables ---
        self.type_var = tk.StringVar()
        self.grade_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.item_var = tk.StringVar()
        self.track_var = tk.StringVar()
        self.result_fields = {}

        # --- UI Layout ---
        self._create_header(master)
        self._create_dropdowns(master)
        self._create_result_form(master)
        self._create_submit_button(master)

    def _create_header(self, master):
        header_frame = ttk.Frame(master, padding="15")
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        ttk.Label(header_frame, text="Record Keeper Tools", font=("Arial", 20, "bold"), foreground="#4F46E5").grid(row=0, column=0, pady=5)

    def _create_dropdowns(self, master):
        dropdown_frame = ttk.LabelFrame(master, text="Event Selection", padding="10")
        dropdown_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        # Type
        ttk.Label(dropdown_frame, text="Type:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        type_menu = ttk.OptionMenu(dropdown_frame, self.type_var, "", "racing", "field", "relay", command=self._on_type_change)
        type_menu.grid(row=0, column=1, padx=5, pady=2)

        # Grade
        ttk.Label(dropdown_frame, text="Grade:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        grade_menu = ttk.OptionMenu(dropdown_frame, self.grade_var, "", "A", "B", "C", command=self._on_grade_gender_change)
        grade_menu.grid(row=0, column=3, padx=5, pady=2)

        # Gender
        ttk.Label(dropdown_frame, text="Gender:", font=("Arial", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=2)
        gender_menu = ttk.OptionMenu(dropdown_frame, self.gender_var, "", "male", "female", command=self._on_grade_gender_change)
        gender_menu.grid(row=0, column=5, padx=5, pady=2)

        # Item
        ttk.Label(dropdown_frame, text="Item:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.item_menu = ttk.OptionMenu(dropdown_frame, self.item_var, "")
        self.item_menu.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Track (for some racing events, shown below items)
        self.track_label = ttk.Label(dropdown_frame, text="Track No.:", font=("Arial", 10))
        self.track_menu = ttk.OptionMenu(dropdown_frame, self.track_var, "", *[""] + [f"Track {i}" for i in range(1, 9)])
        self.track_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.track_menu.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.track_label.grid_remove()
        self.track_menu.grid_remove()

    def _on_type_change(self, *args):
        self._update_items_dropdown()
        self._update_result_form()

    def _on_grade_gender_change(self, *args):
        self._update_items_dropdown()
        self._update_result_form()

    def _update_items_dropdown(self):
        type_ = self.type_var.get()
        grade = self.grade_var.get()
        gender = self.gender_var.get()
        menu = self.item_menu["menu"]
        menu.delete(0, "end")
        items = []
        if type_ == "racing" and grade:
            items = self.racing_events.get(grade, [])
        elif type_ == "field" and grade:
            items = self.field_events.get(grade, [])
        elif type_ == "relay":
            items = self.relay_events
        for item in items:
            menu.add_command(label=item, command=lambda v=item: self._on_item_select(v))
        self.item_var.set(items[0] if items else "")
        self._on_item_select(self.item_var.get())

    def _on_item_select(self, value):
        self.item_var.set(value)
        if self.type_var.get() == "racing" and value in ["100m", "200m", "400m"]:
            self.track_label.grid()
            self.track_menu.grid()
        else:
            self.track_label.grid_remove()
            self.track_menu.grid_remove()
        self._update_result_form()

    def _create_result_form(self, master):
        self.result_frame = ttk.LabelFrame(master, text="Enter Result", padding="10")
        self.result_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self._update_result_form()

    def _update_result_form(self, *args):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        self.result_fields.clear()
        type_ = self.type_var.get()
        item = self.item_var.get()
        row = 0
        if type_ == "racing":
            ttk.Label(self.result_frame, text="Heat/Final:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            types_var = tk.StringVar()
            types_menu = ttk.OptionMenu(self.result_frame, types_var, "heat", "heat", "final")
            types_menu.grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["types"] = types_var
            row += 1

            ttk.Label(self.result_frame, text="Athlete ID:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            athlete_id_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=athlete_id_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["athlete_id"] = athlete_id_var
            row += 1

            ttk.Label(self.result_frame, text="Time (s):", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            time_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=time_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["time"] = time_var

        elif type_ == "field":
            ttk.Label(self.result_frame, text="Heat/Final:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            types_var = tk.StringVar()
            types_menu = ttk.OptionMenu(self.result_frame, types_var, "heat", "heat", "final")
            types_menu.grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["types"] = types_var
            row += 1

            ttk.Label(self.result_frame, text="Athlete ID:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            athlete_id_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=athlete_id_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["athlete_id"] = athlete_id_var
            row += 1

            ttk.Label(self.result_frame, text="Trial:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            trial_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=trial_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["trial"] = trial_var
            row += 1

            ttk.Label(self.result_frame, text="Distance (m):", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            distance_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=distance_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["distance"] = distance_var

        elif type_ == "relay":
            ttk.Label(self.result_frame, text="Athlete ID:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            athlete_id_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=athlete_id_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["athlete_id"] = athlete_id_var
            row += 1

            ttk.Label(self.result_frame, text="Position:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            position_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=position_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["position"] = position_var
            row += 1

            ttk.Label(self.result_frame, text="Team:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            team_var = tk.StringVar()
            team_menu = ttk.OptionMenu(self.result_frame, team_var, "", "Virtue", "Trust", "Loyalty", "Intellect")
            team_menu.grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["team"] = team_var
            row += 1

            ttk.Label(self.result_frame, text="Time (s):", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=2)
            time_var = tk.StringVar()
            ttk.Entry(self.result_frame, textvariable=time_var).grid(row=row, column=1, sticky="w", pady=2)
            self.result_fields["time"] = time_var

    def _create_submit_button(self, master):
        submit_btn = ttk.Button(ttk.Frame(master).grid(row=4, column=0, pady=20), text="Submit Result", command=self.submit_result)
        submit_btn.pack(ipadx=10, ipady=5)

    def submit_result(self):
        if not (self.type_var.get() and self.grade_var.get() and self.gender_var.get() and self.item_var.get()):
            return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        db_gender = "boys" if self.gender_var.get() == "male" else "girls"
        cursor.execute("SELECT event_id FROM event WHERE grade=? AND gender=? AND item=? AND category=?", (self.grade_var.get(), db_gender, self.item_var.get(), type_))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return
        event_id = row[0]

        if self.type_var.get() == "racing":
            types = self.result_fields["types"].get()
            athlete_id = self.result_fields["athlete_id"].get()
            time_val = self.result_fields["time"].get()
            try:
                cursor.execute(
                    "INSERT OR REPLACE INTO racing_result (event_id, types, athlete_id, time) VALUES (?, ?, ?, ?)",
                    (event_id, types, athlete_id, float(time_val))
                )
                conn.commit()
                messagebox.showinfo("Success", "Racing result submitted.")
            except:
                pass
        elif self.type_var.get() == "field":
            types = self.result_fields["types"].get()
            athlete_id = self.result_fields["athlete_id"].get()
            trial = self.result_fields["trial"].get()
            distance = self.result_fields["distance"].get()
            try:
                cursor.execute(
                    "INSERT OR REPLACE INTO field_result (event_id, types, athlete_id, trial, distance) VALUES (?, ?, ?, ?, ?)",
                    (event_id, types, athlete_id, int(trial), float(distance))
                )
                conn.commit()
                messagebox.showinfo("Success", "Field result submitted.")
            except:
                pass
        elif self.type_var.get() == "relay":
            athlete_id = self.result_fields["athlete_id"].get()
            position = self.result_fields["position"].get()
            team = self.result_fields["team"].get()
            time_val = self.result_fields["time"].get()
            try:
                cursor.execute(
                    "INSERT OR REPLACE INTO relay_result (event_id, types, athlete_id, position, team, time) VALUES (?, ?, ?, ?, ?, ?)",
                    (event_id, "individual", athlete_id, int(position), team, float(time_val))
                )
                cursor.execute(
                    "SELECT COUNT(*) FROM relay_result WHERE event_id=? AND team=? AND types='individual'",
                    (event_id, team)
                )
                count = cursor.fetchone()[0]
                max_members = 8 if self.item_var.get() == "8x100" else 4
                if count == max_members:
                    cursor.execute(
                        "SELECT SUM(time) FROM relay_result WHERE event_id=? AND team=? AND types='individual'",
                        (event_id, team)
                    )
                    total_time = cursor.fetchone()[0]
                    cursor.execute(
                        "INSERT OR REPLACE INTO relay_result (event_id, types, athlete_id, position, team, time) VALUES (?, ?, ?, ?, ?, ?)",
                        (event_id, "overall", None, None, team, total_time)
                    )
                conn.commit()
                messagebox.showinfo("Success", "Relay result submitted.")
            except:
                pass
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecordKeeperApp(root)
    root.mainloop()
