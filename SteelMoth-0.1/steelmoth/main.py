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


class UserData(ObservedSubject, object):
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
    w = Tk()
    w.title(title)
    w.option_add('*tearOff', FALSE)
    w.columnconfigure(0, weight=1)
    w.columnconfigure(1, weight=0)
    w.rowconfigure(0, weight=1)
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
    def ok(self, event=None):  # @UnusedVariable
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):  # @UnusedVariable
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    # command hooks
    def validate(self):
        return 1  # override

    def apply(self):
        pass  # override


class WidgetSelector(ObservedSubject, object):
    def __init__(self, user_data, master, **kw):
        def treeview_select_event_handler(self, e):  # @UnusedVariable
            if type(self.ud.iid[self.selection()[0]]['widget']) is Toplevel:
                self.m.entryconfigure("Set Toplevel Title", state=NORMAL)
            else:
                self.m.entryconfigure("Set Toplevel Title", state=DISABLED)
            self.notify()
        self.ud = user_data
        self.w = ttk.Treeview(master)
        self.w.heading('#0', text="Widget")
        self.w.grid(**kw)
        self.w['selectmode'] = 'browse'
        self.m = self.menu()
        self.n = 1
        self.w.bind('<<TreeviewSelect>>',
                    lambda e: treeview_select_event_handler(self, e))
        self.insert_toplevel("root")
        super().__init__()

    def menu(self):
        def insert_menu(parent):
            def insert_widget_command(widget_class, widget_name):
                iid = (widget_name + '{}').format(self.n)
                p = self.w.selection()[0]
                pw = self.ud.iid[p]['widget']
                w = widget_class(pw)
                self.insert(p, 'end', iid, w)
                w.grid()
                self.n += 1
                return w, iid

            def insert_widget_with_text_command(widget_class, widget_name):
                w, iid = insert_widget_command(widget_class, widget_name)
                w.configure(text=iid)

            def insert_frame_command():
                insert_widget_command(ttk.Frame, "frame")

            def insert_label_command():
                insert_widget_with_text_command(ttk.Label, "label")

            def insert_button_command():
                insert_widget_with_text_command(ttk.Button, "button")

            def insert_checkbutton_command():
                insert_widget_with_text_command(ttk.Checkbutton, "checkbutton")

            def insert_radiobutton_command():
                insert_widget_with_text_command(ttk.Radiobutton, "radiobutton")

            def insert_entry_command():
                insert_widget_command(ttk.Entry, "entry")

            def insert_combobox_command():
                insert_widget_command(ttk.Combobox, "combobox")

            def insert_toplevel_command():
                insert_widget_command(Toplevel, "root")
            w = Menu(parent)
            w.add_command(label="Frame", command=insert_frame_command)
            w.add_command(label="Label", command=insert_label_command)
            w.add_command(label="Button", command=insert_button_command)
            w.add_command(label="Checkbutton",
                          command=insert_checkbutton_command)
            w.add_command(label="Radiobutton",
                          command=insert_radiobutton_command)
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
                    return self.e1  # initial focus

                def apply(self):
                    title = self.e1.get()
                    self.result = title
            d = SetToplevelTitleDialog(self.w)
            self.ud.iid[self.w.selection()[0]]['widget'].title(d.result)

        def delete_widget_command():
            iid = self.w.selection()[0]
            self.delete(iid)
        w = Menu(self.w)
        w.add_cascade(label="Insert", menu=insert_menu(w))
        w.add_command(label="Set Toplevel Title",
                      command=set_toplevel_title_command)
        w.add_command(label="Delete", command=delete_widget_command)
        self.w.bind('<3>', lambda e: w.post(e.x_root, e.y_root))
        return w

    def insert_toplevel(self, iid):
        w = Toplevel()
        w.title(iid)
        self.insert('', 'end', iid, w)
        w.grid()
        self.w.selection_set(iid)

    def insert(self, parent, index, iid, widget):  # @UnusedVariable
        self.ud.insert(parent, 'end', iid, widget)
        self.w.insert(parent, 'end', iid, text=iid)

    def delete(self, iid):
        p = self.w.parent(iid)
        self.ud.delete(iid)
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


