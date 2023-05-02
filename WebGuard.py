import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# import os, base64, threading, webbrowser
import platform
import os

# Get the path to the hosts file based on the operating system
if platform.system() == "Windows":
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    hosts_path = "/etc/hosts"

# save the original permission mode
original_mode = os.stat(hosts_path).st_mode

class API():

    def ReadHosts(LISTBOX):
        for i in open(r'C:\Windows\System32\drivers\etc\hosts', 'r').read().splitlines():
            if (i.startswith('#')) or (i.strip() == ''):
                continue
            Cmnd = i.split(' ')
            LISTBOX.insert(0, ' ' + Cmnd[len(Cmnd) - 1])


class GuiApp():
    def __init__(self, root):
        root.geometry('450x200')
        root.title('Web Guard')

        # Variables
        URL = tk.StringVar()

        # Text Bar
        def placeholder(varr):
            if str(URL.get()) == '< URL Here >':
                URLBar.delete(0, tk.END)
            else:
                print()

        URLBar = ttk.Entry(width=71, textvariable=URL)
        URLBar.place(x=7, y=20)
        URLBar.bind("<Button>", placeholder)
        URLBar.insert(0, '< URL Here >')

        # Buttons
        def AllowAccess():
            # Get the path to the hosts file based on the operating system
            if platform.system() == "Windows":
                hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            else:
                hosts_path = "/etc/hosts"

            # # save the original permission mode
            # original_mode = os.stat(hosts_path).st_mode
            os.chmod(hosts_path, 0o200)

        def DenyAccess():
            # Get the path to the hosts file based on the operating system
            if platform.system() == "Windows":
                hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            else:
                hosts_path = "/etc/hosts"

            # Change the permissions of the hosts file to read and write
            os.chmod(hosts_path, original_mode)

        def Quit():
            # Get the path to the hosts file based on the operating system
            if platform.system() == "Windows":
                hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            else:
                hosts_path = "/etc/hosts"

            # restore the original permission mode
            os.chmod(hosts_path, original_mode)
            exit()

        def Add():
            UrlStr = str(URL.get()).strip()
            if not (('https://' in UrlStr) or ('http://' in UrlStr) or ('www.' in UrlStr)):
                messagebox.showerror('Erorr !!', 'Please Tybe Full Url [ Ex: https://www.instagram.com ]')
                return
            if UrlStr in list(listbox.get(0, last=10000)):
                messagebox.showerror('Error !!', 'This URL is Already Added ..')
                return
            listbox.insert(0, UrlStr)

        def Remove():
            listbox.delete(tk.ANCHOR)

        def Update():
            AllWebsites = list(listbox.get(0, last=10000))
            FinalWebsites = []
            # Translate URL Syntax
            for data in AllWebsites:
                if data.startswith(' '):
                    FinalWebsites.append('127.0.0.1 ' + data.strip())
                    continue
                S = data.replace('https://', '').replace('http://', '')
                if 'www.' in S:
                    with_www = str(S)
                    without_www = S.replace('www.', '')
                    FinalWebsites.append('127.0.0.1 ' + with_www)
                    FinalWebsites.append('127.0.0.1 ' + without_www)
                else:
                    FinalWebsites.append('127.0.0.1 ' + S)

            # C:\Windows\System32\drivers\etc\hosts
            README = []
            for data in open(r'C:\Windows\System32\drivers\etc\hosts', 'r').read().splitlines():
                if (data.startswith('#')) or (data.strip() == ''):
                    README.append(data)

            try:
                Hosts = open(r'C:\Windows\System32\drivers\etc\hosts', 'w')
                Hosts.write('\n'.join(README) + '\n')
                Hosts.write('\n'.join(FinalWebsites))
                Hosts.close()
                messagebox.showinfo('Done !!', 'Blocked List Has Updated ..')
            except Exception as AdminErr:
                ERROR = str(AdminErr)[:str(AdminErr).find(':') + 1] + " 'HOSTS_FILE'"
                messagebox.showerror('Admin Error !!', f'Please Run Program as Admin :\n{ERROR}')

        addBtn = ttk.Button(root, text='Add', command=Add)
        addBtn.place(x=7, y=50)

        removeBtn = ttk.Button(root, text='Remove', command=Remove)
        removeBtn.place(x=132, y=50)

        updateBtn = ttk.Button(root, text='Update', command=Update)
        updateBtn.place(x=257, y=50)

        allowaccessBtn = ttk.Button(root, text='Allow Access', command=AllowAccess)
        allowaccessBtn.place(x=7, y=85)

        denyaccessBtn = ttk.Button(root, text='Deny Access', command=DenyAccess)
        denyaccessBtn.place(x=132, y=85)

        quitBtn = ttk.Button(root, text='Exit', command=Quit)
        quitBtn.place(x=257, y=85)



        # Sites List
        listbox = tk.Listbox(root, width=71, height=5)
        listbox.place(x=7, y=115)
        API.ReadHosts(listbox)


if __name__ == '__main__':
    TKGui = tk.Tk()
    TKGui.resizable(0, 0)
    GuiApp(TKGui)
    TKGui.mainloop()