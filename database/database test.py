import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from datetime import datetime

class SportsRegistrationApp:
    def __init__(self, master):
        self.master = master
        master.title("Sports Day Registration")
        # Adjusted geometry to be more compact, allowing for smaller screens too
        master.geometry("550x700")
        master.resizable(False, False) # Prevent resizing to maintain compact layout without scroll

        # Configure column weights for basic responsiveness - keep it for main content
        master.grid_columnconfigure(0, weight=1)

        # --- Gmail Selection at Top ---
        self.debug_gmails = [
            's20201033@carmelss.edu.hk',
            's20011313@carmelss.edu.hk',
            's20122020@carmelss.edu.hk',
            's20229999@carmelss.edu.hk',
            's20242009@carmelss.edu.hk'
        ]
        self.selected_gmail = tk.StringVar(value=self.debug_gmails[0])
        # Call _create_gmail_selector once for initial setup
        self._create_gmail_selector(master)

        # --- User Info (Mocked for Firebase) ---
        self.user_info = {
            'class': '4A',
            'clno': '10',
            'name': 'John Doe',
            'dob': '2010-05-15',
            'gender': 'M',
            'house': 'Virtue'
        }

        # Extract user details from the mocked data
        self.class_info = self.user_info['class']
        self.class_number = self.user_info['clno']
        self.name = self.user_info['name']
        self.grade = self._get_grade(self.user_info['dob'])
        self.gender = 'male' if self.user_info['gender'].upper().startswith('M') else 'female'

        # --- Event Data Definitions ---
        self.racing_events_data = {
            'A': ["100m", "200m", "400m", "800m", "1500m"],
            'B': ["100m", "200m", "400m", "800m", "1500m"],
            'C': ["60m", "100m", "200m", "400m", "800m", "1500m"]
        }
        self.field_events_data = {
            'A': ["High Jump", "Javelin", "Long Jump", "Shot Put"],
            'B': ["High Jump", "Javelin", "Long Jump", "Shot Put"], # Removed "Softball Throw" for general B grade
            'C': ["High Jump", "Long Jump", "Shot Put", "Softball"]
        }

        # --- Tkinter Variables for UI State Management ---
        self.gender_var = tk.StringVar(master)
        self.gender_var.set("") # Default empty selection

        self.racing_checkbox_vars = {}
        self.field_checkbox_vars = {}
        self.racing_checkbox_widgets = {}
        self.field_checkbox_widgets = {}

        # --- UI Element Creation ---
        self._create_header(master)
        # _create_gmail_selector is already called in __init__
        self._create_user_info_section(master)
        self._create_sports_group_display(master)
        self._create_event_sections(master)
        self._create_submit_button(master)

        # Set gender from mocked data (already done above, but good to ensure consistency)
        self.gender = 'male' if self.user_info['gender'].upper().startswith('M') else 'female'

        # Initial update of the UI
        self.update_gender_selection()

    def _create_header(self, master):
        """
        Creates the application's header section.
        Reduced pady for more compactness.
        """
        header_frame = ttk.Frame(master, padding="15") # Reduced padding
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(header_frame, text="Sports Day Registration", font=("Inter", 20, "bold"), foreground="#4F46E5").grid(row=0, column=0, pady=5) # Reduced pady
        ttk.Label(header_frame, text="Welcome to the Sports Day registration portal!", font=("Inter", 10), foreground="#4B5563").grid(row=1, column=0, pady=0)

    def _create_gmail_selector(self, master):
        frame = ttk.LabelFrame(master, text="Select Gmail for Debugging", padding="5")
        frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        ttk.Label(frame, text="Gmail:", font=("Inter", 10)).grid(row=0, column=0, sticky="w", padx=5)
        gmail_menu = ttk.OptionMenu(frame, self.selected_gmail, self.selected_gmail.get(), *self.debug_gmails, command=lambda x: self._on_gmail_change())
        gmail_menu.grid(row=0, column=1, padx=5)
        gmail_menu.config(width=30)

    def _on_gmail_change(self):
        """
        Event handler for gmail selection change.
        Loads user info for the selected gmail and updates the UI.
        """
        # Mocked user info change for selected gmail
        # In a real app, this would fetch data from a database based on selected_gmail
        current_selected_gmail = self.selected_gmail.get()
        if current_selected_gmail == 's20201033@carmelss.edu.hk':
            self.user_info = {
                'class': '4A',
                'clno': '10',
                'name': 'John Doe',
                'dob': '2010-05-15',
                'gender': 'M',
                'house': 'Virtue'
            }
        elif current_selected_gmail == 's20011313@carmelss.edu.hk':
            self.user_info = {
                'class': '6B',
                'clno': '25',
                'name': 'Jane Smith',
                'dob': '2008-11-20',
                'gender': 'F',
                'house': 'Trust'
            }
        elif current_selected_gmail == 's20122020@carmelss.edu.hk':
            self.user_info = {
                'class': '2C',
                'clno': '5',
                'name': 'Peter Jones',
                'dob': '2012-03-01',
                'gender': 'M',
                'house': 'Loyalty'
            }
        elif current_selected_gmail == 's20229999@carmelss.edu.hk':
            self.user_info = {
                'class': '5D',
                'clno': '12',
                'name': 'Alice Brown',
                'dob': '2009-07-07',
                'gender': 'F',
                'house': 'Intellect'
            }
        elif current_selected_gmail == 's20242009@carmelss.edu.hk':
            self.user_info = {
                'class': '1A',
                'clno': '1',
                'name': 'Bob White',
                'dob': '2013-09-25',
                'gender': 'M',
                'house': 'Virtue'
            }
        else:
            # Default or error case
            self.user_info = {
                'class': 'N/A',
                'clno': 'N/A',
                'name': 'Unknown User',
                'dob': '2010-01-01',
                'gender': 'M',
                'house': 'Virtue'
            }


        self.class_info = self.user_info['class']
        self.class_number = self.user_info['clno']
        self.name = self.user_info['name']
        self.grade = self._get_grade(self.user_info['dob'])
        self.gender = 'male' if self.user_info['gender'].upper().startswith('M') else 'female'
        self._create_user_info_section(self.master) # Re-create user info section to update labels
        self.update_gender_selection() # Update event checkboxes based on new gender/grade

    def _get_grade(self, dob):
        """
        Determines the sports grade (A, B, or C) based on the date of birth compared to 1-9-2024.
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
        """
        Creates the section displaying the logged-in user's information.
        Reduced padding and pady for compactness.
        """
        # Clear existing user info frame content if it exists
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
        # Add house display with color only for house name, aligned properly
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
        """
        Creates the label that displays the derived sports group.
        Reduced pady.
        """
        self.sports_group_label = ttk.Label(master, text="", font=("Inter", 11, "bold"), foreground="#10B981", wraplength=450) # Reduced wraplength
        self.sports_group_label.grid(row=3, column=0, sticky="ew", padx=20, pady=5) # Reduced pady

    def _create_event_sections(self, master):
        """
        Creates the parent frames for racing and field events.
        Reduced padding and pady for compactness.
        """
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
        submit_button.grid(row=6, column=0, pady=10) # Reduced pady
        master.style = ttk.Style()
        master.style.configure("TButton",
                               font=("Arial", 12, "bold"), # Changed font to Arial for better readability
                               background="#1E90FF", # Kept background color as Dodger Blue
                               foreground="black", # Changed foreground color to black for better readability
                               padding=(10, 8), # Reduced padding
                               relief="raised",
                               borderwidth=0)
        master.style.map("TButton",
                         background=[('active', '#4682B4')], # Kept active background color as Steel Blue
                         foreground=[('active', 'black')]) # Changed active foreground color to black
        # Add style for checkbuttons as well
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

        # Clear all existing checkboxes from the frames before repopulating
        for widget in self.racing_events_frame.winfo_children():
            widget.destroy()
        for widget in self.field_events_frame.winfo_children():
            widget.destroy()

        self.racing_checkbox_vars.clear()
        self.field_checkbox_vars.clear()
        self.racing_checkbox_widgets.clear()
        self.field_checkbox_widgets.clear()

        if selected_gender:
            # Helper to add checkboxes with correct trace
            def add_checkbox(frame, event_value, var_dict, widget_dict, row):
                var = tk.BooleanVar(self.master)
                # Use partial to avoid late binding bug in lambda
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

            # Add "Softball" only for girls' B grade
            if selected_gender == "female" and self.grade == "B":
                event_value = f"{gender_display} {self.grade} Softball"
                row = len(self.field_events_data.get(self.grade, [])) # Get current number of field events to place softball correctly
                add_checkbox(self.field_events_frame, event_value, self.field_checkbox_vars, self.field_checkbox_widgets, row)


        self.update_event_selection_limits()

    def _event_selection_trace(self, var, *args):
        self.update_event_selection_limits()

    def update_event_selection_limits(self):
        """
        Enables/disables checkboxes based on selection rules.
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
        Collects selected events and displays a summary in a messagebox.
        Includes validation checks.
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

        racing_str = "\n".join(selected_racing) if selected_racing else "None"
        field_str = "\n".join(selected_field) if selected_field else "None"

        messagebox.showinfo(
            "Registration Summary",
            f"Registration for: {self.name}\n"
            f"Class: {self.class_info}, Class No.: {self.class_number}\n"
            f"Gender: {self.gender.capitalize()}\n\n"
            f"Selected Racing Events:\n{racing_str}\n\n"
            f"Selected Field Events:\n{field_str}"
        )

    def __del__(self):
        """
        Ensures the database connection is closed when the application is terminated.
        (This part is commented out as there's no actual database connection in this mock-up)
        """
        # Use context manager for safety
        try:
            if hasattr(self, 'conn'):
                # self.conn.close() # Uncomment if you add a database connection
                pass
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SportsRegistrationApp(root)
    root.mainloop()
