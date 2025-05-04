import ttkbootstrap as tk

class ClipboardCopier(tk.Frame):
    def __init__(self, parent, value="Default ", label=""):
        super().__init__(parent)
        self.label = label
        self.value = value

        # Label to display the text
        self.variable_label = tk.Label(self, text=self.label, font=("Arial", 14))
        self.variable_value = tk.Label(self, text=self.value, font=("Arial", 14))
        self.variable_label.pack(pady=10)
        self.variable_value.pack(pady=10)

        # Copy button
        self.copy_button = tk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)

        # Status message
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.value)
        self.update()  # Keep clipboard data available
        self.status_label.config(text="Copied!")