import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from datetime import datetime
import sqlite3

DB_PATH = "database\Sports day helper"

def get_all_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Ensure stu_info table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stu_info (
            stu_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            class TEXT,
            clno INTEGER,
            gender TEXT NOT NULL,
            dob DATE,
            gmail TEXT,
            house TEXT
        )
    """)
    cursor.execute("SELECT stu_id, name, class, clno, gender, dob, house, gmail FROM stu_info")
    students = cursor.fetchall()
    conn.close()
    return students

def get_next_athlete_id(cursor):
    cursor.execute("SELECT athlete_id FROM participants ORDER BY athlete_id DESC LIMIT 1")
    row = cursor.fetchone()
    if row and row[0]:
        return f"{int(row[0])+1:04d}"
    else:
        return "0001"

def get_event_id(cursor, event_name):
    parts = event_name.split()
    if len(parts) < 3:
        return None
    gender = "boys" if "Boy" in parts[0] else "girls"
    grade = parts[1]
    item = " ".join(parts[2:])
    cursor.execute("SELECT event_id FROM event WHERE grade=? AND gender=? AND item=?", (grade, gender, item))
    row = cursor.fetchone()
    return row[0] if row else None

def save_registration_to_db(data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                athlete_id TEXT PRIMARY KEY NOT NULL,
                stu_id TEXT,
                event_id INTEGER
            )
        """)
        stu_id = data.get('stu_id', None)
        cursor.execute("SELECT athlete_id FROM participants WHERE stu_id=?", (stu_id,))
        row = cursor.fetchone()
        if row and row[0]:
            athlete_id = row[0]
            cursor.execute("DELETE FROM participants WHERE athlete_id=?", (athlete_id,))
        else:
            athlete_id = get_next_athlete_id(cursor)

        for event in data['racing_events']:
            event_id = get_event_id(cursor, event)
            cursor.execute("""
                INSERT INTO participants (athlete_id, stu_id, event_id)
                VALUES (?, ?, ?)
            """, (athlete_id, stu_id, event_id))
        # Field events
        for event in data['field_events']:
            event_id = get_event_id(cursor, event)
            cursor.execute("""
                INSERT INTO participants (athlete_id, stu_id, event_id)
                VALUES (?, ?, ?)
            """, (athlete_id, stu_id, event_id))
        conn.commit()
        conn.close()
        return True, f"Registration submitted successfully! Athlete ID: {athlete_id}"
    except Exception as e:
        return False, f"Database error: {e}"

