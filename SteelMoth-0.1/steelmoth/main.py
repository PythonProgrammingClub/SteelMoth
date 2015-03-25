#!/usr/bin/env python3


import sys  # @UnusedImport
from tkinter import *  # @UnusedWildImport
from tkinter import ttk  # @Reimport


class ObservedSubject(object):
    def __init__(self):
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)
    
    def detach(self, observer):
        self.observers.remove(observer)
    
    def notify(self):
        for o in self.observers:
            o.update()


class UserDataManager(ObservedSubject, object):
    def __init__(self):
        self.iid = {'': {'widget': None,
                         'children': [],
                         'configure': {},
                         'grid': {}}}
        super().__init__()
    
    def insert(self, parent, index, iid, widget):
        if iid in self.iid:
            raise KeyError
        elif index == 'end':
            self.iid[parent]['children'].append(iid)
        else:
            self.iid[parent]['children'][index] = iid
        self.iid[iid] = {'widget': widget,
                         'children': [],
                         'configure': widget and widget.configure() or {},
                         'grid': {}}
    
    def delete(self, iid):
        
        def recursive_delete(iid):
            for i in self.iid[iid]['children']:
                recursive_delete(i)
            del self.iid[iid]
        
        if iid not in self.iid:
            raise KeyError
        self.iid[iid]['widget'].destroy()
        recursive_delete(iid)


def main_window_init(title):
    
    def file_menu(master):
        w = Menu(master)
        w.add_command(label='New', state='disabled')
        w.add_command(label='Open...', state='disabled')
        w.add_command(label='Close', state='disabled')
        w.add_separator()
        w.add_command(label='Exit', command=sys.exit)
        return w
    
    def edit_menu(master):
        w = Menu(master)
        w.add_command(label="Undo", state='disabled')
        return w
    
    w = Tk()
    w.title(title)
    w.option_add('*tearOff', FALSE)
    w.columnconfigure(0, weight=1)
    w.columnconfigure(1, weight=0)
    w.rowconfigure(0, weight=1)
    m = Menu(w)
    w['menu'] = m
    m.add_cascade(menu=file_menu(m), label='File')
    m.add_cascade(menu=edit_menu(m), label='Edit')
    return w


class Dialog(Toplevel):
    # Adapted from: http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)
    
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass
    
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()
    
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
    
    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
    
    # command hooks
    def validate(self):
        return 1 # override
    
    def apply(self):
        pass # override


class WidgetTreeviewManager(ObservedSubject, object):
    def __init__(self, user_data_manager, master, **kw):
        
        def treeview_select_event_handler(self, e):
            if type(self.udm.iid[self.selection()[0]]['widget']) is Toplevel:
                self.m.entryconfigure("Set Toplevel Title", state=NORMAL)
            else:
                self.m.entryconfigure("Set Toplevel Title", state=DISABLED)
            self.notify()
        
        self.udm = user_data_manager
        self.w = ttk.Treeview(master)
        self.w.heading('#0', text="Widget")
        self.w.grid(**kw)
        self.w['selectmode'] = 'browse'
        self.m = self.menu()
        self.n = 1
        self.w.bind('<<TreeviewSelect>>', lambda e: treeview_select_event_handler(self, e))
        super().__init__()
    
    def menu(self):
        
        def insert_menu(parent):
            
            def insert_frame_command():
                iid = 'frame{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = ttk.Frame(pw)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            def insert_label_command():
                iid = 'label{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = ttk.Label(pw)
                w.configure(text=iid)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            def insert_button_command():
                iid = 'button{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = ttk.Button(pw)
                w.configure(text=iid)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            def insert_checkbutton_command():
                iid = 'checkbutton{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = ttk.Checkbutton(pw)
                w.configure(text=iid)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            def insert_radiobutton_command():
                iid = 'radiobutton{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = ttk.Radiobutton(pw)
                w.configure(text=iid)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            def insert_entry_command():
                iid = 'entry{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = ttk.Entry(pw)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            def insert_combobox_command():
                iid = 'combobox{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = ttk.Combobox(pw)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            def insert_toplevel_command():
                iid = 'root{}'.format(self.n)
                p = self.w.selection()[0]
                pw = self.udm.iid[p]['widget']
                w = Toplevel(pw)
                w.title(iid)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
            
            w = Menu(parent)
            w.add_command(label="Frame", command=insert_frame_command)
            w.add_command(label="Label", command=insert_label_command)
            w.add_command(label="Button", command=insert_button_command)
            w.add_command(label="Checkbutton", command=insert_checkbutton_command)
            w.add_command(label="Radiobutton", command=insert_radiobutton_command)
            w.add_command(label="Entry", command=insert_entry_command)
            w.add_command(label="Combobox", command=insert_combobox_command)
            w.add_separator()
            w.add_command(label="Toplevel", command=insert_toplevel_command)
            return w
        
        def set_toplevel_title_command():
            
            class SetToplevelTitleDialog(Dialog):
                
                def body(self, master):
                    Label(master, text="New Toplevel Title:").grid(row=0)
                    self.e1 = Entry(master)
                    self.e1.grid(row=0, column=1)
                    return self.e1 # initial focus
                
                def apply(self):
                    title = self.e1.get()
                    self.result = title
            
            d = SetToplevelTitleDialog(self.w)
            self.udm.iid[self.w.selection()[0]]['widget'].title(d.result)
        
        def delete_widget_command():
            iid = self.w.selection()[0]
            self.delete(iid)
        
        w = Menu(self.w)
        w.add_cascade(label="Insert", menu=insert_menu(w))
        w.add_command(label="Set Toplevel Title", command=set_toplevel_title_command)
        w.add_command(label="Delete", command=delete_widget_command)
        self.w.bind('<3>', lambda e: w.post(e.x_root, e.y_root))
        return w
    
    def insert_toplevel(self, iid):
        w = Toplevel()
        w.title(iid)
        self.insert('', 'end', iid, w)
        w.grid()
        self.w.selection_set(iid)
    
    def insert(self, parent, index, iid, widget):
        self.udm.insert(parent, 'end', iid, widget)
        self.w.insert(parent, 'end', iid, text=iid)
    
    def delete(self, iid):
        p = self.w.parent(iid)
        self.udm.delete(iid)
        self.w.delete(iid)
        self.w.selection_set(p)
    
    def update(self):
        self.notify()
    
    def set_value(self, iid, value=None):
        if value is None:
            return self.w.item(iid, 'text')
        else:
            return self.w.item(iid, text=value)
    
    def selection(self):
        return self.w.selection()


