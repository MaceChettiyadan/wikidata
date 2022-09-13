
import io
import tkinter as tk
from tkinter import ttk
import functions as f
import sv_ttk
import tkinter as tk
import tkinter as tk
from PIL import Image, ImageTk
from urllib.request import urlopen
from supabase import create_client, Client

url = 'https://pqowrgcliihcpbmyiqio.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBxb3dyZ2NsaWloY3BibXlpcWlvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY2MzA2MTMzNiwiZXhwIjoxOTc4NjM3MzM2fQ.wJ77NwuINzY7JwL29wp_f1o4kZ1SRXjKgl6h7neVYlQ'
supabase: Client = create_client(url, key)


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Make the app responsive
        for index in (0, 1, 2, 3, 4, 5, 6, 7):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
            
        self.page = None
        self.stats = []
        # Create widgets
        self.setup_gui() 
        
    def submit_wiki_name(self):
        self.error_label.config(text="")
        name = self.lookup_input.get()
        self.page = f.get_page(name)
        
        if not self.page:
            self.error_label.config(text="self.page '" + name + "' not found. Perhaps your request is too ambiguous?")
            return
        treeview_data = f.extract_headers(self.page.html())
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
                self.treeview.see(str(len(treeview_data) - 1))
                break
            except tk.TclError:
                i -= 1
                continue
        
        title = self.page.title
        #set title of wiki info
        self.wiki_info_title.config(text=title)
        #set summary of wiki info
        tss = ""
        #set tss to nearest sentence to the first 1000 characters of the summary
        tss = f.get_summary(self.page.summary, 1000)
        self.wiki_info_summary.config(text=tss)
        self.wiki_info_popularity.config(text="Popularity: " + str(len(self.page.links)))
        self.wiki_info_length.config(text="Length: " + str(len(self.page.content)))
        if len(self.page.images) > 0:
            try:
                image = self.page.images[0]
                u = urlopen(image)
                raw = u.read()
                u.close()
                im = Image.open(io.BytesIO(raw))
                ratio = im.width/im.height
                photo = ImageTk.PhotoImage(im.resize((int(200*ratio), 200)))
                self.image_overview.config(image=photo)
                self.image_overview.image = photo
            except:
                print('No image.')
                self.image_overview.config(image="")
                
        for i in range(0, len(self.stats)):
            #destroy old stats
            self.stats[i].destroy()
            
        stats = supabase.table("data").select("*").execute()
        checkquered = False
        i = 1
        for row in stats.data:
            name = row['article_name']
            views = row['article_views']
            left = ttk.Label(self.stat_frame, text=name)
            left.grid(row=i, column=0, sticky="w")
            right = ttk.Label(self.stat_frame, text=views)
            right.grid(row=i, column=1, sticky="e")
            self.stats.extend([left, right])
            if name == title:
                checkquered = True
                supabase.table("data").update({"article_views": row['article_views'] + 1}).eq("article_name", name).execute()
            i += 1
        if not checkquered:
            supabase.table("data").insert({"article_name": title, "article_views": 1}).execute()
            left = ttk.Label(self.stat_frame, text=title)
            left.grid(row=i, column=0, sticky="w")
            right = ttk.Label(self.stat_frame, text=1)
            right.grid(row=i, column=1, sticky="e")
            self.stats.extend([left, right])

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
        self.label_p2 = ttk.Label(self.lookup_frame, text="Lookup takes time (downloading data) and python is not multithreaded by default so it crashes.", font=("-size", 10))
        self.label_p2.grid(row=5, column=0, columnspan=2, sticky="nsew")
        
        
        #wiki info frame
        self.wiki_info_frame = ttk.LabelFrame(self, text="Wiki Info", padding=(10, 10))
        self.wiki_info_frame.grid(
            row=2, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=6, columnspan=3
        )
        #title of wiki info
        self.wiki_info_title = ttk.Label(self.wiki_info_frame, text="", font=("-size", 20, "-weight", "bold"), cursor='hand2', foreground="blue")
        self.wiki_info_title.bind("<Button-1>", lambda e: f.open_page(self.page.url))
        self.wiki_info_title.grid(row=0, column=0, sticky="nsew")
        #summary of wiki info, wrap length is 750
        self.wiki_info_summary = ttk.Label(self.wiki_info_frame, text="", wraplength=750, font=("-size", 15))
        self.wiki_info_summary.grid(row=1, column=0, sticky="nsew")
        self.summ_divider = ttk.Separator(self.wiki_info_frame, orient="horizontal", style="Divider.TSeparator")
        self.summ_divider.grid(row=3, column=0, sticky="ew", pady=10)
        #image overview
        self.image_overview = ttk.Label(self.wiki_info_frame)
        self.image_overview.grid(row=2, column=0, sticky="nsew")
        #popularity label
        self.wiki_info_popularity = ttk.Label(self.wiki_info_frame, text="", font=("-size", 15))
        self.wiki_info_popularity.grid(row=4, column=0, sticky="nsew")
        
        self.wiki_info_length = ttk.Label(self.wiki_info_frame, text="", font=("-size", 15))
        self.wiki_info_length.grid(row=5, column=0, sticky="nsew")
        
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
        
        #stat frame
        self.stat_frame = ttk.LabelFrame(self, text="WikiData Stats", padding=(20, 10))
        self.stat_frame.grid(
            row=4, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=4, columnspan=6
        )
        #give stat frame two columns
        self.stat_frame.columnconfigure(0, weight=1)
        #header labels
        self.header_left = ttk.Label(self.stat_frame, text="Article", font=("-size", 15, "-weight", "bold"))
        self.header_right = ttk.Label(self.stat_frame, text="Views", font=("-size", 15, "-weight", "bold"))
        self.header_left.grid(row=0, column=0, sticky="nsew")
        self.header_right.grid(row=0, column=1, sticky="w")

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