class SportsRegistrationApp:
    def __init__(self, master):
        self.master = master
        master.title("Sports Day Registration")
        master.geometry("550x700")
        master.resizable(False, False)
        master.grid_columnconfigure(0, weight=1)

        # --- Gmail Selection from DB ---
        students = get_all_students()
        self.students = students
        self.debug_names = [row[1] for row in students]
        self.selected_name = tk.StringVar(value=self.debug_names[0] if self.debug_names else "")
        self._create_name_selector(master)
        # --- User Info from DB ---
        self.user_info = self._get_user_info_by_name(self.selected_name.get())
        self.class_info = self.user_info['class']
        self.class_number = self.user_info['clno']
        self.name = self.user_info['name']
        self.grade = self._get_grade(self.user_info['dob'])
        self.gender = 'male' if self.user_info['gender'].upper().startswith('M') else 'female'

        # --- Events ---
        self.racing_events_data = {
            'A': ["100m", "200m", "400m", "800m", "1500m"],
            'B': ["100m", "200m", "400m", "800m", "1500m"],
            'C': ["60m", "100m", "200m", "400m", "800m", "1500m"]
        }
        self.field_events_data = {
            'A': ["High Jump", "Javelin", "Long Jump", "Shot Put"],
            'B': ["High Jump", "Javelin", "Long Jump", "Shot Put"],
            'C': ["High Jump", "Long Jump", "Shot Put", "Softball"]
        }

        self.gender_var = tk.StringVar(master)
        self.gender_var.set("")

        self.racing_checkbox_vars = {}
        self.field_checkbox_vars = {}
        self.racing_checkbox_widgets = {}
        self.field_checkbox_widgets = {}

        # --- UI Elements ---
        self._create_header(master)
        self._create_user_info_section(master)
        self._create_sports_group_display(master)
        self._create_event_sections(master)
        self._create_submit_button(master)
        self.gender = 'male' if self.user_info['gender'].upper().startswith('M') else 'female'

        # Initialize UI
        self.update_gender_selection()

    def _get_user_info_by_name(self, name):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT stu_id, name, class, clno, gender, dob, house, gmail FROM stu_info WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                'stu_id': row[0],
                'name': row[1],
                'class': row[2],
                'clno': row[3],
                'gender': row[4],
                'dob': row[5],
                'house': row[6],
                'gmail': row[7]
            }
        else:
            return {
                'stu_id': '',
                'name': '',
                'class': '',
                'clno': '',
                'gender': '',
                'dob': '2000-01-01',
                'house': '',
                'gmail': ''
            }

    def _create_header(self, master):
        header_frame = ttk.Frame(master, padding="15") # Reduced padding
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(header_frame, text="Sports Day Registration", font=("Inter", 20, "bold"), foreground="#4F46E5").grid(row=0, column=0, pady=5) # Reduced pady
        ttk.Label(header_frame, text="Welcome to the Sports Day registration portal!", font=("Inter", 10), foreground="#4B5563").grid(row=1, column=0, pady=0)

    def _create_name_selector(self, master):
        frame = ttk.LabelFrame(master, text="Select Name", padding="5")
        frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        ttk.Label(frame, text="Name:", font=("Inter", 10)).grid(row=0, column=0, sticky="w", padx=5)
        name_menu = ttk.OptionMenu(frame, self.selected_name, self.selected_name.get(), *self.debug_names, command=lambda x: self._on_name_change())
        name_menu.grid(row=0, column=1, padx=5)
        name_menu.config(width=30)

    def _on_name_change(self, *args):
        self.user_info = self._get_user_info_by_name(self.selected_name.get())
        self.class_info = self.user_info['class']
        self.class_number = self.user_info['clno']
        self.name = self.user_info['name']
        self.grade = self._get_grade(self.user_info['dob'])
        self.gender = 'male' if self.user_info['gender'].upper().startswith('M') else 'female'
        self._create_user_info_section(self.master)
        self.update_gender_selection()

    def _get_grade(self, dob):
        """
        based on DOB compared to 1-9-2024.
        """
        cutoff = datetime(2024, 9, 1)
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        age = cutoff.year - dob_date.year - ((cutoff.month, cutoff.day) < (dob_date.month, dob_date.day))
        if age >= 16:
            return 'A'
        elif age >= 14:
            return 'B'
        else:
            return 'C'

    def _create_user_info_section(self, master):
        if hasattr(self, 'user_info_frame'):
            for widget in self.user_info_frame.winfo_children():
                widget.destroy()
            self.user_info_frame.destroy()

        self.user_info_frame = ttk.LabelFrame(master, text="Your Information", padding="10", relief="groove") # Reduced padding
        self.user_info_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5) # Reduced pady
        self.user_info_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.user_info_frame, text=f"Class: {self.class_info}", font=("Inter", 10, "bold")).grid(row=0, column=0, sticky="w", pady=1) # Reduced pady
        ttk.Label(self.user_info_frame, text=f"Class No.: {self.class_number}", font=("Inter", 10, "bold")).grid(row=1, column=0, sticky="w", pady=1) # Reduced pady
        ttk.Label(self.user_info_frame, text=f"Name: {self.name}", font=("Inter", 10, "bold")).grid(row=2, column=0, sticky="w", pady=1)
        house_colors = {
            'Virtue': 'red',
            'Trust': 'green',
            'Loyalty': 'purple',
            'Intellect': 'blue'
        }
        house = self.user_info['house']
        house_color = house_colors.get(house.capitalize(), 'black')
        house_row_frame = ttk.Frame(self.user_info_frame)
        house_row_frame.grid(row=3, column=0, sticky="w", pady=1)
        ttk.Label(house_row_frame, text="House:", font=("Inter", 10, "bold")).pack(side="left")
        ttk.Label(house_row_frame, text=house, font=("Inter", 10, "bold"), foreground=house_color).pack(side="left")

    def _create_sports_group_display(self, master):
        self.sports_group_label = ttk.Label(master, text="", font=("Inter", 11, "bold"), foreground="#10B981", wraplength=450) # Reduced wraplength
        self.sports_group_label.grid(row=3, column=0, sticky="ew", padx=20, pady=5) # Reduced pady

    def _create_event_sections(self, master):
        self.racing_events_frame = ttk.LabelFrame(master, text="Racing Events (Max 2)", padding="10", relief="groove") # Reduced padding
        self.racing_events_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=5) # Reduced pady
        self.racing_events_frame.grid_columnconfigure(0, weight=1)

        self.field_events_frame = ttk.LabelFrame(master, text="Field Events (Max 2)", padding="10", relief="groove") # Reduced padding
        self.field_events_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=5) # Reduced pady
        self.field_events_frame.grid_columnconfigure(0, weight=1)

    def _create_submit_button(self, master):
        """
        Creates the 'Submit Registration' button.
        Reduced pady.
        """
        submit_button = ttk.Button(master, text="Submit Registration", command=self.submit_registration, style="TButton")
        submit_button.grid(row=6, column=0, pady=10)
        master.style = ttk.Style()
        master.style.configure("TButton",
                               font=("Arial", 12, "bold"),
                               background="#1E90FF",
                               foreground="black",
                               padding=(10, 8),
                               relief="raised",
                               borderwidth=0)
        master.style.map("TButton",
                         background=[('active', '#4682B4')],
                         foreground=[('active', 'black')])
        master.style.configure("TCheckbutton", font=("Inter", 10))


    def update_gender_selection(self):
        """
        Updates the sports group display and regenerates the event checkboxes based on database gender.
        """
        selected_gender = self.gender
        gender_display = ""
        if selected_gender == "male":
            gender_display = "Boy's"
        elif selected_gender == "female":
            gender_display = "Girl's"

        if selected_gender:
            self.sports_group_label.config(text=f"Sports Group: {gender_display} {self.grade} Grade")
        else:
            self.sports_group_label.config(text="No gender information available.")

        for widget in self.racing_events_frame.winfo_children():
            widget.destroy()
        for widget in self.field_events_frame.winfo_children():
            widget.destroy()

        self.racing_checkbox_vars.clear()
        self.field_checkbox_vars.clear()
        self.racing_checkbox_widgets.clear()
        self.field_checkbox_widgets.clear()

        if selected_gender:
            def add_checkbox(frame, event_value, var_dict, widget_dict, row):
                var = tk.BooleanVar(self.master)
                var.trace_add("write", partial(self._event_selection_trace, var))
                cb = ttk.Checkbutton(frame, text=event_value, variable=var, style="TCheckbutton")
                cb.grid(row=row, column=0, sticky="w", pady=1)
                var_dict[event_value] = var
                widget_dict[event_value] = cb

            racing_events_for_grade = self.racing_events_data.get(self.grade, [])
            for i, event in enumerate(racing_events_for_grade):
                event_value = f"{gender_display} {self.grade} {event}"
                add_checkbox(self.racing_events_frame, event_value, self.racing_checkbox_vars, self.racing_checkbox_widgets, i)
            if not racing_events_for_grade:
                ttk.Label(self.racing_events_frame, text="No racing events available for this group.", font=("Inter", 9), foreground="#6B7280").grid(row=0, column=0, sticky="w")

            field_events_for_grade = self.field_events_data.get(self.grade, [])
            for i, event in enumerate(field_events_for_grade):
                event_value = f"{gender_display} {self.grade} {event}"
                add_checkbox(self.field_events_frame, event_value, self.field_checkbox_vars, self.field_checkbox_widgets, i)
            if not field_events_for_grade:
                ttk.Label(self.field_events_frame, text="No field events available for this group.", font=("Inter", 9), foreground="#6B7280").grid(row=0, column=0, sticky="w")

            if selected_gender == "female" and self.grade == "B":
                event_value = f"{gender_display} {self.grade} Softball"
                row = len(self.field_events_data.get(self.grade, []))
                add_checkbox(self.field_events_frame, event_value, self.field_checkbox_vars, self.field_checkbox_widgets, row)


        self.update_event_selection_limits()

    def _event_selection_trace(self, var, *args):
        self.update_event_selection_limits()

    def update_event_selection_limits(self):
        """
        Controls checkboxes
        """
        selected_racing_count = sum(var.get() for var in self.racing_checkbox_vars.values())
        selected_field_count = sum(var.get() for var in self.field_checkbox_vars.values())
        total_selected = selected_racing_count + selected_field_count

        for event_value, var in self.racing_checkbox_vars.items():
            widget = self.racing_checkbox_widgets[event_value]
            if var.get():
                widget.state(['!disabled'])
            elif total_selected >= 3 or selected_racing_count >= 2:
                widget.state(['disabled'])
            else:
                widget.state(['!disabled'])

        for event_value, var in self.field_checkbox_vars.items():
            widget = self.field_checkbox_widgets[event_value]
            if var.get():
                widget.state(['!disabled'])
            elif total_selected >= 3 or selected_field_count >= 2:
                widget.state(['disabled'])
            else:
                widget.state(['!disabled'])

    def submit_registration(self):
        """
        Mainly data checking
        """
        selected_racing = [event_value for event_value, var in self.racing_checkbox_vars.items() if var.get()]
        selected_field = [event_value for event_value, var in self.field_checkbox_vars.items() if var.get()]

        if not self.gender:
            messagebox.showwarning("Validation Error", "No gender information available.")
            return

        total_selected = len(selected_racing) + len(selected_field)
        if total_selected == 0:
            messagebox.showwarning("Validation Error", "Please select at least one event.")
            return
        if total_selected > 3:
            messagebox.showwarning("Validation Error", "You can select a maximum of 3 events in total. Please adjust your selection.")
            return
        if len(selected_racing) > 2:
            messagebox.showwarning("Validation Error", "You can select a maximum of 2 racing events. Please adjust your selection.")
            return
        if len(selected_field) > 2:
            messagebox.showwarning("Validation Error", "You can select a maximum of 2 field events. Please adjust your selection.")
            return

        registrationData = {
            'class': self.class_info,
            'class_no': self.class_number,
            'name': self.name,
            'gender': self.gender,
            'racing_events': selected_racing,
            'field_events': selected_field,
            'timestamp': int(datetime.now().timestamp()),
            'stu_id': self.user_info.get('stu_id', None)
        }
        success, msg = save_registration_to_db(registrationData)
        if success:
            messagebox.showinfo("Registration Summary",
                f"Registration for: {self.name}\n"
                f"Class: {self.class_info}, Class No.: {self.class_number}\n"
                f"Gender: {self.gender.capitalize()}\n\n"
                f"Selected Racing Events:\n{', '.join(selected_racing) if selected_racing else 'None'}\n\n"
                f"Selected Field Events:\n{', '.join(selected_field) if selected_field else 'None'}\n\n"
                f"{msg}"
            )
        else:
            messagebox.showerror("Error", msg)

    def __del__(self):
        try:
            if hasattr(self, 'conn'):
                pass
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SportsRegistrationApp(root)
    root.mainloop()