class WidgetEntryManager(object):
    def __init__(self, user_data_manager, master, **kw):
        
        def string_var_written_callback(*args):
            self.stm.set_value(self.iid, self.sv.get())
        
        self.udm = user_data_manager
        self.sv = StringVar()
        self.sv.trace('w', string_var_written_callback)
        self.w = ttk.Entry(master, textvariable=self.sv)
        self.w.grid(**kw)
        self.stm = None     # Source Treeview Manager
    
    def update(self):
        self.iid = self.stm.w.selection()[0]
        self.sv.set(self.stm.set_value(self.iid))


class WidgetConfigurationTreeviewManager(ObservedSubject, object):
    def __init__(self, user_data_manager, selection_source, master, **kw):
        
        def treeview_select_event_handler(self, e):
            self.notify()
        
        self.udm = user_data_manager
        self.ss = selection_source
        self.w = ttk.Treeview(master, columns=('value'))
        self.w.heading('#0', text="Option")
        self.w.heading('value', text="Value")
        self.w.grid(**kw)
        self.w['selectmode'] = 'browse'
        self.w.bind('<<TreeviewSelect>>', lambda e: treeview_select_event_handler(self, e))
        super().__init__()
    
    def update(self):
        iid = self.w.selection()
        for i in self.w.get_children():
            self.w.delete(i)
        w = self.udm.iid[self.ss.selection()[0]]['widget']
        sco = sorted(w.configure())
        for k in sco:
            self.w.insert('', 'end', k, text=k, values=(w[k]))
        if iid and iid[0] in sco:
            self.w.selection_set(iid)
            self.w.see(iid)
        else:
            self.w.selection_set(sco[0])
        self.notify()
    
    def set_value(self, iid, value=None):
        if value is None:
            return self.w.set(iid, 'value')
        else:
            w = self.udm.iid[self.ss.selection()[0]]['widget']
            try:
                if w[iid] != value:
                    w[iid] = value
            except TclError:
                return False
            self.w.set(iid, 'value', value)
            return True


class WidgetConfigurationEntryManager(object):
    def __init__(self, user_data_manager, master, **kw):
        
        def string_var_written_callback(*args):
            if self.stm.set_value(self.iid, self.sv.get()):
                self.w['foreground'] = '#000000'
            else:
                self.w['foreground'] = '#ff0000'
        
        self.udm = user_data_manager
        self.sv = StringVar()
        self.sv.trace('w', string_var_written_callback)
        self.w = ttk.Entry(master, textvariable=self.sv)
        self.w.grid(**kw)
        self.stm = None     # Source Treeview Manager
    
    def update(self):
        self.iid = self.stm.w.selection()[0]
        x = self.iid
        try:
            y = self.stm.set_value(x)
            self.sv.set(y)
        except TclError:
            pass
        self.sv.set(self.stm.set_value(self.iid))

