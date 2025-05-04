import tkinter as tk

class TimeInputFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.active_time = tk.StringVar(value="start")
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()

        # --- Radio buttons ---
        radio_frame = tk.Frame(self)
        radio_frame.pack(anchor="w")
        tk.Radiobutton(radio_frame, text="Edit Start (ms)", variable=self.active_time, value="start", command=self.update_input_state).pack(side="left")
        tk.Radiobutton(radio_frame, text="Edit End (ms)", variable=self.active_time, value="end", command=self.update_input_state).pack(side="left")

        # --- Start time entry ---
        start_frame = tk.Frame(self)
        start_frame.pack(fill="x", pady=5)
        tk.Label(start_frame, text="Start Time (ms):").pack(side="left")
        self.start_entry = tk.Entry(start_frame, textvariable=self.start_time_var, width=12)
        self.start_entry.pack(side="left", padx=5)
        self.start_entry.bind("<FocusOut>", self.sync_times)

        # --- End time entry ---
        end_frame = tk.Frame(self)
        end_frame.pack(fill="x", pady=5)
        tk.Label(end_frame, text="End Time (ms):").pack(side="left")
        self.end_entry = tk.Entry(end_frame, textvariable=self.end_time_var, width=12)
        self.end_entry.pack(side="left", padx=5)
        self.end_entry.bind("<FocusOut>", self.sync_times)

        self.update_input_state()  # Set initial state

    def update_input_state(self):
        if self.active_time.get() == "start":
            self.start_entry.config(state="normal")
            self.end_entry.config(state="disabled")
        else:
            self.end_entry.config(state="normal")
            self.start_entry.config(state="disabled")

    def sync_times(self, event=None):
        try:
            if self.active_time.get() == "start":
                start = int(self.start_time_var.get())
                self.end_time_var.set(str(start + 30000))
            else:
                end = int(self.end_time_var.get())
                self.start_time_var.set(str(max(0, end - 30000)))
        except ValueError:
            # Invalid input — skip syncing
            pass

    def get_times_ms(self):
        """Return start and end as integers in milliseconds, or (None, None) if invalid."""
        try:
            start = int(self.start_time_var.get())
            end = int(self.end_time_var.get())
            return start, end
        except ValueError:
            return None, None
        
    def reset(self, start_ms=0):
        """Reset the time inputs to a given start_ms and start radio selected."""
        self.active_time.set("start")
        self.start_time_var.set(str(start_ms))
        self.end_time_var.set(str(start_ms + 30000))
        self.update_input_state()