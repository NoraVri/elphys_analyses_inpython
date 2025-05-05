import json
import threading
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
import csv
import pandas as pd
import singleneuron_analyses_functions as snafs
from singleneuron_class import SingleNeuron
import ttkbootstrap as tk
from ttkbootstrap.constants import *
from gui_components.clipboard_copier import ClipboardCopier

# --- Helper Functions ---  

def create_plot(block_data,**kwargs):
    kwargs_copy = {key:float(value) for key, value in kwargs.items() if value != "None"}
    data = snafs.get_spikes_from_cellattachedrecording(block_data.segments[0], block_data.file_origin, 0, plot="on", **kwargs_copy)
    return data, kwargs

# --- Main App ---

class BlockPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Plotter")
        self.style = tk.Style("darkly")
        self.current_block = None
        self.results = {}
        self.df_data = []
        self.build_interface()

    def load_neuron(self, neuron_id):
        neuron = SingleNeuron(neuron_id)
        return neuron
    

    def show_loading(self, message="Loading..."):
        if hasattr(self, "right_panel"):
            self.right_panel.pack_forget()

        self.loading_label = tk.Label(self.main_frame, text=message, font=("Arial", 12))
        self.loading_label.pack(pady=20)

        self.root.config(cursor="watch")
        self.root.update()

    def hide_loading(self):
        if hasattr(self, "loading_label"):
            self.loading_label.destroy()

        self.right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.root.config(cursor="")
        self.root.update()
    
    def toggle_theme(self):
        new_theme = "litera" if self.style.theme.name == "darkly" else "darkly"
        plt_theme = "dark_background" if new_theme == "darkly" else "default"
        plt.style.use(plt_theme)
        self.style.theme_use(new_theme)
    
    def build_interface(self):
        # --- Top Menu ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(top_frame, text="Select Folder", command=self.select_folder).pack(side="left")
        tk.Button(top_frame, text="Dark/Light mode", command=self.toggle_theme).pack(side="left")
        tk.Button(top_frame, text="Export CSV", command=self.export_csv).pack(side="right")
        tk.Button(top_frame, text="Export JSON", command=self.export_json).pack(side="right")

        # --- Main Split View ---
        main_frame = tk.Frame(self.root)
        self.main_frame = main_frame
        main_frame.pack(fill="both", expand=True)

        # --- Left Block List ---
        self.block_listbox = tk.Treeview(main_frame)
        self.block_listbox.pack(side="left", fill="y", padx=5, pady=5)
        self.block_listbox.bind("<<TreeviewSelect>>", self.on_block_select)

        # --- Right Panel ---
        self.right_panel = tk.Frame(main_frame)
        self.right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # --- Sliders ---
        self.slider_vars = {}
        self.sliders = []
        self.params = {
            "detection_noisemultiplier":10,
            "detection_threshold": None,
            "getbaseline_lpfilter_freq":0.5,
            "getnoise_hpfilterfreq": 5000,
            "t_start_inms": None,
            "t_end_inms": None,
        }
        
        button_frame = tk.Frame(self.right_panel)
        button_frame.pack(fill='x', pady=5)

        for i in self.params:
            var = tk.IntVar()

            frame = tk.Frame(button_frame)
            frame.pack(side="left", padx=5)

            tk.Label(frame, text=f"{i}:").pack(side="top")

            var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=var, width=10)
            entry.pack(side="top")
            self.slider_vars[i] = var
            self.slider_vars[i].set(self.params[i])  # Set default value
            self.sliders.append(entry)

        # --- Create Mean and Variance Labels ---
        self.mean = 0
        self.variance = 0

        self.mean_label = ClipboardCopier(button_frame, value=self.mean, label="Mean")
        self.mean_label.pack(side="left", padx=5)
        self.variance_label = ClipboardCopier(button_frame, value=self.variance, label="Variance")
        self.variance_label.pack(side="left", padx=5)
        # --- Create Plot Button ---
        self.plot_btn = tk.Button(self.right_panel, text="Create Plot", command=self.create_plot_for_block)
        self.plot_btn.pack(pady=5)

        # --- Plot Display Frame ---
        self.plot_frame = tk.Frame(self.right_panel)
        self.plot_frame.pack(fill='both', expand=True)
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)

    
    def process_folder(self, folder_path):
        neuron_id = os.path.basename(folder_path)
        self.neuron = self.load_neuron(neuron_id)
    
    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        
        self.show_loading("Processing folder...")

        def task():
            self.process_folder(folder)
            self.root.after(0, self.finish_loading_folder)

        threading.Thread(target=task).start()
    def finish_loading_folder(self):
        for idx, block in enumerate(self.neuron.blocks):
            self.block_listbox.insert('', 'end', iid=idx, text=block.file_origin)
        self.results = {}
        self.hide_loading()

    def on_block_select(self, event):
        selected = self.block_listbox.selection()
        if not selected:
            return

        # Save previous block results
        if self.current_block:
            self.save_current_block_results()

        self.current_block = self.neuron.blocks[int(selected[0])]


        # Reset sliders to default (optional: keep per-block values)
        for param, default_val in self.params.items():
            self.slider_vars[param].set(default_val)
        # Clear previous plot
        self.clear_plot()

        # Show simple text placeholder until "Create Plot" is clicked
        tk.Label(self.plot_frame, text=f"Loaded: {self.current_block.file_origin}", font=("Arial", 12)).pack()
    def clear_plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
    def bind_plot_resizing(self):
        self.plot_frame.bind("<Configure>", self.resize_figure)

    def resize_figure(self, event):
        if hasattr(self, "canvas") and hasattr(self, "fig"):
            width_in = event.width / self.fig.dpi
            height_in = event.height / self.fig.dpi
            self.fig.set_size_inches(width_in, height_in, forward=True)
            self.canvas.draw()
    
    def create_plot_for_block(self):
        if not self.current_block:
            return

        values = {param:var.get() for param, var in self.slider_vars.items()}

        data, result = create_plot(self.current_block, **values)
        df_dict_result, self.fig = data[:2]
        try:
            self.mean = data[2]
            self.variance = data[3]
            self.mean_label.variable_value.config(text=self.mean)
            self.variance_label.variable_value.config(text=self.variance)

        except IndexError:
            pass

        self.df_data.append(df_dict_result)
        # Save result for export
        self.results[self.current_block.file_origin] = result

        # Clear previous plot
        self.clear_plot()
    
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.bind_plot_resizing()
        toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        toolbar.update()
        toolbar.pack()
        plt.close(self.fig)



    def save_current_block_results(self):
        if not self.current_block:
            return

        # Only save if plot was generated
        if self.current_block not in self.results:
            return
        block_results = {
            param: var.get() for param, var in self.slider_vars.items()
        }
        self.results[self.current_block.file_origin].update(block_results)

    def export_csv(self):


        if not self.df_data:
            messagebox.showwarning("No Data", "No results to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        all_cellattachedspikes_dict = snafs.make_cellattachedspikepeaks_dictionary()
        for data_dict in self.df_data:
            for key in all_cellattachedspikes_dict:
                all_cellattachedspikes_dict[key] += list(data_dict[key])
                
        
        try:
            cellattachedspikes = pd.DataFrame(all_cellattachedspikes_dict).round(decimals=2)
            cellattachedspikes.to_csv(path, index=False)
            # Save the DataFrame to a CSV file

            messagebox.showinfo("Success", f"Exported to {path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def export_json(self):
        if not self.results:
            messagebox.showwarning("No Data", "No results to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not path:
            return

        # Write JSON
        try:
            with open(path, 'w') as f:
                json.dump(self.results, f, indent=4)
            messagebox.showinfo("Success", f"Exported to {path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
# --- Run the App ---
if __name__ == "__main__":
    root  = tk.Window(themename="darkly")
    app = BlockPlotterApp(root)
    root.mainloop()