class WidgetEntry(object):
    def __init__(self, user_data, selection_source, master, **kw):
        def string_var_written_callback(*args):  # @UnusedVariable
            self.ss.set_value(self.iid, self.sv.get())
        self.ud = user_data
        self.sv = StringVar()
        self.sv.trace('w', string_var_written_callback)
        self.w = ttk.Entry(master, textvariable=self.sv)
        self.w.grid(**kw)
        self.ss = selection_source

    def update(self):
        self.iid = self.ss.w.selection()[0]
        self.sv.set(self.ss.set_value(self.iid))


class MethodSelector(ObservedSubject, object):
    def __init__(self, user_data, selection_source, master, **kw):
        def treeview_select_event_handler(self, e):  # @UnusedVariable
            self.notify()
        self.ud = user_data
        self.ss = selection_source
        self.w = ttk.Treeview(master)
        self.w.heading('#0', text="Method")
        self.w.grid(**kw)
        self.w['selectmode'] = 'browse'
        self.w.bind('<<TreeviewSelect>>',
                    lambda e: treeview_select_event_handler(self, e))
        self.insert("configure(...)")
        super().__init__()

    def insert(self, iid):
        self.w.insert('', 'end', iid, text=iid)
        self.w.selection_set(iid)

    def update(self):
        self.notify()

    def selection(self):
        return self.ss.selection()


class WidgetConfiguration(ObservedSubject, object):
    def __init__(self, user_data, selection_source, master, **kw):
        def treeview_select_event_handler(self, e):  # @UnusedVariable
            self.notify()
        self.ud = user_data
        self.ss = selection_source
        self.w = ttk.Treeview(master, columns=('value'))
        self.w.heading('#0', text="Option")
        self.w.heading('value', text="Value")
        self.w.grid(**kw)
        self.w['selectmode'] = 'browse'
        self.w.bind('<<TreeviewSelect>>',
                    lambda e: treeview_select_event_handler(self, e))
        super().__init__()

    def update(self):
        iid = self.w.selection()
        for i in self.w.get_children():
            self.w.delete(i)
        w = self.ud.iid[self.ss.selection()[0]]['widget']
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
            w = self.ud.iid[self.ss.selection()[0]]['widget']
            try:
                if w[iid] != value:
                    w[iid] = value
            except TclError:
                return False
            self.w.set(iid, 'value', value)
            return True


class WidgetConfigurationEntry(object):
    def __init__(self, user_data, selection_source, master, **kw):
        def string_var_written_callback(*args):  # @UnusedVariable
            if self.ss.set_value(self.iid, self.sv.get()):
                self.w['foreground'] = '#000000'
            else:
                self.w['foreground'] = '#ff0000'
        self.ud = user_data
        self.sv = StringVar()
        self.sv.trace('w', string_var_written_callback)
        self.w = ttk.Entry(master, textvariable=self.sv)
        self.w.grid(**kw)
        self.ss = selection_source

    def update(self):
        self.iid = self.ss.w.selection()[0]
        x = self.iid
        try:
            y = self.ss.set_value(x)
            self.sv.set(y)
        except TclError:
            pass
        self.sv.set(self.ss.set_value(self.iid))


def main():
    ud = UserData()
    mw = main_window_init("Steel Moth")
    ws = WidgetSelector(ud, mw, column=0, row=0, sticky=N+W+E+S)
    we = WidgetEntry(ud, ws, mw, column=0, row=1, sticky=N+W+E+S)
    ms = MethodSelector(ud, ws, mw, column=1, row=0, sticky=N+W+E+S)
    wcs = WidgetConfiguration(ud, ms, mw, column=2, row=0, sticky=N+W+E+S)
    wce = WidgetConfigurationEntry(ud, wcs, mw, column=2, row=1,
                                   sticky=N+W+E+S)
    ud.attach(ws)
    ws.attach(we)
    ws.attach(ms)
    ms.attach(wcs)
    wcs.attach(wce)
    mw.mainloop()
if __name__ == "__main__":
    main()
