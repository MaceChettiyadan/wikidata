
import tkinter as tk
from tkinter import ttk
import functions as f
import sv_ttk
import plotly

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Make the app responsive
        for index in (0, 1, 2, 3, 4, 5, 6, 7):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create widgets
        self.setup_gui()
        
    def submit_wiki_name(self):
        name = self.lookup_input.get()
        page = f.get_page(name)
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
        self.title_label = ttk.Label(self.title_frame, text="WikiData", font=("-size", 25, "-weight", "bold"),)
        self.title_label.grid(row=0, column=0, sticky="nsew")
        #dark mode switch
        self.dark_mode_switch = ttk.Checkbutton(self.title_frame, text="Dark Mode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
        self.dark_mode_switch.grid(row=1, column=0, sticky="nsew")
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
        #lookup how to label
        self.lookup_desc_label = ttk.Label(self.lookup_frame, text="Hint: Try not to use spaces. For example 'AmongUs' instead of 'Among Us'.", font=("-size", 10))
        self.lookup_desc_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
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
    root.attributes("-fullscreen", True)
    root.mainloop()


if __name__ == "__main__":
    main()