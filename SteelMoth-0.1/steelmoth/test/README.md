# SteelMoth-0.1a1: Acceptance Tests


## TkDocs
* Able to layout interfaces discussed in: http://www.tkdocs.com/tutorial/index.html

### Installing Tk | The Obligatory First Program
1. Insert a button widget.
1. Set text to "Hello World".

### A First (Real) Example
1. root
  * root.title("Feet to Meters")
1. mainframe
  * mainframe = ttk.Frame(root, padding="3 3 12 12")
  * mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
  * mainframe.columnconfigure(0, weight=1)
  * mainframe.rowconfigure(0, weight=1)
1. feet_entry
  * feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
  * feet_entry.grid(column=2, row=1, sticky=(W, E))
  * feet = StringVar()
1. a Label
  * ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
  * meters = StringVar()
1. a Button
  * ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
1. a Label
  * ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
1. a Label
  * ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
1. a Label
  * ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
1. mainframe children
  * for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
1. initial focus
  * feet_entry.focus()
1. bind
  * root.bind('<Return>', calculate)

## objectbrowser
* Compare to: objectbrowser -- https://pypi.python.org/pypi/objbrowser