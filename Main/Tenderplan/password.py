from tkinter import *

PASSWORD = ''


def get_passwd():
    global PASSWORD
    root = Tk()
    pwdbox = Entry(root, show='*')

    def onpwdentry(evt):
        global PASSWORD
        PASSWORD = pwdbox.get()
        root.destroy()

    def onokclick():
        global PASSWORD
        PASSWORD = pwdbox.get()
        root.destroy()

    Label(root, text='Пароль к tenderplan.ru').pack(side='top')

    pwdbox.pack(side='top')
    pwdbox.bind('<Return>', onpwdentry)
    Button(root, command=onokclick, text='OK').pack(side='top')

    root.mainloop()
    return PASSWORD
