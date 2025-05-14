import random
import json
import threading

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
import re

# --- Helper Functions ---  

def create_plot(block_data,**kwargs):
    kwargs_copy = {key:float(value) for key, value in kwargs.items() if value != "None"}
    data = snafs.get_spikes_from_cellattachedrecording(block_data.segments[0], block_data.file_origin, 0, plot="on", **kwargs_copy)
    return data, kwargs
loading_messages = [
        "Depolarizing neurons...",
        "Calculating action potentials...",
        "Synapsing with your data...",
        "Firing up those dendrites...",
        "Axon-ally transferring information...",
        "Myelin-ating your requests...",
        "Stimulating the prefrontal cortex...",
        "Waiting for neurotransmitter release...",
        "Crossing the synaptic cleft...",
        "Recruiting more glial cells...",
        "Neural network in training...",
        "Increasing membrane potential...",
        "Propagating signals...",
        "Brain storm in progress...",
        "Connecting neuronal pathways...",
        "Generating spike trains...",
        "Patching those ion channels...",
        "Calculating resting potential...",
        "Summating post-synaptic potentials...",
        "Waiting for refractory period to end..."
    ]
# --- Main App ---

class BlockPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Plotter")
        self.style = tk.Style("darkly")
        plt.style.use('dark_background')
        self.current_block = None
        self.results = {}
        self.df_data = []
        self.build_interface()

    def load_neuron(self, neuron_id):
        neuron = SingleNeuron(neuron_id)
        return neuron
    

    def show_loading(self, message="Loading..."):
        # Store current panes and remove them from the paned window
        if message == "Loading...":
            message = random.choice(loading_messages)
        self.paned_window.forget(self.left_panel)
        self.paned_window.forget(self.right_panel)
        
        # Create and show the loading message in the main frame
        self.loading_label = tk.Label(self.main_frame, text=message, font=("Arial", 12))
        self.loading_label.pack(expand=True, pady=20)
        
        self.root.config(cursor="watch")
        self.root.update()

    def hide_loading(self):
        # Remove the loading message
        if hasattr(self, "loading_label"):
            self.loading_label.destroy()
        
        # Add the panels back to the paned window
        self.paned_window.add(self.left_panel, weight=1)
        self.paned_window.add(self.right_panel, weight=3)
        
        self.root.config(cursor="")
        self.root.update()
    
    def finish_loading_folder(self):
        # Clear existing items in the treeview
        for item in self.block_listbox.get_children():
            self.block_listbox.delete(item)
            
        # Add new items
        for idx, block in enumerate(self.neuron.blocks):
            self.block_listbox.insert('', 'end', iid=str(idx), text=block.file_origin)
        
        # Reset results for the new neuron
        self.results = {}
        self.df_data = []
        self.current_block = None
        self.hide_loading()

    def toggle_theme(self):
        new_theme = "litera" if self.style.theme.name == "darkly" else "darkly"
        plt_theme = "dark_background" if new_theme == "darkly" else "default"
        plt.style.use(plt_theme)
        self.style.theme_use(new_theme)
        # Redraw the current plot with the new theme if one exists
        if hasattr(self, 'current_block') and self.current_block:
            self.create_plot_for_block()
    
    def build_interface(self):
        # --- Top Menu ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(top_frame, text="Load Neuron", command=self.select_folder).pack(side="left")
        tk.Button(top_frame, text="Dark/Light mode", command=self.toggle_theme).pack(side="left")
        tk.Button(top_frame, text="Export CSV", command=self.export_csv).pack(side="right")
        tk.Button(top_frame, text="Export JSON", command=self.export_json).pack(side="right")

        # --- Main Split View ---
        self.main_frame = tk.Frame(self.root)
        
        self.main_frame.pack(fill="both", expand=True)
        # --- Paned Window ---
        self.paned_window = tk.PanedWindow(self.main_frame, orient="horizontal")
        self.paned_window.pack(fill="both", expand=True)
        # --- Left Block List ---
        self.left_panel = tk.Frame(self.paned_window)
        self.block_listbox = tk.Treeview(self.left_panel)
        self.block_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.block_listbox.bind("<<TreeviewSelect>>", self.on_block_select)

        # --- Right Panel ---
        self.right_panel = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_panel, weight=1)
        self.paned_window.add(self.right_panel, weight=3)
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
            entry.bind("<Return>", lambda event: self.create_plot_for_block())
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

    
    def process_neuron(self, folder_path):
        neuron_id = os.path.basename(folder_path)
        self.neuron = self.load_neuron(neuron_id)
    
    def select_folder(self):
        # Create and show QueryDialog
        dialog = tk.dialogs.QueryDialog(
            parent=self.root,
            title="Neuron Intake", 
            prompt="Enter the Neuron ID:",
            initialvalue=""
        )
        dialog.show()
        neuron_name = dialog.result

        
        # Check if user cancelled or entered empty string
        if neuron_name is None or neuron_name.strip() == "":
            tk.MessageDialog(
                parent=self.root,
                title="No Input", 
                message="Please enter a Neuron ID.",
                alert=True
            )
            return

        # Validate neuron name format
        if not re.match(r"^\d{8}[A-Za-z](\d)?$", neuron_name):
            tk.MessageDialog(
                parent=self.root,
                title="Invalid Neuron ID", 
                message="Neuron ID must be in the format 'YYYYMMDD' followed by a letter or a letter and a number.",
                alert=True
            )
            return
        
        # Proceed with loading
        self.show_loading()

        

        def task():
            self.process_neuron(neuron_name)
            self.root.after(0, self.finish_loading_folder)

        threading.Thread(target=task).start()
    def finish_loading_folder(self):
    # Clear existing items in the treeview
        for item in self.block_listbox.get_children():
            self.block_listbox.delete(item)
            
        # Add new items
        for idx, block in enumerate(self.neuron.blocks):
            self.block_listbox.insert('', 'end', iid=str(idx), text=block.file_origin)
        
        # Reset results for the new neuron
        self.results = {}
        self.df_data = []
        self.current_block = None
        self.hide_loading()

    def on_block_select(self, event):
        selected = self.block_listbox.selection()
        if not selected:
            return

        # Save previous block results
        if self.current_block:
            self.save_current_block_results()

        # Convert string ID back to integer index
        idx = int(selected[0])
        self.current_block = self.neuron.blocks[idx]

        # Reset sliders to default (optional: keep per-block values)
        for param, default_val in self.params.items():
            self.slider_vars[param].set(default_val)
        
        # Clear previous plot
        self.clear_plot()
        # Create new plot
        self.create_plot_for_block()
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
        plt_theme = "dark_background" if self.style.theme.name == "darkly" else "default"
        plt.style.use(plt_theme)
        values = {param:var.get() for param, var in self.slider_vars.items()}

        data, result = create_plot(self.current_block, **values)
        df_dict_result, self.fig = data[:2]
        try:
            self.mean = data[2]
            self.variance = data[3]
            self.mean_label.set_value(self.mean)
            self.variance_label.set_value(self.variance)

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
