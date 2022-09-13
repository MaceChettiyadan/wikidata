
import math
import tkinter as tk
from tkinter import ttk
import functions as f
import sv_ttk
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
matplotlib.use('TkAgg')

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Make the app responsive
        for index in (0, 1, 2, 3, 4, 5, 6, 7):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
            
        self.graphs = []
        # Create widgets
        self.setup_gui() 
        
    def submit_wiki_name(self):
        self.error_label.config(text="")
        name = self.lookup_input.get()
        page = f.get_page(name)
        print(page)
        if not page:
            self.error_label.config(text="Page '" + name + "' not found. Perhaps your request is too ambiguous?")
            return
        treeview_data = f.extract_headers(page.html())
        #clear treeview
        self.treeview.delete(*self.treeview.get_children())
        for item in treeview_data:
            parent, iid, text, values = item
            self.treeview.insert(
                parent=parent, index="end", iid=iid, text=text, values=values
            )

            if not parent or iid in {8, 21}:
                self.treeview.item(iid, open=True)  # Open parents

        # Select and scroll
        i = len(treeview_data)
        while i > 0:
            try:
                self.treeview.selection_set(str(len(treeview_data) - 1))
                break
            except tk.TclError:
                i -= 1
                continue
        self.treeview.see("7")
        
        title = page.title
        #set title of wiki info
        self.wiki_info_title.config(text=title)
        #set summary of wiki info
        if len(page.summary.split('.')) >= 3:
            tss = page.summary.split(".")[0] + "." + page.summary.split(".")[1] + "." + page.summary.split(".")[2] + "."
        elif len(page.summary.split('.')) == 2:
            tss = page.summary.split(".")[0] + "." + page.summary.split(".")[1] + "."
        else:
            tss = page.summary.split(".")[0] + "."
        self.wiki_info_summary.config(text=tss)
        self.wiki_info_popularity.config(text="Popularity: " + str(len(page.links)))
        
        #self.setup_graph_view(page.title, page.links)
        
    def setup_graph_view(self, centre, links):
        #remove old graph
        for graph in self.graphs:
            graph.destroy()
            
        
        #create graph G with centre node and links, each node has a position
        G = nx.Graph()
        G.add_node(centre, pos=(0, 0))
        #generate array of tuples of positions in circle
        poss = []
        for x in range(len(links)):
            poss.append((0.5 * math.cos(2 * math.pi * x / len(links)), 0.5 * math.sin(2 * math.pi * x / len(links))))
        
        for link in links:
            G.add_node(link, pos=poss[links.index(link)])
            G.add_edge(centre, link)
        
        
        
        # position is stored as node attribute data for random_geometric_graph
        pos = nx.get_node_attributes(G, "pos")
        
        dmin = 1
        ncenter = 0
        for n in pos:
            x, y = pos[n]
            d = (x - 0.5) ** 2 + (y - 0.5) ** 2
            if d < dmin:
                ncenter = n
                dmin = d
        
        # color by path length from node near center
        p = dict(nx.single_source_shortest_path_length(G, ncenter))
        
        fig = plt.figure(figsize=(4, 6))
        nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=list(p.keys()),
            node_size=80,
            node_color=list(p.values()),
            cmap=plt.cm.Reds_r,
        )

        plt.xlim(-0.05, 1.05)
        plt.ylim(-0.05, 1.05)
        plt.axis("off")
        figure_canvas = FigureCanvasTkAgg(fig, self.graph_view_frame)
        nav = NavigationToolbar2Tk(figure_canvas, self.graph_view_frame)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.graphs.append(figure_canvas.get_tk_widget())
        #append navigation toolbar to graph view frame
        self.graphs.append(nav)
        

    def setup_gui(self):
        #title frame
        self.title_frame = ttk.LabelFrame(self, text="Info", padding=(20, 10)) #inside padding
        #create 20 rows and 2 columns
        for index in range(20):
            self.title_frame.rowconfigure(index=index, weight=1)
            if index < 1:
                self.title_frame.columnconfigure(index=index, weight=1)
        self.title_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=2, columnspan=2 #outside padding
        )
        #title label
        self.title_label = ttk.Label(self.title_frame, text="WikiData", font=("-size", 25, "-weight", "bold"))
        self.title_label.grid(row=0, column=0, sticky="nsew")
        #wikidata description
        self.main_desc_label = ttk.Label(self.title_frame, text="A wiki lookup tool.")
        self.main_desc_label.grid(row=1, column=0, sticky="nsew")
        #dark mode switch
        self.dark_mode_switch = ttk.Checkbutton(self.title_frame, text="Dark Mode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
        self.dark_mode_switch.grid(row=2, column=0, sticky="nsew")
        #quit button
        self.quit_button = ttk.Button(self.title_frame, text="Quit", command=self.quit, style="Accent.TButton")
        self.quit_button.grid(row=3, column=0, sticky="nsew")
        #version label
        self.version_label = ttk.Label(self.title_frame, text="©Mace Chettiyadan | Version 1.0.0", font=("-size", 10))
        self.version_label.grid(row=20, column=2, sticky="nsew")
        
        #lookup frame
        self.lookup_frame = ttk.LabelFrame(self, text="Lookup", padding=(20, 10))
        self.lookup_frame.grid(
            row = 0, column = 2, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=2
        )
        #lookup input field
        self.lookup_input = ttk.Entry(self.lookup_frame, width=30)
        self.lookup_input.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")
        #set lookup_input to span whole row
        self.lookup_input.insert(0, "Enter Wiki Name")
        #submit button
        self.submit_button = ttk.Button(self.lookup_frame, text="Lookup", style="Accent.TButton", command=self.submit_wiki_name)
        self.submit_button.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew")
        #red error text
        self.error_label = ttk.Label(self.lookup_frame, text="", foreground="red")
        self.error_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
        #lookup how to label
        self.lookup_desc_label = ttk.Label(self.lookup_frame, text="Hint: Try not to use spaces. For example 'AmongUs' instead of 'Among Us'.", font=("-size", 10))
        self.lookup_desc_label.grid(row=2, column=0, columnspan=2, sticky="nsew")
        #seperator row 2
        self.warning_seperator = ttk.Separator(self.lookup_frame, orient="horizontal")
        self.warning_seperator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 10))
        self.lookup_warning_label = ttk.Label(self.lookup_frame, text="Also, do not click anywhere when the program is looking up a wiki.", font=("-size", 10))
        self.lookup_warning_label.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.label_p2 = ttk.Label(self.lookup_frame, text="Lookup takes time (downloading data) and python is not multithreaded so it crashes.", font=("-size", 10))
        self.label_p2.grid(row=5, column=0, columnspan=2, sticky="nsew")
        
        
        #wiki info frame
        self.wiki_info_frame = ttk.LabelFrame(self, text="Wiki Info", padding=(10, 10))
        self.wiki_info_frame.grid(
            row=2, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=6, columnspan=3
        )
        #title of wiki info
        self.wiki_info_title = ttk.Label(self.wiki_info_frame, text="e", font=("-size", 20, "-weight", "bold"), cursor='hand2')
        self.wiki_info_title.bind("<Button-1>", lambda e: f.open_page(self.wiki_info_title.cget("text")))
        self.wiki_info_title.grid(row=0, column=0, sticky="nsew")
        #summary of wiki info, wrap length is 750
        self.wiki_info_summary = ttk.Label(self.wiki_info_frame, text="e", wraplength=750, font=("-size", 15))
        self.wiki_info_summary.grid(row=1, column=0, sticky="nsew")
        self.summ_divider = ttk.Separator(self.wiki_info_frame, orient="horizontal", style="Divider.TSeparator")
        self.summ_divider.grid(row=2, column=0, sticky="ew", pady=10)
        #popularity label
        self.wiki_info_popularity = ttk.Label(self.wiki_info_frame, text="Popularity: e", font=("-size", 15))
        self.wiki_info_popularity.grid(row=3, column=0, sticky="nsew")
        
        #headers frame
        self.wiki_headers_frame = ttk.LabelFrame(self, text="Wiki Headers", padding=(20, 10))
        self.wiki_headers_frame.grid(
            row=0, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=4, columnspan=6
        )
        
        self.scrollbar = ttk.Scrollbar(self.wiki_headers_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        self.treeview = ttk.Treeview(
            self.wiki_headers_frame,
            columns=("1", "2"),
            height=10,
            selectmode="browse",
            show=("tree",),
            yscrollcommand=self.scrollbar.set,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=120)
        self.treeview.column(1, anchor="w", width=120)
        self.treeview.column(2, anchor="w", width=120)
        
        #graph view frame
        self.graph_view_frame = ttk.LabelFrame(self, text="Graph View", padding=(20, 10))
        self.graph_view_frame.grid(
            row=4, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=4, columnspan=6
        )

def main():
    root = tk.Tk()
    root.title("WikiData")

    sv_ttk.set_theme("light")

    app = App(root)
    app.pack(fill="both", expand=True)

    root.update_idletasks()  # Make sure every screen redrawing is done

    width, height = root.winfo_width(), root.winfo_height()
    x = int((root.winfo_screenwidth() / 2) - (width / 2))
    y = int((root.winfo_screenheight() / 2) - (height / 2))

    # Set a minsize for the window, and place it in the middle
    root.minsize(width, height)
    root.geometry(f"+{x}+{y}")
    # set root fullscreen
    #root.attributes("-fullscreen", True)
    root.mainloop()


if __name__ == "__main__":
    main()
    
    
#todo
#multithreading
#dark theme support with graph view
#images for articles
#full stop bug
