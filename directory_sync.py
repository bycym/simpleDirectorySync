#!/usr/bin/env python3


from dirsync import sync

import os
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk

class App(object):
    def __init__(self, master, path):
        self.nodes = dict()

        master.geometry('600x400+0+0')


        pane = tk.PanedWindow(orient=tk.VERTICAL)
        pane.pack(fill=tk.BOTH)

        upper_container = tk.Frame(pane)
        upper_container.pack()


        self.SourceDirectoryButton = ttk.Button(upper_container, text="Select Source Dir", command=self.SetSourceDirectory)
        self.SourceDirectoryButton.pack(side=tk.LEFT)
        self.DestinationDirectoryButton = ttk.Button(upper_container, text="Select Destination Dir", command=self.SetDestinationDirectory)
        self.DestinationDirectoryButton.pack(side=tk.RIGHT)


        second_container = tk.Frame(pane)
        second_container.pack()

        self.sourceDirectory = tk.StringVar()
        self.sourceDirectory.set('.')
        self.destinationDirectory = tk.StringVar()
        self.destinationDirectory.set('.')

        self.sourceDirectoryLabel = tk.Label(second_container, textvariable = self.sourceDirectory)
        self.sourceDirectoryLabel.pack(side=tk.LEFT)
        self.destinationDirectoryLabel = tk.Label(second_container, textvariable = self.destinationDirectory)
        self.destinationDirectoryLabel.pack(side=tk.RIGHT)



        frame = tk.Frame(pane)
        # frame = tk.Frame(master)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) 
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Simple Directory Sync', anchor='w')


        # self.tree.grid()
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # ysb.grid(row=0, column=1, sticky='ns')
        # xsb.grid(row=1, column=0, sticky='ew')
        # frame.grid()

        abspath = os.path.abspath(path)
        self.insert_node('', abspath, abspath)
        self.tree.bind('<<TreeviewOpen>>', self.check_open_node)

        # Menu elements
        # self.menu = tk.Menu(master)
        # master.config(menu=self.menu)
        # self.fileMenu = tk.Menu(self.menu)
        # self.menu.add_cascade(label="Source Directory", menu=self.fileMenu)
        # self.fileMenu.add_command(label="Refresh", command=self.RefreshMenu)


        bottom_container = tk.Frame(pane)
        bottom_container.pack()


        self.SourceDirectoryButton = ttk.Button(bottom_container, text="Check Directory", command=self.SetSourceDirectory)
        self.SourceDirectoryButton.pack(side=tk.LEFT)
        self.DestinationDirectoryButton = ttk.Button(bottom_container, text="Synch Directory", command=self.SetDestinationDirectory)
        self.DestinationDirectoryButton.pack(side=tk.RIGHT)

        pane.add(upper_container)
        pane.add(second_container)
        pane.add(frame)
        pane.add(bottom_container)

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        print(abspath)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    def check_open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        print(abspath)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    def SetSourceDirectory(self):
        self.tree.delete(*self.tree.get_children())
        filename = filedialog.askdirectory(initialdir = ".", title = "Select directory")
        abspath = os.path.abspath(filename)
        self.insert_node('', abspath, abspath)
        self.sourceDirectory.set(abspath)
        
    def SetDestinationDirectory(self):
        filename = filedialog.askdirectory(initialdir = ".", title = "Select directory")
        abspath = os.path.abspath(filename) 
        self.destinationDirectory.set(abspath)
    
    def SyncDirectory(self):
        source_path = '/Give/Source/Folder/Here'
        target_path = '/Give/Target/Folder/Here'

        # sync(source_path, target_path, 'sync') #for syncing one way
        # sync(target_path, source_path, 'sync') #for syncing the opposite way


        # import os
        # import time
        # from dirsync import sync

        # sourcedir = "C:/sourcedir"
        # targetdir ="C:/targetdir"

        # mtime, oldmtime = None, None

        # while True:
        #     mtime = os.path.getmtime(sourcedir)
        #     if mtime != oldmtime:
        #         sync(sourcedir, targetdir, "sync")
        #         oldmtime = mtime
        #     time.sleep(60)



if __name__ == '__main__':
    root = tk.Tk()
    app = App(root, path='.')
    root.mainloop()