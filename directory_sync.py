#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import filecmp
import time
from dirsync import sync
from pathlib import Path


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

        abspath = os.path.abspath(".")

        self.sourceDirectory = tk.StringVar()
        self.sourceDirectory.set(abspath)
        self.destinationDirectory = tk.StringVar()
        self.destinationDirectory.set(abspath)

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
        self.tree.tag_configure('notSynced', 
            background='red',
            foreground="#000000"
            )


        # self.tree.grid()
        # ysb.grid(row=0, column=1, sticky='ns')
        # xsb.grid(row=1, column=0, sticky='ew')
        # frame.grid()

        abspath = os.path.abspath(path)
        self.insert_node('', abspath, abspath)
        self.tree.grid(column=1)
        self.tree.bind('<<TreeviewOpen>>', self.check_open_node)
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Menu elements
        # self.menu = tk.Menu(master)
        # master.config(menu=self.menu)
        # self.fileMenu = tk.Menu(self.menu)
        # self.menu.add_cascade(label="Source Directory", menu=self.fileMenu)
        # self.fileMenu.add_command(label="Refresh", command=self.RefreshMenu)


        bottom_container = tk.Frame(pane)
        bottom_container.pack()


        self.SourceDirectoryButton = ttk.Button(bottom_container, text="Check Directory", command=self.CheckDirectory)
        self.SourceDirectoryButton.pack(side=tk.LEFT)
        self.DestinationDirectoryButton = ttk.Button(bottom_container, text="Synch Directory", command=self.SyncDirectory)
        self.DestinationDirectoryButton.pack(side=tk.RIGHT)

        pane.add(upper_container)
        pane.add(second_container)
        pane.add(frame)
        pane.add(bottom_container)

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False, values=abspath)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        # print(abspath)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    def check_open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        # print(abspath)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    def SetSourceDirectory(self):
        self.tree.delete(*self.tree.get_children())
        self.nodes.clear()
        filename = filedialog.askdirectory(initialdir = ".", title = "Select directory")
        abspath = os.path.abspath(filename)
        self.insert_node('', abspath, abspath)
        self.sourceDirectory.set(abspath)
        
    def SetDestinationDirectory(self):
        filename = filedialog.askdirectory(initialdir = ".", title = "Select directory")
        abspath = os.path.abspath(filename) 
        self.destinationDirectory.set(abspath)
    
    def CheckDirectory(self):
        self.tree.delete(*self.tree.get_children())
        self.nodes.clear()
        self.RecursiveCheckDirectory(self.sourceDirectory.get(), self.destinationDirectory.get())
        if not self.tree.get_children():
            self.tree.insert('', 'end', text="All of the synced", open=False)
            


    def RecursiveCheckDirectory(self, sourceDirectory, destinationDirectory):
        listSourceDirectory = os.listdir(sourceDirectory)
        for sourceItem in listSourceDirectory:
            sourcePath = os.path.join(sourceDirectory, sourceItem)
            destinationPath = os.path.join(destinationDirectory, sourceItem)
            if not os.path.exists(destinationPath):
                # print(f"File '{destinationPath}' doesn't exist in destination.")
                self.insert_node('', sourceItem, destinationPath)
                return
            if os.path.isfile(sourcePath):
                print (f"File :{destinationPath}")
                print(f"source: {sourcePath}")
                isIdentical = filecmp.cmp(sourcePath, destinationPath)
                print(f"isIdentical: {isIdentical}")
                if not isIdentical:
                    self.insert_node('', sourceItem, destinationPath)
            elif os.path.isdir(sourcePath):
                self.RecursiveCheckDirectory(sourcePath, destinationPath)
            else:
                print(f'Not a directory or file {destinationPath}')
                self.insert_node('', sourceItem, destinationPath)
                    
    def OnDoubleClick(self, event):
        selected_item = self.tree.focus()
        selectedItemText = self.tree.item(selected_item, "text")
        print(f"node: {self.tree.item(selected_item)}")
        print(f"values: {self.tree.item(selected_item,'values')[0]}")

        selectedItemPath = selectedItemText

        selectedItem_Iid = item_iid = self.tree.selection()[0]
        parent_iid = self.tree.parent(item_iid)

        while parent_iid != "": 
            path = ""
            if parent_iid:
                path = self.tree.item(parent_iid)['text']
            else:
                path = self.tree.item(item_iid)['text']

            item_iid = parent_iid 
            parent_iid = self.tree.parent(item_iid)

            if parent_iid != "" and  path != "":
                selectedItemPath = f'{path}/{selectedItemPath}'


        selectedSourceItemPath = f'{self.sourceDirectory.get()}/{selectedItemPath}'
        selectedDestinationItemPath = f'{self.destinationDirectory.get()}/{selectedItemPath}'

        if os.path.isdir(selectedItemPath):
            print("Its a dir")
        else:
            print(f"{selectedSourceItemPath} and {selectedSourceItemPath}")
            try:
                if filecmp.cmp(selectedSourceItemPath, selectedDestinationItemPath):
                    print("are equal")
                else:
                    print("are NOT equal.")
            except Exception as e: #
                print(f'are NOT equal. Error: {str(e)}')
                # color = '#{:02x}{:02x}{:02x}'.format(values[0], values[1], values[2])
        self.tree.item(selectedItem_Iid, tags="notSynced")
        print(f'{selectedItem_Iid}s tag: {self.tree.item(item_iid, "tags")}')

        # print(data)

        # sync(source_path, target_path, 'sync') #for syncing one way
        # sync(target_path, source_path, 'sync') #for syncing the opposite way

    def SyncDirectory(self):
        sourceDirectory = os.listdir(self.sourceDirectory.get())
        destinationDirectory = os.listdir(self.destinationDirectory.get())
        print("return before sync")
        # return 
        sync(sourceDirectory, destinationDirectory, "sync")
        self.CheckDirectory()
        
        # mtime, oldmtime = None, None

        # while True:
        #     mtime = os.path.getmtime(sourceDirectory)
        #     if mtime != oldmtime:
        #         sync(sourceDirectory, destinationDirectory, "sync")
        #         oldmtime = mtime
        #     time.sleep(60)



if __name__ == '__main__':
    root = tk.Tk()
    app = App(root, path='.')
    root.mainloop()