class BaseConfigureManager(object):
    def __init__(self, user_data_manager, selection_source, master, **kw):
        self.udm = user_data_manager
        self.ss = selection_source
        self.w = ttk.Treeview(master, columns=('value'))
        self.w.heading('#0', text="Option")
        self.w.heading('value', text="Value")
        self.w.grid(**kw)
        self.w['selectmode'] = 'browse'
        self.menu()
    
    def menu(self):
        
        def insert_option_command():
            
            class InsertOptionDialog(Dialog):
                
                def body(self, master):
                    Label(master, text="Option:").grid(row=0)
                    Label(master, text="Value:").grid(row=1)
                    self.e1 = Entry(master)
                    self.e2 = Entry(master)
                    self.e1.grid(row=0, column=1)
                    self.e2.grid(row=1, column=1)
                    return self.e1 # initial focus
                
                def apply(self):
                    option = self.e1.get()
                    value = self.e2.get()
                    self.result = option, value
            
            d = InsertOptionDialog(self.w)
            self.insert(self.ss.selection()[0], 'end', d.result[0], d.result[1])
        
        def delete_option_command():
            self.delete(self.ss.selection()[0])
        
        w = Menu(self.w)
        w.add_command(label="Insert", command=insert_option_command)
        w.add_command(label="Delete", command=delete_option_command)
        self.w.bind('<3>', lambda e: w.post(e.x_root, e.y_root))
        return w


class WidgetLayoutManager(BaseConfigureManager, object):
    
    def insert(self, parent, index, iid, widget):
        pass
    
    def delete(self, iid):
        pass


class WidgetColumnConfigureManager(BaseConfigureManager, object):
    
    def insert(self, parent, index, iid, widget):
        pass
    
    def delete(self, iid):
        pass


class WidgetRowConfigureManager(BaseConfigureManager, object):
    
    def insert(self, parent, index, iid, widget):
        pass
    
    def delete(self, iid):
        pass


def main():
    udm = UserDataManager()
    mw = main_window_init("Steel Moth")
    
    wtm = WidgetTreeviewManager(udm, mw, column=0, row=0, sticky=N+W+E+S)
    wem = WidgetEntryManager(udm, mw, column=0, row=1, sticky=N+W+E+S)
    wtm.insert_toplevel("root")
    
    n = ttk.Notebook(mw)
    n.grid(column=1, row=0, sticky=N+W+E+S, rowspan=2)
    
    wcf = ttk.Frame(n)
    wcf.grid(column=0, row=0, sticky=N+W+E+S)
    wcf.rowconfigure(0, weight=1)
    n.add(wcf, text="configure()")
    wctm = WidgetConfigurationTreeviewManager(udm, wtm, wcf, column=0, row=0, sticky=N+W+E+S, columnspan=2)
    wcem = WidgetConfigurationEntryManager(udm, wcf, column=1, row=1, sticky=N+W+E+S)
    
    wlf = ttk.Frame(n)
    wlf.grid(column=0, row=0, sticky=N+W+E+S)
    wlf.columnconfigure(0, weight=1)
    wlf.rowconfigure(0, weight=1)
    n.add(wlf, text="grid()")
    wlm = WidgetLayoutManager(udm, wtm, wlf, column=0, row=0, sticky=N+W+E+S)
    
    wcolf = ttk.Frame(n)
    wcolf.grid(column=0, row=0, sticky=N+W+E+S)
    wcolf.columnconfigure(0, weight=1)
    wcolf.rowconfigure(0, weight=1)
    n.add(wcolf, text="columnconfigure()")    
    wcolcm = WidgetColumnConfigureManager(udm, wtm, wcolf, column=0, row=0, sticky=N+W+E+S)
    
    wrowf = ttk.Frame(n)
    wrowf.grid(column=0, row=0, sticky=N+W+E+S)
    wrowf.columnconfigure(0, weight=1)
    wrowf.rowconfigure(0, weight=1)
    n.add(wrowf, text="rowconfigure()")    
    wrowcm = WidgetRowConfigureManager(udm, wtm, wrowf, column=0, row=0, sticky=N+W+E+S)
    
    udm.attach(wtm)
    wtm.attach(wem)
    wtm.attach(wctm)
    wctm.attach(wcem)
    
    wem.stm = wtm
    wcem.stm = wctm
    
    mw.mainloop()


if __name__ == "__main__": main()